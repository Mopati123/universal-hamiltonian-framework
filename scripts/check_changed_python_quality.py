#!/usr/bin/env python3
"""Run Black and Ruff only on Python files changed by the current PR.

This is a ratchet: existing formatting debt in untouched legacy files does not
block unrelated work, while new or modified Python files must be clean.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def changed_python_files(base: str) -> list[str]:
    result = subprocess.run(
        [
            "git",
            "diff",
            "--name-only",
            "--diff-filter=ACMR",
            f"{base}...HEAD",
            "--",
            "*.py",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def run(cmd: list[str]) -> int:
    print("+", " ".join(cmd))
    return subprocess.run(cmd, cwd=ROOT, check=False).returncode


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", required=True, help="Base commit SHA for the pull request")
    args = parser.parse_args()

    files = changed_python_files(args.base)
    if not files:
        print("No changed Python files; quality ratchet passes.")
        return 0

    print("Changed Python files:")
    for path in files:
        print(f"- {path}")

    black_rc = run([sys.executable, "-m", "black", "--check", "--diff", *files])
    ruff_rc = run([sys.executable, "-m", "ruff", "check", *files])
    mypy_rc = run(
        [
            sys.executable,
            "-m",
            "mypy",
            "--ignore-missing-imports",
            "--explicit-package-bases",
            *files,
        ]
    )
    return 0 if black_rc == 0 and ruff_rc == 0 and mypy_rc == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
