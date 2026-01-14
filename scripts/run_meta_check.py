"""Run the repository meta self-validation and write `meta_result.json`.

This script is intentionally resilient: it will catch exceptions and always exit 0 so the PR job remains non-blocking.
"""
import json
import os
import sys


def main():
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if repo_root not in sys.path:
        sys.path.insert(0, repo_root)

    result = {
        "improved": False,
        "delta_E": None,
        "error": None,
    }

    try:
        from src.meta.self_cicd import MetaFrameworkCICD

        m = MetaFrameworkCICD(repo_root)
        res = m.run_evolution_cycle()
        result.update(res)
    except Exception as e:
        result["error"] = str(e)
        print("Meta self-check failed:", e)

    # Write result for downstream steps to consume
    out_path = os.path.join(repo_root, "meta_result.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    # Always exit 0 (non-blocking). The PR comment step will report errors.


if __name__ == "__main__":
    main()
