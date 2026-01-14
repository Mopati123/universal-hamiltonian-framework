"""
Run unified canonical validation and report invariant status.

Usage:
    python scripts/run_unified_validation.py --domains markets bioenergetic_consciousness
"""

import argparse
import json
from pathlib import Path

from validation.unified_validation import run_unified_validation


def main() -> int:
    parser = argparse.ArgumentParser(description="Unified Hamiltonian validation runner")
    parser.add_argument(
        "--domains",
        nargs="*",
        help="Optional list of domain adapters to run",
    )
    parser.add_argument("--dt", type=float, default=0.01)
    parser.add_argument("--steps", type=int, default=100)
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()

    results = run_unified_validation(
        domain_filters=args.domains or None,
        dt=args.dt,
        steps=args.steps,
    )

    summary = {}
    for name, result in results.items():
        summary[name] = {
            "energy_drift": result.energy_drift,
            "invariants": [
                {
                    "name": invariant.name,
                    "passed": invariant.passed,
                    "metric": invariant.metric,
                    "threshold": invariant.threshold,
                    "skipped": invariant.skipped,
                }
                for invariant in result.invariants
            ],
        }

    print(json.dumps(summary, indent=2))

    if args.output:
        args.output.write_text(json.dumps(summary, indent=2))
        print(f"Wrote report to {args.output}")

    failed = any(
        not invariant["passed"]
        for domain in summary.values()
        for invariant in domain["invariants"]
    )
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
