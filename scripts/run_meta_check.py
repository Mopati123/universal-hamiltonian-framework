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
        "applied": [],
        "E_initial": 0,
        "E_final": 0,
    }

    try:
        from src.meta.self_cicd import MetaFrameworkCICD

        m = MetaFrameworkCICD(repo_root)
        res = m.run_evolution_cycle()
        result.update(res)
        
        # Validate critical fields
        if 'delta_E' not in result:
            result['error'] = "Missing delta_E in meta check result"
        if 'improved' not in result:
            result['error'] = "Missing improved field in meta check result"
            
    except ImportError as e:
        result["error"] = f"Failed to import MetaFrameworkCICD: {e}"
        print(f"[ERROR] Import error: {e}")
    except Exception as e:
        result["error"] = str(e)
        print(f"[ERROR] Meta self-check failed: {e}")
        import traceback
        traceback.print_exc()

    # Write result for downstream steps to consume
    out_path = os.path.join(repo_root, "meta_result.json")
    try:
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)
        print(f"[INFO] Meta check result written to {out_path}")
        
        # Validate JSON was written correctly
        with open(out_path, "r", encoding="utf-8") as f:
            validated = json.load(f)
        print(f"[INFO] Result validation successful")
        
    except json.JSONDecodeError as e:
        print(f"[ERROR] Failed to write valid JSON to {out_path}: {e}")
        sys.exit(2)
    except IOError as e:
        print(f"[ERROR] Failed to write result file: {e}")
        sys.exit(2)
    except Exception as e:
        print(f"[ERROR] Unexpected error writing result: {e}")
        sys.exit(2)

    # Always exit 0 (non-blocking). The PR comment step will report errors.
    sys.exit(0)


if __name__ == "__main__":
    main()
