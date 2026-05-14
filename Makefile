# bh-sentinel-examples Makefile
# Developer entry points for running the examples and regenerating reports.

SHELL := /bin/bash
PYTHON ?= python3.11
MODEL_DIR := model

# Pinned values for the canonical bh-sentinel-ml >= 0.2.2 artifact hosted at
# https://huggingface.co/bh-healthcare/roberta-large-mnli-int8-onnx. These
# defaults must match config/ml/ml_config.yaml in the bh-sentinel repo. When
# bh-sentinel-ml ships a new pinned model, bump both values here and in
# bh-sentinel's ml_config.yaml in lockstep -- see bh-sentinel's
# docs/ml-artifact-provenance.md for the full re-pinning workflow.
PINNED_REVISION ?= 69eb03178c210deceb076f0a8302bc5705179a58
PINNED_SHA256   ?= 49fa5562da7f1422525e88fd1145d2d06ca93b17c335adf3c4696a30908c91de

.PHONY: help install install-local download-model \
        example-quickstart example-full-pipeline example-batch-corpus example-offline \
        eval test lint format clean

help:
	@echo "bh-sentinel-examples targets:"
	@echo ""
	@echo "  install             Install pinned bh-sentinel-core + bh-sentinel-ml from PyPI"
	@echo "  install-local       Editable install from ../bh-sentinel (for development)"
	@echo "  download-model      Fetch the pinned DistilBART-MNLI INT8 revision into ./model/"
	@echo ""
	@echo "  example-quickstart       Run examples/01_quick_start.py"
	@echo "  example-full-pipeline    Run examples/02_full_pipeline.py"
	@echo "  example-batch-corpus     Run examples/03_batch_corpus.py (writes a report)"
	@echo "  example-offline          Run examples/04_container_offline.py"
	@echo ""
	@echo "  eval                Alias for example-batch-corpus"
	@echo "  test                pytest tests/"
	@echo "  lint                ruff check + ruff format --check"
	@echo "  format              ruff check --fix + ruff format"
	@echo "  clean               Remove caches and generated reports (preserves sample_l1_vs_l2.md)"

install:
	$(PYTHON) -m pip install -e ".[dev]"

install-local:
	$(PYTHON) -m pip install -e ../bh-sentinel/packages/bh-sentinel-core \
	                         -e ../bh-sentinel/packages/bh-sentinel-ml \
	                         -e ".[dev]"

download-model:
	@mkdir -p $(MODEL_DIR)
	@if [ -n "$(PINNED_SHA256)" ]; then \
	  bh-sentinel-ml download-model \
	    --revision $(PINNED_REVISION) \
	    --output $(MODEL_DIR) \
	    --verify-sha256 $(PINNED_SHA256); \
	else \
	  bh-sentinel-ml download-model \
	    --revision $(PINNED_REVISION) \
	    --output $(MODEL_DIR); \
	fi

example-quickstart:
	$(PYTHON) examples/01_quick_start.py

example-full-pipeline:
	$(PYTHON) examples/02_full_pipeline.py

example-batch-corpus:
	$(PYTHON) examples/03_batch_corpus.py

example-offline:
	$(PYTHON) examples/04_container_offline.py

eval: example-batch-corpus

test:
	$(PYTHON) -m pytest tests/ -v

lint:
	ruff check examples scripts tests
	ruff format --check examples scripts tests

format:
	ruff check --fix examples scripts tests
	ruff format examples scripts tests

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .ruff_cache -exec rm -rf {} + 2>/dev/null || true
	find reports -type f -name 'l1_vs_l2_*.md' -not -name 'sample_l1_vs_l2.md' -delete 2>/dev/null || true
