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

## How the L1 vs L2 report was generated

As of `bh-sentinel-ml 0.2.2`, the canonical INT8 ONNX artifact is
published under the bh-healthcare HF org at
[`bh-healthcare/roberta-large-mnli-int8-onnx`](https://huggingface.co/bh-healthcare/roberta-large-mnli-int8-onnx)
(quantized export of [`FacebookAI/roberta-large-mnli`](https://huggingface.co/FacebookAI/roberta-large-mnli)),
with `model_revision` and `model_sha256` pinned in
[`bh-sentinel/config/ml/ml_config.yaml`](https://github.com/bh-healthcare/bh-sentinel/blob/main/config/ml/ml_config.yaml).
The verify-on-load SHA256 check in `TransformerClassifier` passes against
the published artifact, so `Pipeline(enable_transformer=True)` works
end-to-end on first call.

Generating a fresh report against the corpus is now a three-command flow:

```bash
make install            # pulls bh-sentinel-ml==0.2.2 from PyPI
make download-model     # one-time: fetches the pinned INT8 ONNX into ./model/
make example-batch-corpus
```

The checked-in [`reports/sample_l1_vs_l2.md`](reports/sample_l1_vs_l2.md) is a real
run of this flow against the `bh-sentinel-ml 0.2.2` artifact. Re-runs on
different hardware may produce small per-confidence differences in the
L2-only / corroborated columns due to ONNX Runtime CPU optimizations --
the structural L1-only vs L2-only split is stable.

### Observed vs designed: an honest read of the report

The bh-sentinel [main README's "What Layer 2 is designed to target"
table](https://github.com/bh-healthcare/bh-sentinel#what-layer-2-is-designed-to-target-on-the-literary-corpus)
lists aspirational L2 catches on the literary corpus -- e.g. SH-002 on
Woolf, CD-002/CD-005c on Dostoevsky, CD-003/CD-006 on Gilman. The actual
v0.2.2 run **misses all of these on both layers.** That's not a bug; it's
the architecture's `FixedDiscount(0.85)` Phase A calibration meeting
literary text honestly:

- The model has strong discrimination on direct clinical disclosure (e.g.
  it emits 0.998 entailment on "I feel hopeless..." vs "speaker expresses
  hopelessness"). All clinical vignettes get good L1+L2 coverage.
- It has weaker discrimination on metaphorical / period / conditional-mood
  literary text. Raw entailment scores tend to land in the 0.40--0.60
  range, which the conservative Phase A calibration squashes below the
  `min_emit_confidence = 0.55` emit threshold.
- L2 produces **zero** L2-only flag emissions on this corpus. L2 corroborates
  L1 detections (raising confidence on agreed signals) but doesn't add new
  detections on its own. That's a Phase A characteristic, not a Phase A goal.
- The three true-negative entries (weather, recipe, sports) correctly
  produce zero flags. No false positives on routine text.

This is the expected state at Phase A. The architecture
([`docs/architecture.md`](https://github.com/bh-healthcare/bh-sentinel/blob/main/docs/architecture.md)
§"Phased model development") commits to Phase B for the literary-coverage
gap: fine-tuning on clinician-labeled clinical NLI data once that data is
available. Until Phase B ships, L2's role is **clinical corroboration**,
not **literary semantic capture**.

If you want to re-export the artifact yourself (e.g. against a different
upstream base model, or to verify reproducibility), the upstream
[`scripts/export_onnx.py`](https://github.com/bh-healthcare/bh-sentinel/blob/main/scripts/export_onnx.py)
in the bh-sentinel monorepo is the canonical tool. See
[`docs/ml-artifact-provenance.md`](https://github.com/bh-healthcare/bh-sentinel/blob/main/docs/ml-artifact-provenance.md)
in that repo for the licensing chain and re-pinning workflow.

## Contributing

Additional corpus entries (more public-domain literature, more synthetic
vignettes, more true negatives) are welcome. **Never add real clinical
notes or PHI.** Every entry must be public-domain-sourced or explicitly
synthetic.

## License

Apache License 2.0. See [LICENSE](LICENSE).
