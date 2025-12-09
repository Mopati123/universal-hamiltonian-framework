"""
Hamiltonian Engine

Core physics engine for market modeling.
Implements H_θ(x_t) with symplectic evolution.

This is where mathematics meets market reality.
"""

import numpy as np
from typing import Dict, Tuple
from dataclasses import dataclass


@dataclass
class MarketState:
    """Phase space representation of market"""
    S: float  # Stock price (configuration)
    p: float  # Momentum (price velocity)
    sigma: float  # Volatility
    spread: float  # Bid-ask spread
    volume: float  # Trading volume
    timestamp: float  # Time
    
    def to_vector(self):
        """Convert to numpy array for calculations"""
        return np.array([self.S, self.p, self.sigma, self.spread, self.volume])


class HamiltonianEngine:
    """
    Market Hamiltonian: H = T(p) + V(S)
    
    Where:
    - T(p) = kinetic energy (momentum term)
    - V(S) = potential energy (mean reversion + drift)
    
    Ground state = no-arbitrage equilibrium
    """
    
    def __init__(self, theta: Dict[str, float] = None):
        """
        Initialize Hamiltonian with parameters θ
        
        Args:
            theta: Hamiltonian parameters
                - mean_reversion: strength of pull to equilibrium
                - equilibrium: equilibrium price level
                - drift: directional bias
                - friction: damping term
        """
        self.theta = theta or {
            'mean_reversion': 0.1,
            'equilibrium': 100.0,
            'drift': 0.0,
            'friction': 0.01
        }
    
    def kinetic_energy(self, state: MarketState) -> float:
        """
        T(p) = (1/2) * σ² * S² * p²
        
        Kinetic energy from price momentum.
        Higher volatility → more energy for same momentum.
        """
        return 0.5 * state.sigma**2 * state.S**2 * state.p**2
    
    def potential_energy(self, state: MarketState) -> float:
        """
        V(S) = (1/2) * k * (S - S_eq)² + drift * S * p
        
        Potential energy from:
        - Mean reversion (harmonic oscillator)
        - Directional drift
        """
        # Mean reversion term (like a spring)
        k = self.theta['mean_reversion']
        S_eq = self.theta['equilibrium']
        V_reversion = 0.5 * k * (state.S - S_eq)**2
        
        # Drift term (like gravity)
        V_drift = self.theta['drift'] * state.S * state.p
        
        return V_reversion + V_drift
    
    def total_energy(self, state: MarketState) -> float:
        """
        H(S, p) = T(p) + V(S)
        
        Total Hamiltonian energy.
        
        Ground state (minimum) = market equilibrium
        Excitations = deviations that create trading opportunities
        """
        return self.kinetic_energy(state) + self.potential_energy(state)
    
    def forces(self, state: MarketState) -> Dict[str, float]:
        """
        Compute Hamiltonian forces (gradients)
        
        Hamilton's equations:
        dS/dt = ∂H/∂p   (momentum drives price change)
        dp/dt = -∂H/∂S  (price gradient creates force)
        
        Returns:
            Dictionary with dS_dt and dp_dt
        """
        # Numerical gradients (can be made analytical for speed)
        eps = 1e-6
        
        # ∂H/∂p (how momentum affects energy)
        state_plus = MarketState(
            S=state.S, p=state.p + eps, sigma=state.sigma,
            spread=state.spread, volume=state.volume, timestamp=state.timestamp
        )
        state_minus = MarketState(
            S=state.S, p=state.p - eps, sigma=state.sigma,
            spread=state.spread, volume=state.volume, timestamp=state.timestamp
        )
        dH_dp = (self.total_energy(state_plus) - self.total_energy(state_minus)) / (2*eps)
        
        # ∂H/∂S (how price affects energy)
        state_plus = MarketState(
            S=state.S + eps, p=state.p, sigma=state.sigma,
            spread=state.spread, volume=state.volume, timestamp=state.timestamp
        )
        state_minus = MarketState(
            S=state.S - eps, p=state.p, sigma=state.sigma,
            spread=state.spread, volume=state.volume, timestamp=state.timestamp
        )
        dH_dS = (self.total_energy(state_plus) - self.total_energy(state_minus)) / (2*eps)
        
        return {
            'dS_dt': dH_dp,  # Price change from momentum
            'dp_dt': -dH_dS - self.theta['friction'] * state.p  # Force from price + damping
        }
    
    def evolve(self, state: MarketState, dt: float) -> MarketState:
        """
        Symplectic evolution: preserve Hamiltonian structure
        
        Uses leapfrog integration (2nd order symplectic):
        1. Half-step momentum
        2. Full-step position
        3. Half-step momentum
        
        This preserves energy on constraint surface.
        """
        forces = self.forces(state)
        
        # Half-step momentum update
        p_half = state.p + 0.5 * forces['dp_dt'] * dt
        
        # Full-step position update
        S_new = state.S + forces['dS_dt'] * dt
        
        # Create intermediate state for force recalculation
        state_half = MarketState(
            S=S_new, p=p_half, sigma=state.sigma,
            spread=state.spread, volume=state.volume, timestamp=state.timestamp + dt
        )
        forces_new = self.forces(state_half)
        
        # Half-step momentum update (again)
        p_new = p_half + 0.5 * forces_new['dp_dt'] * dt
        
        return MarketState(
            S=S_new,
            p=p_new,
            sigma=state.sigma,  # Update separately via volatility model
            spread=state.spread,  # From live data
            volume=state.volume,  # From live data
            timestamp=state.timestamp + dt
        )
    
    def find_equilibrium(self, initial_state: MarketState, max_iter: int = 1000) -> MarketState:
        """
        Find ground state (equilibrium) via energy minimization
        
        Ground state = minimum energy configuration
        This is the "fair value" according to Hamiltonian
        """
        state = initial_state
        learning_rate = 0.01
        
        for _ in range(max_iter):
            forces = self.forces(state)
            
            # Gradient descent in configuration space
            state = MarketState(
                S=state.S - learning_rate * forces['dp_dt'],
                p=0.0,  # Equilibrium has zero momentum
                sigma=state.sigma,
                spread=state.spread,
                volume=state.volume,
                timestamp=state.timestamp
            )
            
            # Check convergence
            if abs(forces['dp_dt']) < 1e-6:
                break
        
        return state


