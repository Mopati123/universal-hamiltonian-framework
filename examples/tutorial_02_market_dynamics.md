# Tutorial 2: Market Dynamics as Hamiltonian Systems

This tutorial demonstrates how financial markets can be modeled using Hamiltonian mechanics with **Polars** lazy evaluation.

## Setup

```python
import numpy as np
import polars as pl
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, '../src')

from domains.market_dynamics import (
    MarketHamiltonian,
    MarketState,
    PolarsMarketSimulator
)

plt.style.use('dark_background')
```

---

## The Market Phase Space

Financial markets have a natural phase-space structure:

- **q (Position)**: Price
- **p (Momentum)**: Order flow / Volume-weighted momentum

The Hamiltonian:

```
H = p²/(2λ) + ½κ(q - q_eq)²
```

where:
- λ = "liquidity mass" (resistance to price movement)
- κ = mean-reversion strength
- q_eq = equilibrium price

---

## Example 1: Simple Mean-Reverting Market

```python
# Create market Hamiltonian
H_market = MarketHamiltonian(
    liquidity_mass=1.0,
    volatility=0.5,  # Market "temperature"
    mean_reversion_strength=0.3,
    equilibrium_price=100.0
)

# Initial state: price displaced from equilibrium
initial_state = MarketState(price=105.0, momentum=0.0)

# Evolve the market
n_ticks = 500
states = [initial_state]

for t in range(n_ticks):
    current = states[-1]
    next_state = H_market.evolve_tick(current, dt=1.0)
    states.append(next_state)

# Extract data
prices = [s.price for s in states]
momenta = [s.momentum for s in states]
times = list(range(len(states)))

# Plot
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Price evolution
axes[0, 0].plot(times, prices, color='#00d4ff', linewidth=2)
axes[0, 0].axhline(H_market.p_eq, color='white', linestyle='--', alpha=0.5, label='Equilibrium')
axes[0, 0].set_xlabel('Time (ticks)')
axes[0, 0].set_ylabel('Price')
axes[0, 0].set_title('Mean Reversion Dynamics')
axes[0, 0].legend()
axes[0, 0].grid(alpha=0.3)

# Momentum
axes[0, 1].plot(times, momenta, color='#ff6b6b', linewidth=2)
axes[0, 1].set_xlabel('Time (ticks)')
axes[0, 1].set_ylabel('Momentum')
axes[0, 1].set_title('Order Flow Momentum')
axes[0, 1].grid(alpha=0.3)

# Phase portrait
axes[1, 0].plot(prices, momenta, color='#4ecdc4', linewidth=2, alpha=0.7)
axes[1, 0].scatter(prices[0], momenta[0], color='#00ff00', s=100, label='Start', zorder=5)
axes[1, 0].scatter(prices[-1], momenta[-1], color='#ff0000', s=100, label='End', zorder=5)
axes[1, 0].set_xlabel('Price (q)')
axes[1, 0].set_ylabel('Momentum (p)')
axes[1, 0].set_title('Market Phase Portrait')
axes[1, 0].legend()
axes[1, 0].grid(alpha=0.3)

# Energy landscape
energies = [H_market.hamiltonian(s.price, s.momentum) for s in states]
axes[1, 1].plot(times, energies, color='#ffd93d', linewidth=2)
axes[1, 1].set_xlabel('Time (ticks)')
axes[1, 1].set_ylabel('Market Energy H(q, p)')
axes[1, 1].set_title('Energy Dissipation (due to volatility noise)')
axes[1, 1].grid(alpha=0.3)

plt.tight_layout()
plt.savefig('market_dynamics.png', dpi=150, bbox_inches='tight')
plt.show()

print(f"Initial price: ${prices[0]:.2f}")
print(f"Final price: ${prices[-1]:.2f}")
print(f"Equilibrium: ${H_market.p_eq:.2f}")
```

**Key Observation**: Price oscillates around equilibrium just like a physical pendulum!

---

## Example 2: Using Polars for Large-Scale Simulation

```python
# Create simulator with Polars lazy evaluation
sim = PolarsMarketSimulator(H_market)

# Large-scale simulation (thousands of ticks)
initial_state = MarketState(price=100.0, momentum=2.0)

# This creates a LazyFrame - computation is DEFERRED (quantum-like!)
lf = sim.simulate_lazy(
    initial_state,
    n_ticks=10000,
    dt=1.0,
    order_flow_func=lambda t: 0.1 * np.sin(t / 100)  # Periodic order flow
)

# Add technical indicators (still lazy!)
lf = sim.add_derived_metrics(lf)

# Now "measure" by collecting (wavefunction collapse!)
df = lf.collect()

print(df.head())
```

Output:
```
 tick │ price   │ momentum │ energy   │ returns  │ sma_20   │ volatility_20 
──────┼─────────┼──────────┼──────────┼──────────┼──────────┼───────────────
  0   │ 100.0   │ 2.0      │ 2.0      │ null     │ null     │ null
  1   │ 101.99  │ 1.89     │ 1.95     │ 0.0199   │ null     │ null
 ...
```

**Quantum parallel**: Polars lazy evaluation = deferred measurement!

---

## Example 3: Order Book as Potential Energy

The order book creates a "force field" in price space:

```python
# Create mock order book
bids = pl.DataFrame({
    'price': np.arange(95, 100, 0.1),
    'volume': np.random.exponential(10, 50)
})

asks = pl.DataFrame({
    'price': np.arange(100, 105, 0.1),
    'volume': np.random.exponential(10, 50)
})

# Order book creates potential
from domains.market_dynamics import create_order_book_potential

V_orderbook = create_order_book_potential(bids, asks)

# Visualize potential landscape
price_range = np.linspace(95, 105, 200)
potential = [V_orderbook(p) for p in price_range]

plt.figure(figsize=(10, 6))
plt.plot(price_range, potential, color='#00d4ff', linewidth=2)
plt.axvline(100, color='white', linestyle='--', alpha=0.5, label='Mid-price')
plt.xlabel('Price')
plt.ylabel('Potential Energy V(q)')
plt.title('Order Book Potential Landscape')
plt.legend()
plt.grid(alpha=0.3)
plt.savefig('orderbook_potential.png', dpi=150, bbox_inches='tight')
plt.show()
```

**Key Insight**: Bid/ask imbalance creates forces that move price!

---

## Real-World Application: Black-Scholes

The Black-Scholes PDE can be recast as Hamiltonian:

```python
from domains.market_dynamics import BlackScholesHamiltonian

bs_H = BlackScholesHamiltonian(r=0.05, sigma=0.2)

# Option price evolution follows Hamiltonian flow!
# (Details in advanced tutorial)
```

---

## Exercise: Market-Making Strategy

Use the Hamiltonian framework to design a market-making strategy:

1. Find equilibrium price (∂H/∂q = 0)
2. Provide liquidity when |q - q_eq| is large (earn mean-reversion)
3. Withdraw when momentum |p| is too high (volatility protection)

```python
# Your strategy here!
def market_making_strategy(market_state: MarketState, H: MarketHamiltonian):
    """
    Returns: (bid_size, ask_size)
    """
    deviation = abs(market_state.price - H.p_eq)
    momentum_risk = abs(market_state.momentum)
    
    # Provide liquidity when far from equilibrium
    size = max(0, deviation * 10 - momentum_risk)
    
    return (size, size)
```

---

## Next: Tutorial 3 - Blockchain Consensus with Retrocausal Dynamics

See how future blockchain states influence present validation using tachyonic Hamiltonians!

---

**Philosophy**: Markets aren't just "like" physical systems - they **ARE** Hamiltonian systems with literal phase-space dynamics!
