#!/usr/bin/env bash
# Thin wrapper around `bh-sentinel-ml download-model`.
#
# Defaults match the ml_config.yaml shipped with bh-sentinel-ml 0.2.0.
# Override via env vars:
#   PINNED_REVISION=<sha>    override the HF revision
#   PINNED_SHA256=<hex64>    enable SHA256 verification on the downloaded ONNX
#   MODEL_DIR=<path>         override the output directory (default: ./model)

set -euo pipefail

MODEL_DIR="${MODEL_DIR:-model}"
PINNED_REVISION="${PINNED_REVISION:-main}"

mkdir -p "$MODEL_DIR"

if [ -n "${PINNED_SHA256:-}" ]; then
  bh-sentinel-ml download-model \
    --revision "$PINNED_REVISION" \
    --output "$MODEL_DIR" \
    --verify-sha256 "$PINNED_SHA256"
else
  echo "WARNING: PINNED_SHA256 not set -- downloading without SHA256 verification."
  echo "         For production container bakes, always pass --verify-sha256."
  bh-sentinel-ml download-model \
    --revision "$PINNED_REVISION" \
    --output "$MODEL_DIR"
fi

echo ""
echo "Downloaded model is at: $MODEL_DIR"
echo "To use it in an example, examples auto-detect ./model/ or set:"
echo "  export BH_SENTINEL_ML_CACHE=\"$(pwd)/$MODEL_DIR\""
