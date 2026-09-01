from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "docs" / "book_manifest.json"
VALIDATOR = ROOT / "tools" / "validate_book_truth.py"


def test_book_manifest_is_structurally_valid() -> None:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert data["book"]["chapter_count"] == 16
    assert [c["number"] for c in data["chapters"]] == list(range(16))
    assert data["book"]["canonical_exercises"] == "docs/chapter0-exercises.md"


def test_book_truth_audit_schema_passes() -> None:
    result = subprocess.run(
        [sys.executable, str(VALIDATOR)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_truth_certification_is_currently_blocked() -> None:
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), "--certify"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode != 0
    assert "CERTIFICATION BLOCKED" in result.stdout
