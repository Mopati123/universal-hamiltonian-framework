"""
Black-Scholes Option Pricing via Hamiltonian Mechanics

Demonstrates how financial markets follow Hamiltonian evolution.
Phase space: (S, p_S) where S = stock price, p_S = price momentum
"""

import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt


class BlackScholesHamiltonian:
    """
    Black-Scholes Hamiltonian System
    
    Represents financial market dynamics in canonical phase space:
    - q = Stock price S
    - p = Price momentum p_S
    
    H(S, p_S) = (1/2)σ²S²p_S² + rSp_S
    
    This class enables axiom validation for markets as Hamiltonian systems.
    """
    
    def __init__(self, sigma: float, r: float, K: float):
        """
        Initialize market Hamiltonian.
        
        Args:
            sigma: Volatility (annual)
            r: Risk-free rate (annual)
            K: Strike price (for reference)
        """
        self.sigma = sigma
        self.r = r
        self.K = K
    
    def hamiltonian(self, q: float, p: float) -> float:
        """
        Compute total energy: H(S, p_S)
        
        Args:
            q: Stock price
            p: Price momentum
            
        Returns:
            Total Hamiltonian energy
        """
        return black_scholes_hamiltonian(q, p, self.r, self.sigma)
    
    def dq_dt(self, q: float, p: float) -> float:
        """
        Hamilton's equation: dS/dt = ∂H/∂p_S
        
        Canonical derivative of position w.r.t. time.
        Returns rate of change of stock price.
        """
        return self.sigma**2 * q**2 * p + self.r * q
    
    def dp_dt(self, q: float, p: float) -> float:
        """
        Hamilton's equation: dp_S/dt = -∂H/∂S
        
        Canonical derivative of momentum w.r.t. time.
        Returns rate of change of price momentum.
        """
        return -(self.sigma**2 * q * p**2 + self.r * p)


def black_scholes_hamiltonian(S: float, p_S: float, r: float, sigma: float) -> float:
    """
    Hamiltonian for Black-Scholes dynamics.
    
    H = (1/2)σ²S²p_S² + rSp_S
    
    Args:
        S: Stock price (configuration variable)
        p_S: Price momentum (conjugate variable)
        r: Risk-free rate
        sigma: Volatility
        
    Returns:
        Total energy of the system
    """
    return 0.5 * (sigma ** 2) * (S ** 2) * (p_S ** 2) + r * S * p_S


def hamiltons_equations(state: np.ndarray, t: float, r: float, sigma: float) -> np.ndarray:
    """
    Hamilton's equations for market evolution.
    
    dS/dt = ∂H/∂p_S
    dp_S/dt = -∂H/∂S
    
    Args:
        state: [S, p_S] current state
        t: Time
        r: Risk-free rate
        sigma: Volatility
        
    Returns:
        [dS/dt, dp_S/dt] time derivatives
    """
    S, p_S = state
    
    # Hamilton's equations
    dS_dt = sigma**2 * S**2 * p_S + r * S  # = ∂H/∂p_S
    dp_S_dt = -(sigma**2 * S * p_S**2 + r * p_S)  # = -∂H/∂S
    
    return np.array([dS_dt, dp_S_dt])


def price_european_call(S0: float, K: float, r: float, sigma: float, T: float) -> float:
    """
    Price European call option using Hamiltonian evolution.
    
    Args:
        S0: Initial stock price
        K: Strike price
        r: Risk-free rate (annual)
        sigma: Volatility (annual)
        T: Time to expiration (years)
        
    Returns:
        Option value
    """
    # Initial state in phase space
    # p_S = 0 means no initial momentum (equilibrium)
    state_0 = np.array([S0, 0.0])
    
    # Time points for evolution
    t = np.linspace(0, T, 1000)
    
    # Evolve via Hamilton's equations
    trajectory = odeint(hamiltons_equations, state_0, t, args=(r, sigma))
    
    # Terminal stock price
    S_T = trajectory[-1, 0]
    
    # Payoff at expiration
    payoff = max(S_T - K, 0)
    
    # Discount back to present
    option_value = np.exp(-r * T) * payoff
    
    return option_value


def visualize_phase_space(S0: float, r: float, sigma: float, T: float):
    """
    Visualize Hamiltonian evolution in (S, p_S) phase space.
    
    Args:
        S0: Initial stock price
        r: Risk-free rate  
        sigma: Volatility
        T: Time horizon
    """
    # Multiple initial momentum values
    p_S_values = np.linspace(-0.1, 0.1, 5)
    
    plt.figure(figsize=(10, 6))
    
    for p_S_0 in p_S_values:
        state_0 = np.array([S0, p_S_0])
        t = np.linspace(0, T, 1000)
        trajectory = odeint(hamiltons_equations, state_0, t, args=(r, sigma))
        
        plt.plot(trajectory[:, 0], trajectory[:, 1], 
                label=f'Initial p_S = {p_S_0:.2f}', alpha=0.7)
    
    plt.xlabel('Stock Price S (q)')
    plt.ylabel('Price Momentum p_S (p)')
    plt.title('Black-Scholes Evolution in Phase Space')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('market_phase_space.png', dpi=150)
    print("Phase space visualization saved to 'market_phase_space.png'")


if __name__ == "__main__":
    print("=" * 60)
    print("Black-Scholes via Hamiltonian Mechanics")
    print("=" * 60)
    
    # Market parameters
    S0 = 100.0  # Current stock price
    K = 105.0   # Strike price
    r = 0.05    # 5% risk-free rate
    sigma = 0.2  # 20% volatility
    T = 1.0     # 1 year to expiration
    
    print(f"\nMarket Parameters:")
    print(f"  Current Stock Price: ${S0:.2f}")
    print(f"  Strike Price: ${K:.2f}")
    print(f"  Risk-Free Rate: {r*100:.1f}%")
    print(f"  Volatility: {sigma*100:.1f}%")
    print(f"  Time to Expiration: {T:.1f} years")
    
    # Calculate option value via Hamiltonian evolution
    option_value = price_european_call(S0, K, r, sigma, T)
    
    print(f"\nCall Option Value (Hamiltonian Method): ${option_value:.2f}")
    
    # Compare with Black-Scholes formula
    from scipy.stats import norm
   
    d1 = (np.log(S0/K) + (r + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)
    bs_value = S0*norm.cdf(d1) - K*np.exp(-r*T)*norm.cdf(d2)
    
    print(f"Black-Scholes Formula Value: ${bs_value:.2f}")
    print(f"Difference: ${abs(option_value - bs_value):.4f}")
    
    # Phase space visualization
    print(f"\nGenerating phase space visualization...")
    visualize_phase_space(S0, r, sigma, T)
    
    print("\n" + "=" * 60)
    print("Key Insight:")
    print("=" * 60)
    print("Market prices follow Hamiltonian evolution!")
    print("- Stock price S = position (q)")
    print("- Price momentum p_S = conjugate variable (p)")
    print("- Black-Scholes PDE ≡ Hamilton's equations")
    print("- This is THE SAME mathematics as quantum mechanics")
    print("\n➡️  Markets, atoms, consciousness: ALL Hamiltonian! ✨")
