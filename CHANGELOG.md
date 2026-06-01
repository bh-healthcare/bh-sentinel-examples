# Changelog

All notable changes to `bh-sentinel-examples` are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project tracks the bh-sentinel monorepo's release cadence rather than
maintaining its own SemVer line — each version here corresponds to a specific
pinning of [`bh-sentinel-ml`](https://pypi.org/project/bh-sentinel-ml/).

## [Unreleased]

## [0.1.2] - 2026-06-01

Re-pins to `bh-sentinel-ml 0.2.3` / `bh-sentinel-core 0.1.2` and **corrects a false claim** in the 0.1.1 docs. The 0.1.1 "Observed vs designed" section reported that L2 produced zero L2-only emissions and no false positives on routine text. Both were artifacts of a Layer 2 attribution bug in `bh-sentinel-core < 0.1.2` — every flag was mislabeled `detection_layer=pattern_match`, so the report's "L2-only" bucket was structurally always empty regardless of what the transformer emitted. With the fix released, L2 actually over-fires.

### Fixed

- **`reports/sample_l1_vs_l2.md` regenerated** against `bh-sentinel-core 0.1.2` / `bh-sentinel-ml 0.2.3`. The buggy 0.1.1 run reported `L2-only = 0` / 60% agreement; the corrected run shows **`L2-only = 128`** / ~6% agreement, with false positives on all three true negatives (weather/recipe/sports).
- **README "Observed vs designed" section rewritten.** The prior text documented the attribution bug as a Phase A characteristic ("zero L2-only emissions", "no false positives on routine text"). It now states the real finding: Phase A zero-shot L2 has useful recall but unusable precision on non-clinical text; the signal and noise score distributions overlap (a real self-harm disclosure and a "don't forget your sunscreen" reminder score within 0.002 of each other); and the fix is discrimination (the Phase B clinical fine-tune), not a threshold.
- **Stale `DistilBART-MNLI` references** in the README corrected to `RoBERTa-large-MNLI` (the pinned source since `bh-sentinel-ml 0.2.2`).
- **`.gitignore` gaps closed:** `/model/` (the ~342MB downloaded ONNX was committable), `.DS_Store`, generated `reports/l1_vs_l2_*.md`, and `reports/experiment/`.

### Changed

- Dependency floors raised: `bh-sentinel-core>=0.1.2` (required for correct L1/L2 report bucketing) and `bh-sentinel-ml>=0.2.3` (adds `score_flags()`). See the bh-sentinel monorepo CHANGELOG [`[0.1.2]`](https://github.com/bh-healthcare/bh-sentinel/blob/main/CHANGELOG.md) and [`[ml-0.2.3]`](https://github.com/bh-healthcare/bh-sentinel/blob/main/CHANGELOG.md).

## [0.1.1] - 2026-05-13

First release pinning the canonical published `bh-sentinel-ml` artifact end-to-end. The previous `0.1.0` scaffold shipped before any `bh-sentinel-ml` release pinned a real ONNX model; the `sample_l1_vs_l2.md` file under `reports/` was a format-only stub.

### Changed

- Bumped `bh-sentinel-ml` dependency floor from `>=0.2.0,<0.3` to `>=0.2.2,<0.3`. `bh-sentinel-ml 0.2.2` is the first release that pins a working canonical INT8 ONNX artifact end-to-end (0.2.1 was published but yanked from PyPI due to a non-functional L2 path; see the bh-sentinel monorepo's [CHANGELOG `[ml-0.2.2]`](https://github.com/bh-healthcare/bh-sentinel/blob/main/CHANGELOG.md) entry).
- [`Makefile`](Makefile) `PINNED_REVISION` and `PINNED_SHA256` defaults now point at the v0.2.2 pinned artifact at [`bh-healthcare/roberta-large-mnli-int8-onnx`](https://huggingface.co/bh-healthcare/roberta-large-mnli-int8-onnx) on HF Hub. Operators no longer need to set these env vars manually for the `make download-model` flow.
- [`README.md`](README.md) "How the L1 vs L2 report was generated" section rewritten to reflect the v0.2.2 pinning and the actual published artifact (replaces the prior "regenerating the report requires v0.2.1 prerequisites" placeholder).
- [`reports/sample_l1_vs_l2.md`](reports/sample_l1_vs_l2.md) replaced with a real run of `make example-batch-corpus` against the v0.2.2 artifact (was a format-only stub).

### Added

- New section in the README ("Observed vs designed: an honest read of the report") documenting where the v0.2.2 L2 path lands vs the bh-sentinel main README's aspirational "what L2 is designed to target" table. The literary corpus entries (Woolf, Gilman, Tolstoy, Dostoevsky) miss their `expected_flags_hint` on both layers — that's a known Phase A characteristic, not a bug, and the documented path forward is Phase B (clinical fine-tune) in v0.3.
- Timestamped report artifact at [`reports/l1_vs_l2_ml_0_2_2.md`](reports/l1_vs_l2_ml_0_2_2.md) for audit history.
- This `CHANGELOG.md`.

### Fixed

- Maintainer email in [`pyproject.toml`](pyproject.toml) updated from the unreachable scaffold placeholder `oss@bh-healthcare.github.io` (`.github.io` domains cannot receive email) to the maintainer-controlled forwarder `oss@bh-healthcare.org`. No runtime effect; metadata-only.

## [0.1.0] - 2026-04-21

Initial scaffold of the `bh-sentinel-examples` companion repository. At this point `bh-sentinel-ml` was at `0.2.0` with placeholder pinned values in `ml_config.yaml`; the Makefile and README in this repo documented the workflow but the actual sample report was a format-only stub describing what real numbers would look like once `bh-sentinel-ml 0.2.1` shipped a real pinned artifact.

### Added

- `examples/` directory with four progressively-richer integration examples
- `data/real_world_corpus.yaml` — 11-entry shared corpus (public-domain literature + synthetic vignettes + true negatives)
- `data/clinical_fixtures/` — additional synthetic intake examples
- `scripts/run_eval.py` — shared L1 vs L2 evaluation harness
- `scripts/download_model.sh` — thin wrapper over `bh-sentinel-ml download-model`
- `Makefile` with developer entry points (`make install`, `make example-batch-corpus`, etc.)
- `reports/sample_l1_vs_l2.md` — format stub
- `tests/test_smoke.py` — smoke tests

[Unreleased]: https://github.com/bh-healthcare/bh-sentinel-examples/compare/v0.1.2...HEAD
[0.1.2]: https://github.com/bh-healthcare/bh-sentinel-examples/compare/v0.1.1...v0.1.2
[0.1.1]: https://github.com/bh-healthcare/bh-sentinel-examples/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/bh-healthcare/bh-sentinel-examples/releases/tag/v0.1.0
