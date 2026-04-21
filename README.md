# bh-sentinel-examples

**Reproducible local integrations for [`bh-sentinel`](https://github.com/bh-healthcare/bh-sentinel).**

This repo is the hands-on companion to `bh-sentinel-core` and `bh-sentinel-ml`.
Install the packages, pre-download the pinned INT8 model, and run any of the
numbered examples to see Layer 1 (pattern matching) and Layer 2 (zero-shot
transformer) in action on real text -- all locally, no cloud setup.

The examples are the honest answer to "does Layer 2 actually catch what we hope
it catches?" Run them against the checked-in corpus (public-domain literature,
synthetic clinical vignettes, true-negative everyday text) and generate a
per-entry L1-vs-L2 comparison report on your own workstation.

> **Clinical Use Notice:** `bh-sentinel` is clinical decision support software.
> It is not a diagnostic tool, not FDA-cleared, and not a substitute for clinical
> judgment. These examples are for development, validation, and teaching --
> never for autonomous clinical action. All outputs are signals for clinician
> review. See the [main repository](https://github.com/bh-healthcare/bh-sentinel)
> for the full clinical disclaimer.

---

## Prerequisites

- Python 3.11 or 3.12
- ~300MB free disk space for the downloaded model
- Internet access (one-time, for the model download)

## Install

```bash
make install            # installs the pinned bh-sentinel-core + bh-sentinel-ml from PyPI
make download-model     # one-time: fetch the pinned DistilBART-MNLI INT8 revision into ./model/
```

For development against an unreleased branch of `bh-sentinel`:

```bash
make install-local      # editable install from ../bh-sentinel/packages/bh-sentinel-{core,ml}
```

## Run the examples

```bash
make example-quickstart      # 01: simplest L1-only usage
make example-full-pipeline   # 02: L1 + L2 + L3 on a single intake
make example-batch-corpus    # 03: runs the shared corpus, writes a per-entry report
make example-offline         # 04: shows the BH_SENTINEL_ML_OFFLINE=1 production path
```

Or run any example directly:

```bash
python examples/01_quick_start.py
python examples/02_full_pipeline.py
python examples/03_batch_corpus.py --report reports/my_run.md
```

## What's in here

```
bh-sentinel-examples/
├── examples/
│   ├── 01_quick_start.py         # L1-only, smallest possible integration
│   ├── 02_full_pipeline.py       # L1 + L2 + L3 with auto-downloaded model
│   ├── 03_batch_corpus.py        # runs data/real_world_corpus.yaml, writes report
│   └── 04_container_offline.py   # demonstrates BH_SENTINEL_ML_OFFLINE + model_path
├── data/
│   ├── real_world_corpus.yaml    # public-domain literature + synthetic vignettes (11 entries)
│   └── clinical_fixtures/        # additional synthetic intake/session examples
├── scripts/
│   ├── download_model.sh         # thin wrapper over `bh-sentinel-ml download-model`
│   └── run_eval.py               # core L1 vs L2 comparison harness
├── reports/
│   └── sample_l1_vs_l2.md        # checked-in reference output from a real run
├── model/                        # gitignored; model lands here after `make download-model`
├── tests/                        # smoke tests: imports work, CLIs run, corpus loads
├── Makefile                      # developer entry points
├── pyproject.toml                # pinned dependency versions
└── README.md                     # this file
```

## Reading the L1 vs L2 report

`make example-batch-corpus` writes a markdown report with one row per corpus
entry, grouped into three buckets:

- **L1 only** -- flags caught by pattern matching alone. These are the v0.1
  baseline detections.
- **L2 only** -- new flags the transformer added on top. The interesting
  column for judging whether Layer 2 is pulling its weight.
- **Corroborated** -- flags detected by both layers. Higher-signal flags;
  the merged record carries `corroborating_layers=["transformer"]` or
  `["pattern_match"]` depending on which confidence won.

A representative report lives at [`reports/sample_l1_vs_l2.md`](reports/sample_l1_vs_l2.md).
Your run will differ slightly as the model SHA and your local hardware
may affect inference precision.

## Calibration caveat

Layer 2 ships with `FixedDiscount(0.85)` as its Phase A calibrator
(see bh-sentinel architecture §4.8). Temperature-scaling calibration
against clinician-labeled data is a v0.3 deliverable. **Do not treat
the confidence numbers in these reports as clinically validated
probabilities.** They reflect a conservative dampening of the raw
DistilBART-MNLI softmax output, which is itself uncalibrated on
clinical text. The purpose of these examples is:

1. Demonstrate the integration is wired correctly end-to-end.
2. Let teams feel the difference between deterministic patterns and
   semantic classification on text they care about.
3. Seed conversations about where L2 helps and where it hurts.

Production deployments should run their own calibration against
de-identified organizational notes before tuning thresholds. See
[bh-sentinel architecture §4.8](https://github.com/bh-healthcare/bh-sentinel/blob/main/docs/architecture.md)
for the recommended workflow.

## Regenerating the real-model report (bh-sentinel-ml v0.2.1 prerequisite)

The checked-in [`reports/sample_l1_vs_l2.md`](reports/sample_l1_vs_l2.md)
is a stub showing the report *format*. Generating a real L1 vs L2
table requires a canonical ONNX export of the DistilBART-MNLI baseline
and an exact SHA pinned in `bh-sentinel-ml`'s `ml_config.yaml`.

As of `bh-sentinel-ml 0.2.0`, the pinned revision is `"main"` and the
pinned SHA256 is a placeholder (see the TODOs in
[`bh-sentinel/config/ml/ml_config.yaml`](https://github.com/bh-healthcare/bh-sentinel/blob/main/config/ml/ml_config.yaml)).
The follow-up release `bh-sentinel-ml 0.2.1` will:

1. Export `valhalla/distilbart-mnli-12-3` (or equivalent) to ONNX
   using `optimum-cli export onnx`.
2. INT8 quantize via `onnxruntime.quantization`.
3. Host the converted artifact under the bh-healthcare HF org (or
   cite a trusted third-party ONNX conversion with a pinned SHA).
4. Update `model_revision` and `model_sha256` in `ml_config.yaml` +
   the vendored copy.
5. Add a `scripts/export_onnx.py` helper to bh-sentinel-ml for anyone
   wanting to re-export locally.

### Reproducing locally today (one-off, pre-0.2.1)

If you want to generate a real report before `0.2.1` lands:

```bash
# From this repo root:
pip install "optimum[onnxruntime]>=1.16"

# Convert the HF model to ONNX (takes 3-5 min, writes several files)
optimum-cli export onnx \
    --model valhalla/distilbart-mnli-12-3 \
    --task zero-shot-classification \
    ./model

# The exporter writes model.onnx; bh-sentinel-ml expects model_int8.onnx
# by default. Either rename or pass --onnx-filename to the CLI.
cp model/model.onnx model/model_int8.onnx

# Compute the SHA256 the TransformerClassifier will verify against:
shasum -a 256 model/model_int8.onnx

# Temporarily patch the vendored ml_config.yaml in your editable
# bh-sentinel-ml checkout to match the SHA you just computed, then:
make example-batch-corpus

# The generated report lands in ./reports/l1_vs_l2_<timestamp>.md
```

Contributions that automate this conversion + pinning flow are
welcome once `bh-sentinel-ml 0.2.1` resolves the canonical model
source.

## Contributing

Additional corpus entries (more public-domain literature, more synthetic
vignettes, more true negatives) are welcome. **Never add real clinical
notes or PHI.** Every entry must be public-domain-sourced or explicitly
synthetic.

## License

Apache License 2.0. See [LICENSE](LICENSE).