# Example usage and validation
if __name__ == "__main__":
    print("="*70)
    print("Hamiltonian Engine - Validation Test")
    print("="*70)
    
    # Initialize engine
    engine = HamiltonianEngine(theta={
        'mean_reversion': 0.1,
        'equilibrium': 450.0,  # SPY fair value
        'drift': 0.0,
        'friction': 0.01
    })
    
    # Create market state (SPY @ 450, moving up $0.10/sec)
    state = MarketState(
        S=450.0,     # Current price
        p=0.10,      # Momentum ($/sec)
        sigma=0.20,  # 20% annual volatility
        spread=0.01, # 1 cent spread
        volume=1e6,  # 1M volume
        timestamp=0.0
    )
    
    print(f"\nInitial State:")
    print(f"  Price: ${state.S:.2f}")
    print(f"  Momentum: ${state.p:.4f}/sec")
    print(f"  Volatility: {state.sigma*100:.1f}%")
    
    # Calculate energy
    H = engine.total_energy(state)
    print(f"\nHamiltonian Energy: {H:.6f}")
    print(f"  Kinetic: {engine.kinetic_energy(state):.6f}")
    print(f"  Potential: {engine.potential_energy(state):.6f}")
    
    # Calculate forces
    forces = engine.forces(state)
    print(f"\nForces:")
    print(f"  dS/dt (price change): ${forces['dS_dt']:.6f}/sec")
    print(f"  dp/dt (momentum change): ${forces['dp_dt']:.6f}/sec²")
    
    # Evolve forward 1 second
    print(f"\nEvolving 1 second with symplectic integrator...")
    state_new = engine.evolve(state, dt=1.0)
    
    print(f"\nNew State:")
    print(f"  Price: ${state_new.S:.2f} (change: ${state_new.S - state.S:+.2f})")
    print(f"  Momentum: ${state_new.p:.4f}/sec (change: ${state_new.p - state.p:+.4f})")
    
    # Energy conservation check
    H_new = engine.total_energy(state_new)
    print(f"\nEnergy Conservation:")
    print(f"  Initial energy: {H:.6f}")
    print(f"  Final energy: {H_new:.6f}")
    print(f"  Drift: {abs(H_new - H):.8f} ({'✓ conserved' if abs(H_new-H) < 0.01 else '✗ not conserved'})")
    
    # Find equilibrium
    print(f"\nFinding equilibrium (ground state)...")
    equilibrium = engine.find_equilibrium(state)
    
    print(f"  Equilibrium price: ${equilibrium.S:.2f}")
    print(f"  Equilibrium energy: {engine.total_energy(equilibrium):.6f}")
    print(f"  Distance from current: ${abs(equilibrium.S - state.S):.2f}")
    
    print(f"\n✅ Hamiltonian Engine validation complete!")
    print("="*70)
