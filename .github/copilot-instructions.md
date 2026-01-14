# GitHub Copilot Instructions for Universal Hamiltonian Framework 🔧

Hi Copilot — this repository uses a mix of Python, Cython, and Mojo to implement a cross-domain Hamiltonian framework. Use these instructions to make focused, safe, and high-value changes.

## Quick orientation (big picture) 📌
- Core math & integrators live under `src/core/` (e.g., `PhaseSpace`, `HamiltonianSystem`).
- Symbolic derivation & compilation tooling: `src/compiler/` (see `hamiltonian_dsl.py` and `symbolic_engine.py`).
- Domain implementations: `src/domains/` (examples: `market_dynamics.py`, `bioenergetic_consciousness.py`); domain modules may be pure Python, `.pyx` or `.mojo` files.
- Visualization: `src/viz/` and `examples/` contain runnable demos.
- Meta CI automation & self-validation: `src/meta/self_cicd.py` — **always run this locally before proposing changes that modify structure or add files**.

## How to run & validate changes locally ✅
- Setup: `python -m venv .venv && .venv\Scripts\activate` (Windows) or `source .venv/bin/activate` (UNIX).
- Install: `pip install -e .[dev]` (includes test & lint tools).
- Run tests: `pytest tests/` (tests assume running from repo root; many tests insert `src` into `sys.path`).
- Run meta check: `python src/meta/self_cicd.py` — this discovers "energy voids" and suggests small, testable improvements; use it to guide low-risk changes.
- Lint & format: `black --check src/ tests/` and `ruff check src/ tests/`; type-check: `mypy src/ --ignore-missing-imports`.
- Build docs: `pip install -e .[docs]` then run your Sphinx/myst checks (docs are markdown-based in `docs/`).

## Project-specific patterns & conventions 🧭
- System definition pattern: use `@define_system` (see `src/compiler/hamiltonian_dsl.py`) to create Hamiltonian classes. Coordinate names become attributes: `q.x` / momentum `p.px` in decorated methods.
- Numerical gradient/force: many systems use a small finite-difference epsilon for `force(q)`. If you change this logic, ensure unit tests still pass (some tests rely on this implementation detail).
- Backends: Cython (`*.pyx`) and Mojo (`*.mojo`) are present. Code must provide a Python fallback if Mojo/Cython is not available — guard with the `MOJO_AVAILABLE` / `CYTHON_AVAILABLE` flags where appropriate.
- Tests often use `pytest.mark.benchmark` and `pytest.skip` for optional backends; match that style when adding new tests that rely on optional extensions.

## Files & names to reference in patches ✍️
- Core integration & PhaseSpace: `src/core/__init__.py` and `src/core/hamiltonian_engine.mojo`
- DSL & symbolic engine: `src/compiler/hamiltonian_dsl.py`, `src/compiler/symbolic_engine.py`
- Domain examples: `src/domains/market_dynamics.py`, `src/domains/bioenergetic_consciousness.py`
- Meta-CI self-check: `src/meta/self_cicd.py` (runs automatic "energy void" detection)
- Packaging & tooling: `pyproject.toml`, `.github/workflows/ci.yml` (CI runs tests, lint, docs, and Docker builds).

## How to make acceptable contributions (explicit, actionable) 📝
- Always run `pytest` and `python src/meta/self_cicd.py` locally. If `self_cicd` reports high-priority voids related to your change, address or document them in the PR description.
- Add tests to `tests/` using the project's style (file-level docstring, `test_*` functions, `pytest` markers). Prefer deterministic numeric checks (e.g., energy conservation relative error bounds already used in `tests/test_core.py`).
- Add succinct docstrings for new modules/functions and update `docs/` where reasonable.
- Use 100-char max line length (project `black` config), and follow `ruff` and `mypy` defaults.
- When introducing a new dependency, update `pyproject.toml` and run the repository's dependency verification policy (note: the repository uses kluster dependency checks locally/CI; coordinate with maintainers if unsure).

