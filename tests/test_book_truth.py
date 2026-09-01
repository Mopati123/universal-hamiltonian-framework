from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "docs" / "book_manifest.json"
VALIDATOR = ROOT / "tools" / "validate_book_truth.py"


def run_validator(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(VALIDATOR), *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def test_book_manifest_is_canonical() -> None:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert data["book"]["chapter_count"] == 16
    assert data["book"]["certification_status"] == "certified"
    assert data["book"]["canonical_exercises"] == "docs/chapter0-exercises.md"
    assert [c["number"] for c in data["chapters"]] == list(range(16))
    assert all(c["audit_status"] == "aligned" for c in data["chapters"])


def test_book_structural_truth_validation_passes() -> None:
    result = run_validator()
    assert result.returncode == 0, result.stdout + result.stderr
    assert "BOOK STRUCTURAL VALIDATION PASS" in result.stdout


def test_book_truth_certification_passes() -> None:
    result = run_validator("--certify")
    assert result.returncode == 0, result.stdout + result.stderr
    assert "BOOK TRUTH CERTIFICATION PASS" in result.stdout
