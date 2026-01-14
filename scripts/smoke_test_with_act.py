"""Smoke test GitHub workflows locally using 'act'.

Usage:
    python scripts/smoke_test_with_act.py [--job JOB]

This script checks for 'act' in PATH and runs a minimal job locally to validate workflow syntax/run.
It is a convenience smoke test and will not replace CI validation.
"""
import argparse
import shutil
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--job", default="update-status", help="Job name to run with act (default: update-status)")
    args = parser.parse_args()

    act_path = shutil.which("act")
    if not act_path:
        print("'act' is not installed or not found in PATH.")
        print("Install it from https://github.com/nektos/act or use your package manager.")
        sys.exit(2)

    cmd = [act_path, "-j", args.job, "--no-color", "-P", "ubuntu-latest=nektos/act-environments-ubuntu:18.04"]
    print("Running:", " ".join(cmd))
    try:
        subprocess.check_call(cmd)
    except subprocess.CalledProcessError as e:
        print(f"act returned non-zero exit code: {e.returncode}")
        sys.exit(e.returncode)
    except OSError as e:
        print("Failed to run 'act':", e)
        sys.exit(3)


if __name__ == "__main__":
    main()
