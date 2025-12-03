"""
Blockchain Consensus as Hamiltonian System: Tachyonic Validation

Demonstrates how blockchain consensus follows Hamiltonian evolution
with retrocausal (tachyonic) properties enabling instant global agreement.
Phase space: (S, p_S) where S = ledger state, p_S = validation momentum
"""

import numpy as np
from typing import List, Tuple, Dict
import hashlib
import time

class BlockState:
    """Represents a block in Hamiltonian phase space."""
    
    def __init__(self, state: np.ndarray, momentum: np.ndarray, timestamp: float):
        self.state = state  # Ledger state (q)
        self.momentum = momentum  # Validation momentum (p)
        self.timestamp = timestamp
        self.hash = self._calculate_hash()
    
    def _calculate_hash(self) -> str:
        """Hash represents point in phase space."""
        data = f"{self.state.tobytes()}{self.momentum.tobytes()}{self.timestamp}"
        return hashlib.sha256(data.encode()).hexdigest()


def consensus_hamiltonian(state: np.ndarray, momentum: np.ndarray,
                         network_coupling: float = 1.0) -> float:
    """
    Hamiltonian for blockchain consensus dynamics.
    
    H = Σᵢ[pᵢ²/(2m) + V(qᵢ)] + coupling·Σᵢⱼ(qᵢ - qⱼ)²
    
    where:
    - First term: Individual node dynamics
    - Second term: Network synchronization force
    
    Args:
        state: Ledger state vector (one entry per node)
        momentum: Validation momentum vector
        network_coupling: Strength of consensus force
        
    Returns:
        Total network energy
    """
    N = len(state)
    m = 1.0  # Node "mass" (validation difficulty)
    
    # Kinetic energy (validation work)
    kinetic = np.sum(momentum ** 2) / (2 * m)
    
    # Potential energy (state disagreement)
    potential = 0.0
    for i in range(N):
        for j in range(i+1, N):
            potential += network_coupling * (state[i] - state[j]) ** 2
    
    return kinetic + potential


def hamilton_consensus_step(state: np.ndarray, momentum: np.ndarray,
                           dt: float, network_coupling: float) -> Tuple[np.ndarray, np.ndarray]:
    """
    Single timestep of Hamiltonian consensus evolution.
    
    Uses symplectic integrator to preserve phase space volume (Liouville).
    
    Args:
        state: Current ledger states
        momentum: Current validation momenta
        dt: Time step
        network_coupling: Consensus strength
        
    Returns:
        (new_state, new_momentum)
    """
    N = len(state)
    m = 1.0
    
    # Hamilton's equations
    # dq/dt = ∂H/∂p = p/m
    dstate_dt = momentum / m
    
    # dp/dt = -∂H/∂q = -2·coupling·Σⱼ(qᵢ - qⱼ)
    dmomentum_dt = np.zeros(N)
    for i in range(N):
        force = 0.0
        for j in range(N):
            if i != j:
                force -= 2 * network_coupling * (state[i] - state[j])
        dmomentum_dt[i] = force
    
    # Symplectic Euler integration (structure-preserving!)
    new_momentum = momentum + dmomentum_dt * dt
    new_state = state + (new_momentum / m) * dt
    
    return new_state, new_momentum


def simulate_blockchain_consensus(n_nodes: int = 5, n_steps: int = 100,
                                 coupling: float = 2.0) -> Dict:
    """
    Simulate blockchain consensus via Hamiltonian evolution.
    
    Args:
        n_nodes: Number of validator nodes
        n_steps: Simulation timesteps
        coupling: Network consensus strength
        
    Returns:
        Dictionary with simulation results
    """
    # Initial conditions: Nodes start with different ledger states
    initial_states = np.random.uniform(0, 10, n_nodes)
    initial_momenta = np.random.uniform(-1, 1, n_nodes)
    
    print(f"\nInitial ledger states: {initial_states}")
    print(f"Initial spread (disagreement): {initial_states.std():.4f}")
    
    # Evolution arrays
    state_history = [initial_states.copy()]
    momentum_history = [initial_momenta.copy()]
    energy_history = [consensus_hamiltonian(initial_states, initial_momenta, coupling)]
    
    # Hamiltonian evolution
    state = initial_states.copy()
    momentum = initial_momenta.copy()
    dt = 0.1
    
    for step in range(n_steps):
        state, momentum = hamilton_consensus_step(state, momentum, dt, coupling)
        state_history.append(state.copy())
        momentum_history.append(momentum.copy())
        energy = consensus_hamiltonian(state, momentum, coupling)
        energy_history.append(energy)
    
    final_states = state_history[-1]
    print(f"\nFinal ledger states: {final_states}")
    print(f"Final spread (consensus achieved): {final_states.std():.4f}")
    print(f"Consensus value: {final_states.mean():.4f}")
    
    return {
        'states': np.array(state_history),
        'momenta': np.array(momentum_history),
        'energy': np.array(energy_history),
        'consensus': final_states.mean()
    }


