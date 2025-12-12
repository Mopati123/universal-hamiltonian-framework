"""
Cross-Domain Coupling Engine

Enables coupling between different domain Hamiltonians:
- Quantum + Market (price dynamics affect quantum decoherence)
- Consciousness + Blockchain (attention influences consensus)
- Market + Consciousness (trader psychology as neural field)

This demonstrates the true power of the Universal Hamiltonian Framework:
systems from different domains are literally coupled, not metaphorically.
"""

import numpy as np
from typing import List, Tuple, Callable
from dataclasses import dataclass

from core import PhaseSpace


@dataclass
class CoupledSystem:
    """
    Multiple Hamiltonians coupled together.
    
    H_total = Σᵢ Hᵢ + Σᵢⱼ V_coupling(i, j)
    """
    subsystems: List
    coupling_strengths: np.ndarray  # Matrix of coupling constants
    coupling_functions: List[List[Callable]]  # i,j coupling functions
    
    def total_hamiltonian(self, states: List[PhaseSpace]) -> float:
        """
        Compute total energy of coupled system.
        
        Args:
            states: List of phase-space states, one per subsystem
        
        Returns:
            Total Hamiltonian energy
        """
        # Individual system energies
        H_total = 0.0
        for i, (system, state) in enumerate(zip(self.subsystems, states)):
            if hasattr(system, 'hamiltonian'):
                H_total += system.hamiltonian(state.q, state.p)
        
        # Coupling terms
        n = len(self.subsystems)
        for i in range(n):
            for j in range(i+1, n):
                if self.coupling_strengths[i, j] != 0:
                    coupling_func = self.coupling_functions[i][j]
                    if coupling_func:
                        H_coupling = coupling_func(states[i], states[j])
                        H_total += self.coupling_strengths[i, j] * H_coupling
        
        return H_total
    
    def evolution_step(
        self,
        states: List[PhaseSpace],
        dt: float
    ) -> List[PhaseSpace]:
        """
        Evolve coupled system by one timestep.
        
        Each system experiences:
        1. Its own internal forces
        2. Coupling forces from other systems
        """
        n = len(self.subsystems)
        new_states = []
        
        for i, (system, state) in enumerate(zip(self.subsystems, states)):
            # Internal evolution
            if hasattr(system, '_verlet_step'):
                new_state = system._verlet_step(state, dt)
            else:
                # Fallback: simple Euler step
                new_state = state.copy()
            
            # Add coupling forces
            for j in range(n):
                if j != i and self.coupling_strengths[i, j] != 0:
                    coupling_force = self._compute_coupling_force(
                        i, j, states[i], states[j]
                    )
                    # Add to momentum
                    new_state.p += dt * coupling_force
            
            new_states.append(new_state)
        
        return new_states
    
    def _compute_coupling_force(
        self,
        i: int,
        j: int,
        state_i: PhaseSpace,
        state_j: PhaseSpace
    ) -> np.ndarray:
        """
        Compute force on system i due to coupling with system j.
        
        F_coupling = -∂V_coupling/∂qᵢ
        """
        epsilon = 1e-7
        force = np.zeros_like(state_i.q)
        
        coupling_func = self.coupling_functions[i][j]
        if not coupling_func:
            return force
        
        # Numerical gradient
        for k in range(len(state_i.q)):
            state_i.q[k] += epsilon
            V_plus = coupling_func(state_i, state_j)
            state_i.q[k] -= 2*epsilon
            V_minus = coupling_func(state_i, state_j)
            state_i.q[k] += epsilon  # Restore
            
            force[k] = -(V_plus - V_minus) / (2*epsilon)
        
        return self.coupling_strengths[i, j] * force


# ============================================================================
# Example: Quantum-Market Coupling
# ============================================================================