## CI & release notes ⚠️
- GitHub Actions: `.github/workflows/ci.yml` — jobs: `test`, `lint`, `build-docs`, `benchmark`, `docker`. The `docker` job pushes only when not a PR and uses `DOCKERHUB` secrets.
- Pull requests run `.github/workflows/pr_checks.yml`, which includes style checks, tests, a non-blocking meta self-validation running `python src/meta/self_cicd.py`, and a PR comment with a PASS/WARN badge.
- PRs will be automatically labeled `meta:passed` (Delta-E < 0) or `meta:review-needed` (Delta-E >= 0) to help triage.
- A daily cron run updates the meta Badge (see `.github/workflows/update_meta_status.yml`) which writes `meta/meta_shields.json` and updates the badge in `README.md` (badge message is `PASS`/`WARN`).
- The PR validation job (`.github/workflows/pr_checks.yml`) now includes a **blocking** step to validate GitHub workflow YAML (`scripts/validate_github_workflows.py`).
- Use `python scripts/validate_github_workflows.py` to locally validate GitHub workflow YAML parsing before opening a PR.
- Local smoke test with `act`: `python scripts/smoke_test_with_act.py --job update-status` (requires `act` installed: https://github.com/nektos/act).
- Docker build requires DockerHub secrets: `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN` (see the workflow for usage).
- Keep changes small and well-tested; the repository favors measurable improvements (the meta-framework tries to ensure ΔE ≤ 0 for changes).

## Safety & meta-automation precautions ⚠️
- The repo contains `src/meta/self_cicd.py` which can *modify the tree* (e.g., create `__init__.py` files). Do not blindly accept or apply all automated suggestions — validate each generated change with tests and a short human rationale in the PR.
- Avoid edits that intentionally inflate code size/complexity without measurable validation in `self_cicd`.

## Quick examples (copyable) 📎
- Adding a new domain file: `src/domains/my_new_domain.py` (include docstring header, dataclass state, and a test in `tests/test_my_new_domain.py` that validates evolution or a conserved quantity).
- Using the DSL:
  - Create class with `coordinates = ['x','y']` and define `kinetic(self,p)` and `potential(self,q)`; tests should use `define_system` to instantiate the compiled class.

## Mojo vs Cython checklist 🔧
- When to add Mojo:
  - Add Mojo (`.mojo`) for hot inner loops in `src/core/` (e.g., `hamiltonian_engine.mojo`, `propagator.mojo`).
  - Keep Mojo code minimal and numerically explicit; prefer typed arrays and avoid Python-specific runtime behavior in kernels.
  - Add a Python fallback in the same module or a sibling `.py` file gated by `MOJO_AVAILABLE`.
  - Update `mojo.toml` `sources` and `compile.flags` if adding new Mojo sources.
  - Add tests that `pytest.skip` when Mojo runtime is unavailable (use `pytest.importorskip` or runtime flags).
- When to add Cython:
  - Use Cython (`.pyx`, `.pxd`) for performance-critical bindings that require tight NumPy/C API access (see `src/domains/classical_mechanics.pyx`).
  - Provide a pure-Python implementation alongside the `.pyx` (use `CYTHON_AVAILABLE` guard and import fallbacks).
  - Add `include-package-data` entries and ensure `pyproject.toml` lists Cython in build requirements (already present).
  - Add `tests` that compile/build in CI or guard with `pytest.importorskip("cython")`.
- General guidance:
  - Document ABI/FFI assumptions in the module docstring (e.g., array layouts, dtype, column order).
  - Add small, deterministic unit tests that validate numerical outputs to within tight tolerances.

## Test templates 🧪
- Unit test for a new domain (structure):

```python
# tests/test_my_new_domain.py
import numpy as np
import pytest
from core import PhaseSpace
from compiler import define_system

@define_system
class Example:
    coordinates = ['x']
    def kinetic(self, p):
        return p.px ** 2 / 2
    def potential(self, q):
        return 0.5 * q.x ** 2


def test_energy_conservation():
    system = Example()
    initial = PhaseSpace(q=np.array([1.0]), p=np.array([0.0]))
    t, q_traj, p_traj = system.evolve(initial, t_max=1.0, dt=0.01)
    E_initial = system.hamiltonian(initial.q, initial.p)
    E_final = system.hamiltonian(q_traj[-1], p_traj[-1])
    assert abs(E_final - E_initial) / abs(E_initial) < 1e-3
```

- Mojo/Cython presence test pattern:

```python
import pytest
pytest.importorskip('mojo_runtime', reason='Mojo runtime not available')
# proceed with Mojo-specific tests
```

- Benchmark tests: use `@pytest.mark.benchmark` and keep workloads small and deterministic.

## Example PR message & checklist ✍️
Use a short Conventional Commit title and the checklist below in the PR description. Paste the output of `python src/meta/self_cicd.py` into the description (include the Delta-E result).

Title example:
```
feat(domains): add mean-reversion market Hamiltonian
```

PR description template (copy into PR body):

- Summary: One-sentence description of change and motivation
- Files changed: list key files
- Tests added: file names / short description
- Self-validation: include `python src/meta/self_cicd.py` output (Delta-E) and explain if ΔE ≥ 0 why this is acceptable
- Lint/type: confirm `black`, `ruff`, `mypy` pass locally
- Notes for reviewers: flags, performance implications, compatibility notes

---
If anything here is unclear or you'd like more examples (e.g., a PR automation that comments on Delta-E or enforces a stricter check), tell me which area to expand and I will iterate. Thanks! 🙏