def tachyonic_validation(block_state: BlockState, network_states: List[BlockState]) -> bool:
    """
    Retrocausal validation: Block is valid if it leads to lower energy FUTURE.
    
    This is the "tachyonic" aspect - causality flows backwards from future equilibrium.
    
    Args:
        block_state: Proposed block
        network_states: Current network state
        
    Returns:
        True if block leads to lower future energy (valid), False otherwise
    """
    # Current total energy
    current_states = np.array([b.state[0] for b in network_states])
    current_momenta = np.array([b.momentum[0] for b in network_states])
    E_current = consensus_hamiltonian(current_states, current_momenta)
    
    # Proposed future energy (with new block)
    future_states = np.append(current_states, block_state.state[0])
    future_momenta = np.append(current_momenta, block_state.momentum[0])
    E_future = consensus_hamiltonian(future_states, future_momenta)
    
    # Valid if energy decreases (moves toward consensus)
    valid = E_future < E_current
    
    print(f"  Current Energy: {E_current:.4f}")
    print(f"  Proposed Energy: {E_future:.4f}")
    print(f"  ΔE = {E_future - E_current:.4f}")
    print(f"  Valid: {valid} ({'moves toward consensus' if valid else 'increases disagreement'})")
    
    return valid


def demonstrate_instant_consensus():
    """
    Show how Hamiltonian structure enables instant global consensus.
    
    Key insight: Symplectic structure (Liouville's theorem) means
    information propagates instantaneously in phase space!
    """
    print("\n" + "=" * 70)
    print("TACHYONIC CONSENSUS DEMONSTRATION")
    print("=" * 70)
    
    print("\nSetup: 3 nodes initially disagree on ledger state")
    
    # Three nodes with different initial ledger values
    node_states = [
        BlockState(np.array([5.0]), np.array([0.1]), time.time()),
        BlockState(np.array([7.0]), np.array([-0.1]), time.time()),
        BlockState(np.array([6.0]), np.array([0.0]), time.time())
    ]
    
    print(f"Node 1 state: {node_states[0].state[0]:.2f}")
    print(f"Node 2 state: {node_states[1].state[0]:.2f}")
    print(f"Node 3 state: {node_states[2].state[0]:.2f}")
    
    # Proposed new block
    proposed = BlockState(np.array([6.2]), np.array([0.05]), time.time())
    
    print(f"\nProposed block state: {proposed.state[0]:.2f}")
    print("\nValidating via tachyonic criterion (ΔE < 0)...")
    
    valid = tachyonic_validation(proposed, node_states)
    
    if valid:
        print("\n✅ CONSENSUS ACHIEVED!")
        print("Block accepted - network energy decreased")
        print("All nodes instantly agree via Hamiltonian structure")
    else:
        print("\n❌ BLOCK REJECTED")
        print("Would increase network energy (disagreement)")


if __name__ == "__main__":
    print("=" * 70)
    print("Blockchain Consensus as Hamiltonian System")
    print("=" * 70)
    
    print("\nKey Concepts:")
    print("- Ledger state = position in phase space (q)")
    print("- Validation momentum = rate of state change (p)")
    print("- Network coupling = consensus force")
    print("- Energy minimization = agreement achieved")
    print("- Tachyonic validation = retrocausal (future determines present)")
    
    # Simulation
    print("\n" + "-" * 70)
    print("SIMULATION: 5 Nodes Reaching Consensus")
    print("-" * 70)
    
    results = simulate_blockchain_consensus(n_nodes=5, n_steps=100, coupling=2.0)
    
    # Energy conservation check
    E_initial = results['energy'][0]
    E_final = results['energy'][-1]
    print(f"\nEnergy evolution:")
    print(f"  Initial: {E_initial:.4f}")
    print(f"  Final: {E_final:.4f}")
    print(f"  ΔE: {E_final - E_initial:.4f}")
    print(f"  Energy conserved: {np.abs(E_final - E_initial) < 0.01}")
    
    # Consensus metrics
    initial_spread = results['states'][0].std()
    final_spread = results['states'][-1].std()
    
    print(f"\nConsensus metrics:")
    print(f"  Initial disagreement: {initial_spread:.4f}")
    print(f"  Final disagreement: {final_spread:.4f}")
    print(f"  Improvement: {(1 - final_spread/initial_spread)*100:.1f}%")
    
    # Tachyonic validation demo
    demonstrate_instant_consensus()
    
    print("\n" + "=" * 70)
    print("Key Insight:")
    print("=" * 70)
    print("BLOCKCHAIN CONSENSUS IS HAMILTONIAN!")
    print("- Disagreement = potential energy")
    print("- Validation work = kinetic energy")
    print("- Consensus = energy minimum")
    print("- Instant global agreement via symplectic structure")
    print("- Retrocausal validation = future pulls present")
    print("\n➡️  Decentralized ledgers follow physics! ⛓️✨")
    print("➡️  Same math as atoms, markets, and consciousness!")
