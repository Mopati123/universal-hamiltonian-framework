#!/usr/bin/env python3
"""Quality ratchet for Python files changed by the current branch.

New support/test Python files must be Black-, Ruff-, and mypy-clean. Legacy
`src/` modules carry pre-existing repository-wide style/type debt, so changed
legacy source files are syntax-compiled and covered by the full test suite
instead of forcing unrelated whole-file reformatting in this milestone.
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
    parser.add_argument("--base", required=True, help="Base commit SHA or ref")
    args = parser.parse_args()

    files = changed_python_files(args.base)
    if not files:
        print("No changed Python files; quality ratchet passes.")
        return 0

    strict_files = [path for path in files if not path.startswith("src/")]
    legacy_src_files = [path for path in files if path.startswith("src/")]

    print("Changed Python files:")
    for path in files:
        print(f"- {path}")

    diff_rc = run(["git", "diff", "--check", f"{args.base}...HEAD"])

    black_rc = 0
    ruff_rc = 0
    mypy_rc = 0
    if strict_files:
        black_rc = run([sys.executable, "-m", "black", "--check", "--diff", *strict_files])
        ruff_rc = run([sys.executable, "-m", "ruff", "check", *strict_files])
        mypy_rc = run(
            [
                sys.executable,
                "-m",
                "mypy",
                "--ignore-missing-imports",
                "--explicit-package-bases",
                *strict_files,
            ]
        )

    compile_rc = 0
    if legacy_src_files:
        compile_rc = run([sys.executable, "-m", "py_compile", *legacy_src_files])

    return 0 if diff_rc == 0 and black_rc == 0 and ruff_rc == 0 and mypy_rc == 0 and compile_rc == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
