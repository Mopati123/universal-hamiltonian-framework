"""
Smoke and invariant tests for ApexQuantumICT.
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from domains.apex_quantum_ict import ApexQuantumICT, MarketRegime, create_initial_apex_state


def test_total_hamiltonian_is_finite():
    apex = ApexQuantumICT(n_assets=3, n_strategies=4)
    state = create_initial_apex_state(n_assets=3, n_strategies=4)

    energy = apex.H_total(state)
    assert np.isfinite(energy), "H_total should be finite"
    assert np.isscalar(energy), "H_total should be a scalar"


def test_evolve_state_preserves_shapes_and_norm():
    apex = ApexQuantumICT(n_assets=4, n_strategies=3)
    state = create_initial_apex_state(n_assets=4, n_strategies=3)

    new_state = apex.evolve_state(state, dt=0.05)

    assert new_state.prices.shape == state.prices.shape
    assert new_state.orderflows.shape == state.orderflows.shape
    assert new_state.predicted_prices.shape == state.predicted_prices.shape
    assert new_state.strategy_amplitudes.shape == state.strategy_amplitudes.shape

    norm = np.linalg.norm(new_state.strategy_amplitudes)
    assert np.isclose(norm, 1.0, atol=1e-6), "Strategy amplitudes should stay normalized"

    assert np.isfinite(apex.H_total(new_state))


def test_measure_regime_and_collapse_strategy():
    apex = ApexQuantumICT(n_assets=5, n_strategies=6)
    state = create_initial_apex_state(n_assets=5, n_strategies=6)

    regime = apex.measure_regime(state)
    assert isinstance(regime, MarketRegime)

    strategy = apex.collapse_strategy(state)
    assert 0 <= strategy < apex.n_strategies
