"""Shared L1 vs L2 evaluation harness.

Runs a Pipeline(enable_transformer=False) (L1 baseline) and a
Pipeline(enable_transformer=True) (full pipeline) against every entry
in a corpus YAML, then writes a markdown report grouped into three
buckets: L1 only, L2 only, corroborated.

Imported by examples/03_batch_corpus.py. Also usable standalone:

    python scripts/run_eval.py --corpus data/real_world_corpus.yaml

The report format is stable so diffs between runs are readable when
the model revision or calibration changes.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import yaml
from bh_sentinel.core import Pipeline
from bh_sentinel.core.models.flags import DetectionLayer, LayerStatus


@dataclass
class EntryReport:
    fixture_id: str
    category: str
    source: str
    l1_only: list[str]
    l2_only: list[str]
    corroborated: list[str]
    expected: list[str]
    hint_hit_l1: list[str]
    hint_hit_l2: list[str]
    hint_missed_by_both: list[str]
    l2_status: LayerStatus


def _load_corpus(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        raise FileNotFoundError(f"corpus not found: {path}")
    data = yaml.safe_load(path.read_text())
    return list(data.get("fixtures") or [])


def _build_pipelines(model_dir: Path | None) -> tuple[Pipeline, Pipeline]:
    l1_only = Pipeline(enable_transformer=False)
    if model_dir and model_dir.exists():
        l2_pipe = Pipeline(
            enable_transformer=True,
            transformer_model_path=model_dir,
            transformer_auto_download=False,
        )
    else:
        l2_pipe = Pipeline(enable_transformer=True, transformer_auto_download=True)
    return l1_only, l2_pipe


def _classify_entry(
    entry: dict[str, Any],
    l1_only: Pipeline,
    l2_pipe: Pipeline,
) -> EntryReport:
    text = entry["text"]
    expected = list(entry.get("expected_flags_hint") or [])

    r1 = l1_only.analyze_sync(text)
    r2 = l2_pipe.analyze_sync(text)

    r1_flags = [f.flag_id for f in list(r1.flags) + list(r1.protective_factors)]
    l1_ids = set(r1_flags)

    merged = list(r2.flags) + list(r2.protective_factors)
    l2_primary_ids = {f.flag_id for f in merged if f.detection_layer == DetectionLayer.TRANSFORMER}
    corroborated = {
        f.flag_id
        for f in merged
        if f.corroborating_layers  # any non-empty list means cross-layer agreement
    }

    return EntryReport(
        fixture_id=entry["id"],
        category=entry.get("category", "?"),
        source=str(entry.get("source", "?")),
        l1_only=sorted(l1_ids - (l2_primary_ids | corroborated)),
        l2_only=sorted(l2_primary_ids - l1_ids),
        corroborated=sorted(corroborated),
        expected=sorted(expected),
        hint_hit_l1=sorted(set(expected) & l1_ids),
        hint_hit_l2=sorted(set(expected) & (l2_primary_ids | corroborated)),
        hint_missed_by_both=sorted(set(expected) - (l1_ids | l2_primary_ids | corroborated)),
        l2_status=r2.pipeline_status.layer_2_transformer,
    )


def _format_report(reports: list[EntryReport], corpus_path: Path) -> str:
    lines: list[str] = []
    lines.append(f"# L1 vs L2 comparison -- {corpus_path.name}")
    lines.append("")
    lines.append(f"- Generated: `{datetime.now(UTC).isoformat()}`")
    lines.append(f"- Corpus: `{corpus_path}`")
    lines.append(f"- Entries: {len(reports)}")
    l2_ok = sum(1 for r in reports if r.l2_status == LayerStatus.COMPLETED)
    lines.append(f"- L2 completed cleanly on: {l2_ok}/{len(reports)} entries")
    lines.append("")

    # Per-entry section.
    for r in reports:
        lines.append(f"## `{r.fixture_id}` ({r.category})")
        lines.append(f"*Source:* {r.source}")
        lines.append("")
        lines.append("| Bucket | Flag IDs |")
        lines.append("|---|---|")
        lines.append(f"| L1 only | {', '.join(r.l1_only) or '_none_'} |")
        lines.append(f"| L2 only | {', '.join(r.l2_only) or '_none_'} |")
        lines.append(f"| Corroborated (both) | {', '.join(r.corroborated) or '_none_'} |")
        if r.expected:
            lines.append(f"| Expected hint | {', '.join(r.expected)} |")
            lines.append(f"| Hint hit by L1 | {', '.join(r.hint_hit_l1) or '_none_'} |")
            lines.append(f"| Hint hit by L2 | {', '.join(r.hint_hit_l2) or '_none_'} |")
            lines.append(
                f"| Hint missed by both | {', '.join(r.hint_missed_by_both) or '_none_'} |"
            )
        lines.append("")

    # Aggregate.
    total_l1_only = sum(len(r.l1_only) for r in reports)
    total_l2_only = sum(len(r.l2_only) for r in reports)
    total_both = sum(len(r.corroborated) for r in reports)
    total = total_l1_only + total_l2_only + total_both
    agreement = (total_both / total) if total else 0.0

    lines.append("## Aggregate")
    lines.append("")
    lines.append(f"- L1-only flag emissions: {total_l1_only}")
    lines.append(f"- L2-only flag emissions: {total_l2_only}")
    lines.append(f"- Corroborated (both layers agreed): {total_both}")
    lines.append(f"- L1/L2 agreement rate: {agreement:.1%}")
    lines.append("")
    lines.append(
        "> Agreement rate is informational, not a quality gate. L1 and L2 "
        "are measuring different things; agreement simply indicates overlap "
        "where both layers had strong-enough signal to emit."
    )

    return "\n".join(lines) + "\n"


def run_eval(
    *,
    corpus_path: Path,
    report_path: Path,
    model_dir: Path | None = None,
) -> int:
    """Run the L1 vs L2 evaluation end-to-end and write the report.

    Returns a process exit code: 0 if every entry's expected_flags_hint
    is covered by at least one layer, 1 if any hint is completely
    missed. Non-zero exit is a soft signal, not a hard quality claim --
    literary corpus entries are allowed to have hints neither layer
    catches without invalidating the run.
    """
    corpus = _load_corpus(corpus_path)
    l1_only, l2_pipe = _build_pipelines(model_dir)

    reports = [_classify_entry(entry, l1_only, l2_pipe) for entry in corpus]

    report_text = _format_report(reports, corpus_path)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report_text)

    print(f"Wrote L1 vs L2 report: {report_path}")
    print(
        f"Entries: {len(reports)}, "
        f"L2 completed on {sum(1 for r in reports if r.l2_status == LayerStatus.COMPLETED)}"
    )

    any_hint_missed = any(r.hint_missed_by_both for r in reports if r.expected)
    return 1 if any_hint_missed else 0


def _main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--corpus",
        type=Path,
        default=Path(__file__).resolve().parent.parent / "data" / "real_world_corpus.yaml",
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=Path(__file__).resolve().parent.parent / "reports" / "l1_vs_l2_latest.md",
    )
    parser.add_argument(
        "--model-dir",
        type=Path,
        default=Path(__file__).resolve().parent.parent / "model",
    )
    args = parser.parse_args(argv)
    return run_eval(
        corpus_path=args.corpus,
        report_path=args.report,
        model_dir=args.model_dir if args.model_dir.exists() else None,
    )


if __name__ == "__main__":
    raise SystemExit(_main())
