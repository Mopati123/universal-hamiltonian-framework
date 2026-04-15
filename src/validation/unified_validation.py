"""
Unified validation runner for canonical Hamiltonians.

Builds canonical HL programs from domain adapters, checks invariants, and
feeds results into the meta-learning loop.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Dict, List, Optional, Tuple

import numpy as np

from domains.domain_adapters import CanonicalAdapterResult, default_adapters
# Import for meta-learning feedback loop


@dataclass
class InvariantResult:
    name: str
    passed: bool
    metric: float
    threshold: float
    skipped: bool = False


@dataclass
class DomainValidationResult:
    domain: str
    invariants: List[InvariantResult]
    energy_drift: float


def _finite_difference_grad(
    hamiltonian: Callable[[np.ndarray, np.ndarray], float],
    q: np.ndarray,
    p: np.ndarray,
    epsilon: float = 1e-6,
) -> Tuple[np.ndarray, np.ndarray]:
    dH_dq = np.zeros_like(q, dtype=float)
    dH_dp = np.zeros_like(p, dtype=float)

    for i in range(len(q)):
        q_plus = q.copy()
        q_minus = q.copy()
        q_plus[i] += epsilon
        q_minus[i] -= epsilon
        dH_dq[i] = (hamiltonian(q_plus, p) - hamiltonian(q_minus, p)) / (2.0 * epsilon)

    for i in range(len(p)):
        p_plus = p.copy()
        p_minus = p.copy()
        p_plus[i] += epsilon
        p_minus[i] -= epsilon
        dH_dp[i] = (hamiltonian(q, p_plus) - hamiltonian(q, p_minus)) / (2.0 * epsilon)

    return dH_dq, dH_dp


def _symplectic_euler_step(
    hamiltonian: Callable[[np.ndarray, np.ndarray], float],
    q: np.ndarray,
    p: np.ndarray,
    dt: float,
) -> Tuple[np.ndarray, np.ndarray]:
    dH_dq, _ = _finite_difference_grad(hamiltonian, q, p)
    p_new = p - dt * dH_dq
    _, dH_dp_new = _finite_difference_grad(hamiltonian, q, p_new)
    q_new = q + dt * dH_dp_new
    return q_new, p_new


def _energy_drift(
    hamiltonian: Callable[[np.ndarray, np.ndarray], float],
    q0: np.ndarray,
    p0: np.ndarray,
    dt: float,
    steps: int,
) -> float:
    q = q0.copy()
    p = p0.copy()
    h0 = hamiltonian(q, p)

    for _ in range(steps):
        q, p = _symplectic_euler_step(hamiltonian, q, p, dt)

    h1 = hamiltonian(q, p)
    return abs(h1 - h0) / (abs(h0) + 1e-12)


def estimate_lyapunov(
    hamiltonian: Callable[[np.ndarray, np.ndarray], float],
    q0: np.ndarray,
    p0: np.ndarray,
    dt: float,
    steps: int = 50,
    epsilon: float = 1e-7,
) -> float:
    """
    Estimate maximum Lyapunov exponent via trajectory divergence.
    
    For stable Hamiltonian systems, Lyapunov exponent should be near 0.
    Positive values indicate chaos; negative values indicate convergence.
    
    Uses finite difference: λ ≈ (1/t) * ln(|δz(t)| / |δz(0)|)
    """
    # Perturb initial condition
    q_perturbed = q0 + np.random.randn(len(q0)) * epsilon
    p_perturbed = p0 + np.random.randn(len(p0)) * epsilon
    
    # Evolve both trajectories
    q, p = q0.copy(), p0.copy()
    q_p, p_p = q_perturbed.copy(), p_perturbed.copy()
    
    for _ in range(steps):
        q, p = _symplectic_euler_step(hamiltonian, q, p, dt)
        q_p, p_p = _symplectic_euler_step(hamiltonian, q_p, p_p, dt)
    
    # Compute separation
    delta_z0 = np.sqrt(np.sum((q_perturbed - q0)**2) + np.sum((p_perturbed - p0)**2))
    delta_zt = np.sqrt(np.sum((q_p - q)**2) + np.sum((p_p - p)**2))
    
    # Lyapunov exponent
    t_total = steps * dt
    lyap = np.log(delta_zt / (delta_z0 + 1e-12)) / t_total
    
    return float(lyap)


def _symplectic_jacobian_det(
    hamiltonian: Callable[[np.ndarray, np.ndarray], float],
    q: np.ndarray,
    p: np.ndarray,
    dt: float,
    epsilon: float = 1e-6,
) -> float:
    state = np.concatenate([q, p]).astype(float)
    n = len(state)
    jacobian = np.zeros((n, n), dtype=float)

    base_q = q.copy()
    base_p = p.copy()
    base_next = np.concatenate(_symplectic_euler_step(hamiltonian, base_q, base_p, dt))

    for i in range(n):
        delta = np.zeros_like(state)
        delta[i] = epsilon
        q_plus = (state + delta)[: len(q)]
        p_plus = (state + delta)[len(q) :]
        next_plus = np.concatenate(_symplectic_euler_step(hamiltonian, q_plus, p_plus, dt))
        jacobian[:, i] = (next_plus - base_next) / epsilon

    return float(np.linalg.det(jacobian))


def _validate_invariants(
    adapter: CanonicalAdapterResult,
    dt: float,
    steps: int,
    max_dim_for_jacobian: int,
) -> DomainValidationResult:
    q0 = adapter.initial_q
    p0 = adapter.initial_p

    canonical_ok = len(q0) == len(p0) and len(q0) > 0
    canonical_result = InvariantResult(
        name="canonical_pairs",
        passed=canonical_ok,
        metric=float(len(q0)),
        threshold=float(len(p0)),
    )

    drift = _energy_drift(adapter.hamiltonian, q0, p0, dt, steps)
    # TIGHTENED: Threshold changed from 0.05 (5%) to 0.01 (1%)
    # For conservative Hamiltonians, energy should be nearly conserved
    # Dissipative systems will naturally have higher drift
    energy_threshold = 0.01
    energy_result = InvariantResult(
        name="energy_conservation",
        passed=drift < energy_threshold,
        metric=drift,
        threshold=energy_threshold,
    )

    # Check symplectic volume preservation
    # For high-dimensional systems, use Lyapunov exponent estimate instead
    total_dim = len(q0) + len(p0)
    if total_dim > max_dim_for_jacobian:
        # Estimate Lyapunov exponent via trajectory divergence
        det_j = estimate_lyapunov(adapter.hamiltonian, q0, p0, dt)
        # Stable dynamics: |lyapunov| < 0.1 (not chaotic)
        symplectic_ok = abs(det_j) < 0.1
        symplectic_skipped = False
    else:
        try:
            det_j = _symplectic_jacobian_det(adapter.hamiltonian, q0, p0, dt)
            symplectic_ok = abs(det_j - 1.0) < 0.1
            symplectic_skipped = False
        except Exception:
            det_j = float("nan")
            symplectic_ok = False
            symplectic_skipped = False

    symplectic_result = InvariantResult(
        name="symplectic_volume",
        passed=symplectic_ok,
        metric=det_j,
        threshold=0.1,
        skipped=symplectic_skipped,
    )

    return DomainValidationResult(
        domain=adapter.name,
        invariants=[canonical_result, energy_result, symplectic_result],
        energy_drift=drift,
    )


def run_unified_validation(
    domain_filters: Optional[List[str]] = None,
    dt: float = 0.01,
    steps: int = 100,
    meta_params_path: Optional[Path] = None,
    max_dim_for_jacobian: int = 8,
) -> Dict[str, DomainValidationResult]:
    adapters = default_adapters()
    results: Dict[str, DomainValidationResult] = {}

    for adapter in adapters:
        if domain_filters and adapter.name not in domain_filters:
            continue
        built = adapter.build()
        if not built:
            continue
        results[adapter.name] = _validate_invariants(
            built,
            dt=dt,
            steps=steps,
            max_dim_for_jacobian=max_dim_for_jacobian,
        )

    penalty = 0.0
    for result in results.values():
        for invariant in result.invariants:
            if not invariant.passed and not invariant.skipped:
                penalty += abs(invariant.metric)

    # Use MetaObjective for meta-learning (not MetaHamiltonian - semantic fix)
    from meta.self_cicd import MetaObjective
    meta = MetaObjective()
    if meta_params_path is None:
        meta_params_path = Path(__file__).resolve().parents[2] / "meta_parameters.json"
    meta.load_parameters(str(meta_params_path))
    meta.learn_from_iteration("invariant_violation", -penalty, penalty == 0.0)
    meta.save_parameters(str(meta_params_path))

    return results
