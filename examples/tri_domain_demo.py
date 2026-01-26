"""
Tri-domain demo: blockchain + consciousness + ApexQuantumICT.

Runs short, low-cost simulations for each domain and prints a compact summary.
Falls back to the example blockchain implementation if Polars is unavailable.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Dict

import numpy as np


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
sys.path.insert(0, str(SRC_ROOT))
sys.path.insert(0, str(REPO_ROOT))


def run_blockchain_demo() -> Dict[str, Any]:
    """Run a minimal blockchain consensus simulation."""
    try:
        from domains.blockchain_consensus import (
            BlockState,
            TachyonicBlockchainHamiltonian,
            simulate_tachyonic_blockchain,
        )

        consensus_target = "a" * 32
        hamiltonian = TachyonicBlockchainHamiltonian(
            network_mass=1.0,
            consensus_strength=1.0,
            retrocausal_coupling=0.1,
            target_block_time=10.0,
        )
        genesis = BlockState(
            state_hash="0" * 32,
            validation_rate=1.0,
            timestamp=0.0,
            block_height=0,
        )
        history = simulate_tachyonic_blockchain(
            hamiltonian=hamiltonian,
            n_blocks=12,
            consensus_target=consensus_target,
            initial_state=genesis,
        )

        first = history.chain_data[0]
        last = history.chain_data[-1]
        first_state = BlockState(
            state_hash=first["state_hash"],
            validation_rate=first["validation_rate"],
            timestamp=first["timestamp"],
            block_height=first["block_height"],
        )
        last_state = BlockState(
            state_hash=last["state_hash"],
            validation_rate=last["validation_rate"],
            timestamp=last["timestamp"],
            block_height=last["block_height"],
        )
        energy_start = hamiltonian.total_hamiltonian(first_state, consensus_target)
        energy_end = hamiltonian.total_hamiltonian(last_state, consensus_target)

        return {
            "source": "src",
            "blocks": len(history.chain_data),
            "energy_start": float(energy_start),
            "energy_end": float(energy_end),
            "energy_delta": float(energy_end - energy_start),
        }
    except Exception as exc:
        from examples.domain_blockchain import simulate_blockchain_consensus

        results = simulate_blockchain_consensus(n_nodes=4, n_steps=30, coupling=1.5)
        energy_start = float(results["energy"][0])
        energy_end = float(results["energy"][-1])
        return {
            "source": f"examples (fallback: {type(exc).__name__})",
            "blocks": int(results["states"].shape[0]),
            "energy_start": energy_start,
            "energy_end": energy_end,
            "energy_delta": energy_end - energy_start,
        }


def run_consciousness_demo() -> Dict[str, Any]:
    """Run a minimal bioenergetic consciousness evolution."""
    from domains.bioenergetic_consciousness import (
        BioenergticConsciousness,
        create_initial_state,
    )

    system = BioenergticConsciousness(retention_days=7.0)
    state = create_initial_state(retention_days=7.0)

    q0 = np.concatenate([state.psi, [state.E_bio]])
    p0 = np.concatenate([state.pi, [0.0]])
    energy_start = system.hamiltonian(q0, p0)

    for _ in range(5):
        state = system.evolve_state(state, dt=0.02)

    q1 = np.concatenate([state.psi, [state.E_bio]])
    p1 = np.concatenate([state.pi, [0.0]])
    energy_end = system.hamiltonian(q1, p1)

    return {
        "energy_start": float(energy_start),
        "energy_end": float(energy_end),
        "energy_delta": float(energy_end - energy_start),
        "phi": float(state.phi),
        "coherence": float(state.coherence),
        "cognitive_velocity": float(system.compute_cognitive_velocity(state)),
    }


def run_apex_demo() -> Dict[str, Any]:
    """Run a minimal ApexQuantumICT evolution."""
    from domains.apex_quantum_ict import (
        ApexQuantumICT,
        create_initial_apex_state,
    )

    apex = ApexQuantumICT(n_assets=3, n_strategies=4)
    state = create_initial_apex_state(n_assets=3, n_strategies=4)

    energy_start = apex.H_total(state)
    state = apex.evolve_state(state, dt=0.05)
    energy_end = apex.H_total(state)

    regime = apex.measure_regime(state)
    strategy = apex.collapse_strategy(state)

    return {
        "energy_start": float(energy_start),
        "energy_end": float(energy_end),
        "energy_delta": float(energy_end - energy_start),
        "regime": regime.value,
        "strategy": int(strategy),
    }


def main() -> None:
    np.random.seed(7)

    print("=" * 70)
    print("TRI-DOMAIN DEMO: BLOCKCHAIN + CONSCIOUSNESS + APEX")
    print("=" * 70)

    blockchain = run_blockchain_demo()
    consciousness = run_consciousness_demo()
    apex = run_apex_demo()

    print("\n[Blockchain]")
    print(f"  source: {blockchain['source']}")
    print(f"  blocks: {blockchain['blocks']}")
    print(f"  energy: {blockchain['energy_start']:.4f} -> {blockchain['energy_end']:.4f}")
    print(f"  delta:  {blockchain['energy_delta']:.4f}")

    print("\n[Consciousness]")
    print(f"  energy: {consciousness['energy_start']:.4f} -> {consciousness['energy_end']:.4f}")
    print(f"  delta:  {consciousness['energy_delta']:.4f}")
    print(f"  phi:    {consciousness['phi']:.4f}")
    print(f"  coh:    {consciousness['coherence']:.4f}")
    print(f"  v_cog:  {consciousness['cognitive_velocity']:.4f}")

    print("\n[ApexQuantumICT]")
    print(f"  energy: {apex['energy_start']:.4f} -> {apex['energy_end']:.4f}")
    print(f"  delta:  {apex['energy_delta']:.4f}")
    print(f"  regime: {apex['regime']}")
    print(f"  strat:  {apex['strategy']}")

    print("\nDone.")


if __name__ == "__main__":
    main()
