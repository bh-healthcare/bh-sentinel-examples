"""02: L1 + L2 + L3 full pipeline on a single intake.

Enables the transformer layer. On first run the pinned DistilBART-MNLI
revision is auto-downloaded from HuggingFace Hub into the user's cache
(or ./model/ if you ran `make download-model` first, since that sets up
the cache location this example uses).

Run:
    make download-model    # optional one-time cache prewarm
    python examples/02_full_pipeline.py
"""

from __future__ import annotations

import os
from pathlib import Path

from bh_sentinel.core import Pipeline

SAMPLE = (
    "32 yo female presents to PHP intake. Reports she has not been sleeping "
    "for three days and stopped taking her Seroquel two weeks ago because "
    "she couldn't afford the copay. Endorses active suicidal ideation with "
    "a vague plan but denies intent to act. History of one prior attempt by "
    "overdose in 2021. Reports drinking heavily since losing her job last "
    "month, approximately a pint of vodka daily. Hearing voices "
    "intermittently that tell her she is worthless. No identified social "
    "supports. Lives alone with her two cats."
)


def main() -> None:
    local_model_dir = Path(__file__).resolve().parent.parent / "model"
    model_path = local_model_dir if local_model_dir.exists() else None
    # If the local model dir exists use it + disable auto-download; otherwise
    # let bh-sentinel-ml fall back to the platformdirs cache.
    os.environ.setdefault("BH_SENTINEL_ML_CACHE", str(local_model_dir))

    pipeline = Pipeline(
        enable_patterns=True,
        enable_transformer=True,
        enable_emotion_lexicon=True,
        transformer_model_path=model_path,
        transformer_auto_download=model_path is None,
    )

    result = pipeline.analyze_sync(SAMPLE)

    print("=" * 70)
    print("  02: Full pipeline (L1 + L2 + L3 + L4)")
    print("=" * 70)
    print("Pipeline status:")
    print(f"  L1 pattern:    {result.pipeline_status.layer_1_pattern}")
    print(f"  L2 transformer:{result.pipeline_status.layer_2_transformer}")
    print(f"  L3 emotion:    {result.pipeline_status.layer_3_emotion_lexicon}")
    print(f"  L4 rules:      {result.pipeline_status.layer_4_rules}")
    print()
    print(f"Max severity:            {result.summary.max_severity}")
    print(f"Requires immediate review: {result.summary.requires_immediate_review}")
    print(f"Recommended action:      {result.summary.recommended_action or '-'}")
    print(f"Total risk flags:        {result.summary.total_flags}")
    print()

    if result.flags:
        print("Risk flags (with layer attribution):")
        for flag in result.flags:
            layers = [flag.detection_layer.value] + [
                layer.value for layer in flag.corroborating_layers
            ]
            print(
                f"  [{flag.severity}] {flag.flag_id}: {flag.name} "
                f"(confidence={flag.confidence:.2f})"
            )
            print(f"    detected by: {', '.join(layers)}")
            print(f"    {flag.basis_description}")
            print()

    if result.emotions and result.emotions.primary:
        print(f"Primary emotion: {result.emotions.primary}")
        top = sorted(
            result.emotions.category_scores.items(),
            key=lambda kv: kv[1],
            reverse=True,
        )[:5]
        for cat, score in top:
            if score > 0:
                print(f"  {cat}: {score:.2f}")


if __name__ == "__main__":
    main()
