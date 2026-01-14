"""Simple workflow validator: checks that YAML syntax is valid for files under .github/workflows

Usage:
    python scripts/validate_github_workflows.py

This is a small smoke check that helps when running workflows locally via `act` or during local development.
"""

import glob
import sys

try:
    import yaml
except Exception:
    print("PyYAML not installed. Install with: pip install pyyaml")
    sys.exit(2)

ok = True
for path in glob.glob('.github/workflows/*.yml') + glob.glob('.github/workflows/*.yaml'):
    print(f"Validating: {path}")
    try:
        with open(path, 'r', encoding='utf-8') as f:
            yaml.safe_load(f)
        print("  OK")
    except Exception as e:
        ok = False
        print(f"  ERROR parsing {path}: {e}")

if not ok:
    print("One or more workflow files failed validation")
    sys.exit(1)
else:
    print("All workflows parse successfully")
    sys.exit(0)
