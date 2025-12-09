"""
Quantum Decision Layer

Implements wavefunction over trading actions with:
- Superposition of regimes
- Variational quantum eigensolver (VQE)
- Measurement (collapse to action)

This is where quantum principles meet trading decisions.
"""

import numpy as np
from typing import List, Dict, Tuple
from scipy.optimize import minimize
from enum import Enum


class TradingAction(Enum):
    """Discrete trading actions"""
    LONG = "LONG"      # Buy/hold long position
    FLAT = "FLAT"      # No position
    SHORT = "SHORT"    # Sell/hold short position
    HEDGE = "HEDGE"    # Hedged (delta-neutral)


class QuantumDecisionLayer:
    """
    Quantum-inspired decision making via wavefunction.
    
    Key concepts:
    - |ψ⟩ = superposition of action states
    - Unitary evolution before measurement
    - VQE minimizes expected energy + costs
    - Measurement collapses to single action
    """
    
    def __init__(self, actions: List[TradingAction] = None):
        """
        Initialize quantum state over actions
        
        Args:
            actions: List of possible trading actions
        """
        self.actions = actions or list(TradingAction)
        self.n_actions = len(self.actions)
        
        # Wavefunction: complex amplitudes
        # Initialize to |FLAT⟩ (no position)
        self.psi = np.zeros(self.n_actions, dtype=complex)
        flat_idx = self.actions.index(TradingAction.FLAT)
        self.psi[flat_idx] = 1.0
        
        # History for analysis
        self.history = []
    
    def normalize(self):
        """Ensure ⟨ψ|ψ⟩ = 1"""
        norm = np.sqrt(np.sum(np.abs(self.psi)**2))
        if norm > 0:
            self.psi /= norm
    
    def probabilities(self) -> np.ndarray:
        """
        Calculate measurement probabilities
        
        P(action) = |⟨action|ψ⟩|² = |ψ_action|²
        """
        return np.abs(self.psi)**2
    
    def construct_unitary(self, angles: np.ndarray) -> np.ndarray:
        """
        Build parameterized unitary transformation
        
        U(θ) is built from rotation matrices, ensuring U†U = I
        
        Args:
            angles: Rotation angles for each qubit/action pair
        
        Returns:
            Unitary matrix (n_actions × n_actions)
        """
        n = self.n_actions
        U = np.eye(n, dtype=complex)
        
        # Apply sequence of 2x2 rotations
        idx = 0
        for i in range(n):
            for j in range(i+1, n):
                if idx < len(angles):
                    theta = angles[idx]
                    
                    # Rotation in (i,j) subspace
                    c, s = np.cos(theta), np.sin(theta)
                    R = np.eye(n, dtype=complex)
                    R[i,i] = c
                    R[i,j] = -s
                    R[j,i] = s
                    R[j,j] = c
                    
                    U = R @ U
                    idx += 1
        
        return U
    
    def variational_update(self, hamiltonian_engine, market_state, trading_costs: Dict):
        """
        VQE-like optimization: minimize ⟨ψ|H|ψ⟩ + costs
        
        This is the core quantum-inspired algorithm:
        1. Parameterize U(θ) as rotations
        2. Minimize expected energy over θ
        3. Apply optimal U to current state
        
        Args:
            hamiltonian_engine: Physics engine for energy calculation
            market_state: Current market state
            trading_costs: Cost per action (spread, commissions, impact)
        """
        
        def objective(angles):
            """Expected energy + trading costs"""
            # Build trial unitary
            U = self.construct_unitary(angles)
            
            # Apply to current wavefunction
            psi_trial = U @ self.psi
            
            # Calculate probabilities
            probs = np.abs(psi_trial)**2
            
            # Expected energy
            E_expected = 0.0
            for i, action in enumerate(self.actions):
                prob = probs[i]
                
                # Simulate taking this action
                # (In real system, this would update position and evolve)
                position_change = self._action_to_position_change(action)
                
                # Estimated energy after action
                # (Simplified: just use current state energy)
                E = hamiltonian_engine.total_energy(market_state)
                
                E_expected += prob * E
            
            # Add trading costs
            cost_expected = sum(
                probs[i] * trading_costs.get(action.value, 0.0)
                for i, action in enumerate(self.actions)
            )
            
            return E_expected + cost_expected
        
        # Number of parameters for U
        n_params = self.n_actions * (self.n_actions - 1) // 2
        
        # Initialize random angles
        init_angles = np.random.randn(n_params) * 0.1
        
        # Minimize
        result = minimize(
            objective,
            init_angles,
            method='BFGS',
            options={'maxiter': 100}
        )
        
        # Apply optimal unitary
        U_opt = self.construct_unitary(result.x)
        self.psi = U_opt @ self.psi
        self.normalize()
        
        # Record
        self.history.append({
            'timestamp': market_state.timestamp,
            'probabilities': self.probabilities().copy(),
            'energy': result.fun
        })
    
    def measure(self) -> TradingAction:
        """
        Measurement: collapse wavefunction to single action
        
        Sample according to Born rule: P(action) = |ψ_action|²
        
        This is where quantum superposition becomes classical reality.
        """
        probs = self.probabilities()
        
        # Sample action
        idx = np.random.choice(self.n_actions, p=probs)
        action = self.actions[idx]
        
        # After measurement, collapse to measured state
        self.psi = np.zeros(self.n_actions, dtype=complex)
        self.psi[idx] = 1.0
        
        return action
    
    def expected_action(self) -> TradingAction:
        """
        Get most probable action WITHOUT measurement
        
        Useful for analysis/display without collapsing state.
        """
        probs = self.probabilities()
        idx = np.argmax(probs)
        return self.actions[idx]
    
    def _action_to_position_change(self, action: TradingAction) -> float:
        """Map action to position change"""
        mapping = {
            TradingAction.LONG: 1.0,
            TradingAction.FLAT: 0.0,
            TradingAction.SHORT: -1.0,
            TradingAction.HEDGE: 0.5  # Partial position
        }
        return mapping.get(action, 0.0)
    
    def entanglement_measure(self) -> float:
        """
        Measure entanglement in state
        
        For single-asset, this is just purity: Tr(ρ²)
        Pure state (no entanglement): purity = 1
        Mixed state: purity < 1
        """
        # Density matrix ρ = |ψ⟩⟨ψ|
        rho = np.outer(self.psi, self.psi.conj())
        
        # Purity = Tr(ρ²)
        purity = np.trace(rho @ rho).real
        
        return purity


