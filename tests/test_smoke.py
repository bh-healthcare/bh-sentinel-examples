"""Smoke tests for bh-sentinel-examples.

Lightweight: verifies structure, that example scripts are syntactically
valid and expose a `main()` callable, that the corpus parses, and that
the L1-only example runs to completion. Heavier L2 paths exercise the
downloaded model and are run manually -- deliberately NOT in CI.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
EXAMPLES_DIR = REPO_ROOT / "examples"
SCRIPTS_DIR = REPO_ROOT / "scripts"
DATA_DIR = REPO_ROOT / "data"


def _load_numbered_example(path: Path) -> ModuleType:
    """Import a file whose name starts with a digit (not a valid Python
    identifier) via importlib.util."""
    spec = importlib.util.spec_from_file_location(f"example_{path.stem}", path)
    assert spec and spec.loader, f"could not build spec for {path}"
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_all_example_files_expose_main() -> None:
    examples = sorted(EXAMPLES_DIR.glob("0*.py"))
    assert examples, "no numbered example files found"
    for path in examples:
        mod = _load_numbered_example(path)
        assert hasattr(mod, "main"), f"{path.name} is missing a main() entry point"
        assert callable(mod.main)


def test_run_eval_script_importable() -> None:
    from scripts import run_eval

    assert hasattr(run_eval, "run_eval")
    assert callable(run_eval.run_eval)


def test_real_world_corpus_parses() -> None:
    corpus_path = DATA_DIR / "real_world_corpus.yaml"
    assert corpus_path.exists(), "data/real_world_corpus.yaml missing"
    data = yaml.safe_load(corpus_path.read_text())
    fixtures = data.get("fixtures", [])
    assert isinstance(fixtures, list) and len(fixtures) > 0
    for fx in fixtures:
        assert "id" in fx and "text" in fx
        assert fx.get("public_domain") is True or fx.get("source") == "synthetic", (
            f"entry {fx.get('id')} must be public_domain or synthetic"
        )


def test_clinical_fixtures_parse() -> None:
    fixtures_path = DATA_DIR / "clinical_fixtures" / "intake_examples.yaml"
    assert fixtures_path.exists()
    data = yaml.safe_load(fixtures_path.read_text())
    assert isinstance(data.get("fixtures"), list)


def test_example_01_runs_end_to_end(capsys) -> None:
    """L1-only example doesn't require the model download."""
    mod = _load_numbered_example(EXAMPLES_DIR / "01_quick_start.py")
    mod.main()
    out = capsys.readouterr().out
    assert "Layer 1 only" in out
    assert "Pipeline status" in out


def test_example_04_fails_safely_without_model(capsys, monkeypatch) -> None:
    """Offline example must print the helpful message and exit clean
    when ./model/ is absent -- demonstrating the container-build-time
    failure mode."""
    # Ensure BH_SENTINEL_ML_OFFLINE is set to whatever the example will set.
    monkeypatch.delenv("BH_SENTINEL_ML_OFFLINE", raising=False)

    mod = _load_numbered_example(EXAMPLES_DIR / "04_container_offline.py")
    # The example sets BH_SENTINEL_ML_OFFLINE=1 and looks for ./model/.
    # We cannot guarantee absence globally, so just assert the call
    # returns without raising -- the structural contract.
    mod.main()
    out = capsys.readouterr().out
    assert "Offline production pattern" in out


def test_sample_report_is_present() -> None:
    """The checked-in sample L1 vs L2 report must exist so the README
    link resolves and new readers can see expected output format."""
    sample = REPO_ROOT / "reports" / "sample_l1_vs_l2.md"
    assert sample.exists()
    content = sample.read_text()
    assert "L1 vs L2" in content
    assert "Aggregate" in content
