"""01: Layer 1 only -- smallest possible integration.

Uses only `bh-sentinel-core`. No transformer, no model download, no
network. Fastest way to see pattern-based detection working against a
short clinical text.

Run:
    python examples/01_quick_start.py
"""

from __future__ import annotations

from bh_sentinel.core import Pipeline

SAMPLE = (
    "Patient reports active suicidal ideation for the past two days. "
    "Stopped taking her Lexapro last week because she could not afford the copay. "
    "Sleeping about 12 hours per day. No identified social supports."
)


def main() -> None:
    # No kwargs -- default Pipeline runs L1 + L3 + L4 only.
    pipeline = Pipeline()
    result = pipeline.analyze_sync(SAMPLE)

    print("=" * 70)
    print("  01: Layer 1 only")
    print("=" * 70)
    print(f"Input:\n  {SAMPLE}\n")
    print(f"Max severity:            {result.summary.max_severity}")
    print(f"Requires immediate review: {result.summary.requires_immediate_review}")
    print(f"Recommended action:      {result.summary.recommended_action or '-'}")
    print(f"Total flags:             {result.summary.total_flags}")
    print()

    if result.flags:
        print("Risk flags:")
        for flag in result.flags:
            print(
                f"  [{flag.severity}] {flag.flag_id}: {flag.name} "
                f"(confidence={flag.confidence:.2f}, temporal={flag.temporal_context})"
            )
            print(f"    {flag.basis_description}")
    else:
        print("No risk flags.")

    if result.protective_factors:
        print("\nProtective factors:")
        for flag in result.protective_factors:
            print(f"  [POSITIVE] {flag.flag_id}: {flag.name}")

    print()
    print(
        f"Pipeline status: L1={result.pipeline_status.layer_1_pattern}, "
        f"L2={result.pipeline_status.layer_2_transformer}, "
        f"L3={result.pipeline_status.layer_3_emotion_lexicon}, "
        f"L4={result.pipeline_status.layer_4_rules}"
    )


if __name__ == "__main__":
    main()