# Example usage and validation
if __name__ == "__main__":
    print("="*70)
    print("Quantum Decision Layer - Validation Test")
    print("="*70)
    
    # Create quantum layer
    quantum = QuantumDecisionLayer()
    
    print(f"\nInitial State:")
    print(f"  Actions: {[a.value for a in quantum.actions]}")
    print(f"  Wavefunction: {quantum.psi}")
    print(f"  Probabilities: {quantum.probabilities()}")
    
    # Create superposition
    print(f"\nCreating superposition...")
    quantum.psi = np.array([0.5, 0.5, 0.5, 0.5], dtype=complex)
    quantum.normalize()
    
    probs = quantum.probabilities()
    print(f"  Equal superposition: {probs}")
    print(f"  Sum of probabilities: {probs.sum():.6f} (should be 1.0)")
    
    # Test unitarity
    print(f"\nTesting unitary transformations...")
    angles = np.random.randn(6) * 0.5  # 4 actions → 6 angles
    U = quantum.construct_unitary(angles)
    
    # Check U†U = I
    identity_check = U.conj().T @ U
    is_unitary = np.allclose(identity_check, np.eye(4))
    print(f"  U†U = I: {is_unitary} {'✓' if is_unitary else '✗'}")
    
    # Apply unitary
    psi_original = quantum.psi.copy()
    quantum.psi = U @ quantum.psi
    quantum.normalize()
    
    # Check norm preserved
    norm_before = np.sum(np.abs(psi_original)**2)
    norm_after = np.sum(np.abs(quantum.psi)**2)
    print(f"  Norm before: {norm_before:.6f}")
    print(f"  Norm after: {norm_after:.6f}")
    print(f"  Preserved: {np.allclose(norm_before, norm_after)} {'✓' if np.allclose(norm_before, norm_after) else '✗'}")
    
    # Measure purity
    purity = quantum.entanglement_measure()
    print(f"\nPurity: {purity:.6f} (1.0 = pure state)")
    
    # Perform measurements
    print(f"\nPerforming 1000 measurements...")
    measurements = [quantum.measure().value for _ in range(1000)]
    
    # Create fresh state for measurement test
    quantum.psi = np.array([0.6, 0.3, 0.1, 0.0], dtype=complex)
    quantum.normalize()
    
    print(f"  Theoretical probabilities:")
    for action, prob in zip(quantum.actions, quantum.probabilities()):
        print(f"    {action.value}: {prob:.3f}")
    
    # New measurements with defined probabilities
    measurements = []
    for _ in range(1000):
        # Reset to same state each time for statistical test
        quantum.psi = np.array([0.6, 0.3, 0.1, 0.0], dtype=complex)
        quantum.normalize()
        measurements.append(quantum.measure().value)
    
    print(f"  Empirical frequencies:")
    for action in quantum.actions:
        count = measurements.count(action.value)
        freq = count / 1000
        print(f"    {action.value}: {freq:.3f}")
    
    print(f"\n✅ Quantum Decision Layer validation complete!")
    print("="*70)
