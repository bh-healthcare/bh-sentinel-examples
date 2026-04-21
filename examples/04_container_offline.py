"""04: Production / VPC-isolated pattern demonstration.

Shows the offline rail that a Lambda or container would use. Fails fast
with a PHI-safe static error if the model is not pre-baked at the
expected location. The purpose is to validate the offline path locally
before it ships in a real container image.

Expected usage inside a Dockerfile:

    RUN pip install bh-sentinel-ml
    RUN bh-sentinel-ml download-model --output /opt/bh-sentinel-ml/model \\
          --revision <pinned_sha> --verify-sha256 <pinned_onnx_sha256>
    ENV BH_SENTINEL_ML_OFFLINE=1

Then at runtime the handler constructs the pipeline with
transformer_model_path pointing at /opt/bh-sentinel-ml/model and
transformer_auto_download=False. This example does the same thing
pointing at ./model/ so you can see the semantics locally.

Run:
    make download-model
    python examples/04_container_offline.py
"""

from __future__ import annotations

import os
from pathlib import Path

from bh_sentinel.core import Pipeline

SAMPLE = (
    "Patient expresses feeling like a burden to her family and "
    "questions the point of continuing treatment."
)


def main() -> None:
    model_dir = Path(__file__).resolve().parent.parent / "model"
    os.environ["BH_SENTINEL_ML_OFFLINE"] = "1"

    print("=" * 70)
    print("  04: Offline production pattern")
    print("=" * 70)
    print(f"BH_SENTINEL_ML_OFFLINE={os.environ['BH_SENTINEL_ML_OFFLINE']}")
    print(f"transformer_model_path={model_dir}")
    print("transformer_auto_download=False")
    print()

    if not model_dir.exists():
        print("Model directory not found. Run `make download-model` first.")
        print(
            "This demonstrates the expected failure mode: production containers "
            "that do not pre-bake the model get a clean PHI-safe error."
        )
        return

    pipeline = Pipeline(
        enable_transformer=True,
        transformer_model_path=model_dir,
        transformer_auto_download=False,
    )
    result = pipeline.analyze_sync(SAMPLE)

    print(f"L2 status: {result.pipeline_status.layer_2_transformer}")
    print(f"Flags detected: {len(result.flags)}")
    for flag in result.flags:
        print(f"  [{flag.severity}] {flag.flag_id}: {flag.name}")


if __name__ == "__main__":
    main()
