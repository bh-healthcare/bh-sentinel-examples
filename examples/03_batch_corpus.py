"""03: Batch L1 vs L2 comparison against the shared corpus.

Runs every entry in data/real_world_corpus.yaml through both a
Pipeline(enable_transformer=False) (L1-only baseline) and a
Pipeline(enable_transformer=True) (full pipeline), then writes a
markdown report tabulating L1-only, L2-only, and corroborated flags
per entry.

Usage:
    python examples/03_batch_corpus.py [--report reports/my_run.md]

By default writes a timestamped file to reports/. Non-zero exit code if
any entry's expected_flags_hint is completely missed by both layers.
"""

from __future__ import annotations

import argparse
import os
import sys
from datetime import datetime
from pathlib import Path

# Reuse the shared eval harness.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from scripts.run_eval import run_eval  # noqa: E402


def _default_report_path() -> Path:
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return Path(__file__).resolve().parent.parent / "reports" / f"l1_vs_l2_{stamp}.md"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--corpus",
        type=Path,
        default=Path(__file__).resolve().parent.parent / "data" / "real_world_corpus.yaml",
    )
    parser.add_argument("--report", type=Path, default=None)
    parser.add_argument(
        "--model-dir",
        type=Path,
        default=Path(__file__).resolve().parent.parent / "model",
        help="Directory containing the downloaded INT8 model.",
    )
    args = parser.parse_args(argv)

    report_path = args.report or _default_report_path()
    report_path.parent.mkdir(parents=True, exist_ok=True)

    if args.model_dir.exists():
        os.environ.setdefault("BH_SENTINEL_ML_CACHE", str(args.model_dir))

    return run_eval(
        corpus_path=args.corpus,
        report_path=report_path,
        model_dir=args.model_dir if args.model_dir.exists() else None,
    )


if __name__ == "__main__":
    raise SystemExit(main())
