<!-- PR title should follow Conventional Commits -->

## Summary
- Short description of the change and why it matters.

## Files changed
- List the most important files changed (top-level):

## Checklist (required before requesting review)
- [ ] Tests: `pytest tests/` all pass locally
- [ ] Meta-check: Ran `python src/meta/self_cicd.py` and pasted the output below (include Delta-E)
- [ ] Tests added for new behavior (file names)
- [ ] Documentation updated (`docs/` or module docstrings)
- [ ] Formatting & types: `black --check`, `ruff check`, `mypy` passed
- [ ] Mojo/Cython additions include a Python fallback and tests guarded with `pytest.importorskip`
- [ ] New dependencies added to `pyproject.toml` and kluster dependency check performed

## Self-validation output (paste here)
```
# Paste the stdout of: python src/meta/self_cicd.py
```

## Notes for reviewers
- Any special instructions, flags, or performance considerations.


Thank you! Please include reviewers and any relevant issue numbers in the PR body.