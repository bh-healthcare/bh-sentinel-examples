# Changelog

All notable changes to `bh-sentinel-examples` are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project tracks the bh-sentinel monorepo's release cadence rather than
maintaining its own SemVer line — each version here corresponds to a specific
pinning of [`bh-sentinel-ml`](https://pypi.org/project/bh-sentinel-ml/).

## [Unreleased]

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

[Unreleased]: https://github.com/bh-healthcare/bh-sentinel-examples/compare/v0.1.1...HEAD
[0.1.1]: https://github.com/bh-healthcare/bh-sentinel-examples/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/bh-healthcare/bh-sentinel-examples/releases/tag/v0.1.0