def quantum_market_coupling_example():
    """
    Couple quantum oscillator with market price.
    
    Interpretation:
    - Quantum uncertainty affects market volatility
    - Market momentum influences quantum decoherence rate
    
    This is NOT metaphor - we're literally coupling the phase spaces!
    """
    from compiler import define_system
    from domains.market_dynamics import MarketHamiltonian, MarketState
    
    # Quantum subsystem
    @define_system
    class QuantumOsc:
        coordinates = ['x']
        
        def kinetic(self, p):
            return p.px**2 / 2
        
        def potential(self, q):
            return 0.5 * q.x**2
    
    quantum_system = QuantumOsc()
    
    # Market subsystem
    market_system = MarketHamiltonian(liquidity_mass=1.0, volatility=0.1)
    
    # Coupling function: market volatility increases with quantum uncertainty
    def quantum_to_market_coupling(quantum_state: PhaseSpace, market_state: PhaseSpace):
        """
        Market momentum influenced by quantum position uncertainty.
        
        Economic interpretation: quantum fluctuations = fundamental uncertainty
        """
        quantum_uncertainty = abs(quantum_state.q[0])  # Simplified
        return quantum_uncertainty * market_state.p[0]
    
    def market_to_quantum_coupling(market_state: PhaseSpace, quantum_state: PhaseSpace):
        """
        Quantum decoherence influenced by market activity.
        
        Physical interpretation: market "measures" quantum system
        """
        market_volatility = abs(market_state.p[0])  # Momentum = activity
        return market_volatility * quantum_state.q[0]**2
    
    # Create coupled system
    n_systems = 2
    coupling_matrix = np.array([
        [0.0, 0.1],  # quantum -> market coupling
        [0.05, 0.0]  # market -> quantum coupling
    ])
    
    coupling_funcs = [
        [None, quantum_to_market_coupling],
        [market_to_quantum_coupling, None]
    ]
    
    coupled = CoupledSystem(
        subsystems=[quantum_system, market_system],
        coupling_strengths=coupling_matrix,
        coupling_functions=coupling_funcs
    )
    
    # Initial states
    quantum_initial = PhaseSpace(q=np.array([1.0]), p=np.array([0.0]))
    market_initial = PhaseSpace(q=np.array([100.0]), p=np.array([5.0]))
    
    states = [quantum_initial, market_initial]
    
    # Evolve
    trajectory = []
    dt = 0.01
    n_steps = 1000
    
    for step in range(n_steps):
        trajectory.append(states)
        states = coupled.evolution_step(states, dt)
    
    return coupled, trajectory


# ============================================================================
# Example: Consciousness-Blockchain Coupling
# ============================================================================

def consciousness_blockchain_coupling():
    """
    Couple neural attention field with blockchain consensus.
    
    Interpretation:
    - Collective attention drives consensus formation
    - Blockchain state influences neural field dynamics
    
    This models: "wisdom of crowds" as literal phase-space coupling!
    """
    # TODO: Implement when Mojo consciousness module is available
    pass


# ============================================================================
# Meta-Hamiltonian: Self-Referential System
# ============================================================================

class MetaHamiltonian:
    """
    A Hamiltonian whose evolution depends on its own structure.
    
    H_meta(t) = H[H](t)
    
    This creates self-reference: system observing itself evolve.
    Gödelian strange loop in phase space!
    """
    
    def __init__(self, base_hamiltonian_func: Callable):
        """
        Args:
            base_hamiltonian_func: Function that takes H and returns new H
        """
        self.base_func = base_hamiltonian_func
        self.history = []  # Store past Hamiltonians
    
    def evolve_meta(self, initial_H: float, n_steps: int, dt: float):
        """
        Evolve the Hamiltonian itself.
        
        At each step:
        1. Current H evolves state
        2. State evolution changes H
        3. New H used for next step
        
        This is consciousness observing itself!
        """
        H_current = initial_H
        self.history = [H_current]
        
        for step in range(n_steps):
            # Hamiltonian evolves based on its own value
            H_next = self.base_func(H_current)
            
            self.history.append(H_next)
            H_current = H_next
        
        return np.array(self.history)
    
    def compute_self_complexity(self) -> float:
        """
        Measure how much H depends on its own history.
        
        High complexity = strong self-reference
        """
        if len(self.history) < 2:
            return 0.0
        
        # Compute autocorrelation
        H_array = np.array(self.history)
        autocorr = np.corrcoef(H_array[:-1], H_array[1:])[0, 1]
        
        return abs(autocorr)


# Example meta-Hamiltonian
def logistic_meta_hamiltonian(H_current: float, r: float = 3.5) -> float:
    """
    Logistic map as meta-Hamiltonian evolution.
    
    H_next = r * H_current * (1 - H_current)
    
    For r > 3.57, this becomes chaotic!
    """
    return r * H_current * (1 - H_current)


if __name__ == '__main__':
    # Example: Run quantum-market coupling
    print("Quantum-Market Coupling Demo")
    print("="*60)
    
    coupled, traj = quantum_market_coupling_example()
    
    print(f"Evolved {len(traj)} steps")
    print(f"Initial energy: {coupled.total_hamiltonian(traj[0]):.4f}")
    print(f"Final energy: {coupled.total_hamiltonian(traj[-1]):.4f}")
    
    # Example: Meta-Hamiltonian
    print("\nMeta-Hamiltonian Demo")
    print("="*60)
    
    meta = MetaHamiltonian(lambda H: logistic_meta_hamiltonian(H, r=3.8))
    history = meta.evolve_meta(initial_H=0.1, n_steps=100, dt=1.0)
    
    print(f"Self-complexity: {meta.compute_self_complexity():.4f}")
    print("(High value = strong self-reference, possible chaos)")
