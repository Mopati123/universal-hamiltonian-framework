"""
Market Dynamics - Hamiltonian Formulation

Financial markets as phase-space systems with Polars lazy evaluation.

Phase space: (price, momentum/volume)
Hamiltonian: H = kinetic + potential(order_book) + noise
"""

import numpy as np
import polars as pl
from typing import Callable, Tuple
from dataclasses import dataclass

@dataclass
class MarketState:
    """Phase-space point for market: (price, momentum)"""
    price: float  # q - Position in price space
    momentum: float  # p - Related to volume/order flow
    
    def to_array(self) -> np.ndarray:
        return np.array([self.price, self.momentum])


class MarketHamiltonian:
    """
    Market dynamics as Hamiltonian system.
    
    H = p²/(2λ) + V(q) + noise
    
    where:
    - q = price
    - p = momentum (related to volume)
    - λ = "liquidity mass"
    - V(q) = order book potential
    """
    
    def __init__(
        self,
        liquidity_mass: float = 1.0,
        volatility: float = 0.1,
        mean_reversion_strength: float = 0.5,
        damping: float = 0.05,
        equilibrium_price: float = 100.0
    ):
        self.lambda_liq = liquidity_mass
        self.sigma = volatility  # Market temperature
        self.kappa = mean_reversion_strength
        self.damping = damping
        self.p_eq = equilibrium_price
    
    def kinetic_energy(self, momentum: float) -> float:
        """T = p²/(2λ) - momentum component"""
        return momentum**2 / (2 * self.lambda_liq)
    
    def potential_energy(self, price: float) -> float:
        """
        V(q) = ½κ(q - q_eq)²
        
        Mean-reversion potential: market tends toward equilibrium.
        """
        return 0.5 * self.kappa * (price - self.p_eq)**2
    
    def hamiltonian(self, price: float, momentum: float) -> float:
        """Total energy: H = T + V"""
        return self.kinetic_energy(momentum) + self.potential_energy(price)
    
    def force(self, price: float) -> float:
        """F = -∂V/∂q = -κ(q - q_eq)"""
        return -self.kappa * (price - self.p_eq)
    
    def evolve_tick(
        self,
        state: MarketState,
        dt: float = 1.0,
        external_flow: float = 0.0
    ) -> MarketState:
        """
        Evolve one time tick with Langevin dynamics.
        
        Includes:
        - Hamiltonian evolution
        - Thermal noise (volatility)
        - External order flow
        """
        q, p = state.price, state.momentum
        
        # Symplectic step
        F = self.force(q)
        p_half = p + 0.5 * dt * F + external_flow
        # Add thermal noise (volatility) to half-step momentum so price can move immediately
        noise = np.random.normal(0, self.sigma * np.sqrt(dt))
        p_half_noisy = p_half + noise
        q_new = q + dt * p_half_noisy / self.lambda_liq
        F_new = self.force(q_new)
        p_new = p_half_noisy + 0.5 * dt * F_new
        
        # Damping (mean reversion) term: reduce momentum over time
        # gamma = self.kappa (mean_reversion_strength) used as damping coeff
        if hasattr(self, 'damping'):
            gamma = self.damping
        else:
            gamma = 0.0
        # Attenuate momentum
        p_new = p_new * (1.0 - gamma * dt)

        # Note: noise already applied to p_half_noisy (affects q_new). p_new may be further modified by damping above.

        return MarketState(price=q_new, momentum=p_new)


class PolarsMarketSimulator:
    """
    Market simulation with Polars lazy evaluation.
    
    Lazy evaluation mirrors quantum deferred measurement:
    - Define computation graph
    - Collect only when observed
    """
    
    def __init__(self, hamiltonian: MarketHamiltonian):
        self.H = hamiltonian
        self.tick_data = []
    
    def simulate_lazy(
        self,
        initial_state: MarketState,
        n_ticks: int,
        dt: float = 1.0,
        order_flow_func: Callable[[int], float] = lambda t: 0.0
    ) -> pl.LazyFrame:
        """
        Simulate market with lazy evaluation.
        
        Returns LazyFrame - computation deferred until .collect()
        """
        states = [initial_state]
        
        for t in range(n_ticks):
            external_flow = order_flow_func(t)
            next_state = self.H.evolve_tick(states[-1], dt, external_flow)
            states.append(next_state)
        
        # Create DataFrame (lazy)
        df = pl.DataFrame({
            'tick': range(len(states)),
            'price': [s.price for s in states],
            'momentum': [s.momentum for s in states],
            'energy': [self.H.hamiltonian(s.price, s.momentum) for s in states],
        })
        
        return df.lazy()
    
    def add_derived_metrics(self, lf: pl.LazyFrame) -> pl.LazyFrame:
        """
        Add technical indicators using lazy operations.
        
        Demonstrates Polars query optimization.
        """
        return lf.with_columns([
            # Returns
            pl.col('price').pct_change().alias('returns'),
            
            # Moving averages (lazy - only computed if needed)
            pl.col('price').rolling_mean(window_size=20).alias('sma_20'),
            pl.col('price').rolling_mean(window_size=50).alias('sma_50'),
            
            # Volatility (rolling std)
            pl.col('returns').rolling_std(window_size=20).alias('volatility_20'),
            
            # Energy conservation check
            (pl.col('energy') - pl.col('energy').first()).alias('energy_drift'),
        ])


def create_order_book_potential(bids: pl.DataFrame, asks: pl.DataFrame) -> Callable:
    """
    Create potential energy from order book depth.
    
    V(q) reflects supply/demand imbalance.
    """
    def potential(price: float) -> float:
        # Count bids above and asks below
        bid_pressure = len(bids.filter(pl.col('price') >= price))
        ask_pressure = len(asks.filter(pl.col('price') <= price))
        
        # Imbalance creates force
        imbalance = (bid_pressure - ask_pressure) / (bid_pressure + ask_pressure + 1)
        
        return -imbalance * price  # Pressure pushes price
    
    return potential


# Example: Black-Scholes as Hamiltonian system
class BlackScholesHamiltonian:
    """
    Black-Scholes PDE as Hamiltonian field theory.
    
    ∂V/∂t + ½σ²S²∂²V/∂S² + rS∂V/∂S - rV = 0
    
    Can be cast as Hamiltonian evolution in (S, Π) space.
    """
    
    def __init__(self, r: float, sigma: float):
        self.r = r  # Risk-free rate
        self.sigma = sigma  # Volatility
    
    def hamiltonian(self, S: float, Pi: float) -> float:
        """
        H = -rS·∂/∂S + ½σ²S²·∂²/∂S²
        
        (Simplified representation)
        """
        # Drift term
        drift = -self.r * S * Pi
        
        # Diffusion term (simplified)
        diffusion = 0.5 * self.sigma**2 * S**2 * Pi**2
        
        return drift + diffusion
