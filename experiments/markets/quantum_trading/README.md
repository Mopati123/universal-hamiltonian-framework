# Quantum-Inspired Trading System

## 🎯 Quick Start - Run It Now!

This is the **practical application of the Universal Hamiltonian Framework** demonstrating how mathematics underpins trading.

### Install & Run in 3 Steps:

```bash
# 1. Clone the repository
git clone https://github.com/Mopati123/universal-hamiltonian-framework.git
cd universal-hamiltonian-framework

# 2. Install dependencies
pip install -r src/quantum_trading/requirements.txt

# 3. Run the demo!
python run_quantum_trading_demo.py
```

**That's it!** You'll see the quantum trading system in action.

---

## 📊 What Is This?

A production-ready trading system combining:

1. **Hamiltonian Engine** - Physics-based market modeling
2. **Quantum Decision Layer** - Superposition of trading actions  
3. **QUBO Optimizer** - Portfolio allocation via quantum-inspired annealing
4. **Risk-Aware Execution** - Safe order placement

**This is Chapter 9 of the Book of Mopati brought to life!**

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────┐
│           APPLICATION LAYER                      │
│   Trading strategies, Risk management            │
└──────────────────┬──────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────┐
│       QUANTUM DECISION LAYER                     │
│  • Wavefunction |ψ⟩ over actions                │
│  • VQE optimization                              │
│  • Measurement → discrete trades                 │
└──────────────────┬──────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────┐
│       HAMILTONIAN ENGINE                         │
│  • Phase space (S, p, σ)                        │
│  • Energy H(S,p)                                │
│  • Symplectic evolution                          │
└──────────────────┬──────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────┐
│       DATA INFRASTRUCTURE                        │
│  MT5, Deriv, Alpaca, TradingView, yfinance      │
│  (Phase 2 - Multi-source data)                   │
└─────────────────────────────────────────────────┘
```

---

## 🧪 Components

### 1. Hamiltonian Engine (`src/quantum_trading/hamiltonian/engine.py`)

```python
from src.quantum_trading.hamiltonian.engine import HamiltonianEngine

engine = HamiltonianEngine()
energy = engine.total_energy(market_state)
forces = engine.forces(market_state)
```

**Features:**
- Kinetic energy: `T = 0.5 * σ² * S² * p²`
- Potential energy: `V = k(S - S_eq)² + drift*S*p`
- Symplectic integration (preserves structure)
- Equilibrium finding (ground state = fair value)

### 2. Quantum Decision Layer (`src/quantum_trading/quantum/wavefunction.py`)

```python
from src.quantum_trading.quantum.wavefunction import QuantumDecisionLayer

quantum = QuantumDecisionLayer()
quantum.variational_update(engine, state, costs)  # VQE
action = quantum.measure()  # Collapse to LONG/FLAT/SHORT/HEDGE
```

**Features:**
- True quantum superposition
- Unitary evolution (`U†U = I`)
- VQE minimizes `⟨ψ|H|ψ⟩ + costs`
- Probabilistic measurement (`P = |ψ|²`)

### 3. QUBO Optimizer (`src/quantum_trading/optimization/qubo.py`)

```python
from src.quantum_trading.optimization.qubo import QUBOOptimizer

optimizer = QUBOOptimizer(universe=['SPY', 'QQQ', 'IWM'])
portfolio = optimizer.optimize(engine, market_states, constraints, capital)
```

**Features:**
- Hamiltonian → QUBO matrix conversion
- Simulated annealing (quantum analogue)
- Constraint handling
- Portfolio allocation

### 4. Trading System (`src/quantum_trading/execution/system.py`)

```python
from src.quantum_trading.execution.system import TradingSystem

system = TradingSystem(universe=['SPY'], capital=10000, mode='simulation')
system.run(iterations=10)
```

**Features:**
- Event-driven architecture
- Multi-source data integration
- Risk-aware execution
- Complete logging for validation

---

## 📚 Documentation

### Core Concepts

**Phase Space**: `(S, p)` where:
- `S` = stock price (configuration)
- `p` = momentum (price velocity)

**Hamiltonian**: `H(S, p) = T(p) + V(S)`
- Ground state = market equilibrium
- Excitations = trading opportunities

**Quantum Layer**: Wavefunction over actions:
```
|ψ⟩ = α|LONG⟩ + β|FLAT⟩ + γ|SHORT⟩ + δ|HEDGE⟩
```

**QUBO**: Minimize `x^T Q x` where `x ∈ {0,1}^n`
- Maps Hamiltonian to combinatorial optimization
- Solved via quantum-inspired annealing

### Mathematical Foundation

See **docs/book-of-mopati-chapter9-empirical-validation.md** for complete mathematical derivation showing how:
1. Markets follow Hamiltonian structure
2. Quantum principles apply to decision-making
3. QUBO maps to portfolio optimization
4. System integrates for actual trading

---

## 🔬 Running Tests

Each component includes validation tests:

```bash
# Test Hamiltonian engine
python src/quantum_trading/hamiltonian/engine.py

# Test quantum layer  
python src/quantum_trading/quantum/wavefunction.py

# Test QUBO optimizer
python src/quantum_trading/optimization/qubo.py

# Test full system
python src/quantum_trading/execution/system.py
```

All tests include:
- Mathematical validation (energy conservation, unitarity)
- Example usage
- Expected output

---

## 🎮 Modes

### Simulation Mode (Default)
```python
system = TradingSystem(mode='simulation')
```
- Generates random market states
- No real money, no API keys needed
- Perfect for learning and testing

### Live Mode (Phase 2 Integration)
```python
system = TradingSystem(mode='live')
```
- Connects to real data sources (MT5, Alpaca, etc.)
- Requires Phase 2 data connectors
- See `experiments/markets/API_SETUP.md` for configuration

---

## 📈 Example Output

```
QUANTUM-INSPIRED TRADING SYSTEM
=================================================================

Configuration:
  Universe: ['SPY', 'QQQ']
  Capital: $10,000.00
  Mode: simulation

Starting event loop...

[Iteration 1/10]
  Hamiltonian energies:
    SPY: $450.23, E=0.000234
    QQQ: $380.45, E=0.000189
  Quantum layer:
    → LONG: 0.412
      FLAT: 0.301
      SHORT: 0.187
      HEDGE: 0.100
  ✓ Measured: LONG
  Portfolio:
    SPY: 11.08 shares @ $450.23 = $4,990.55
    QQQ: 13.13 shares @ $380.45 = $4,994.71
  PnL: +$15.23, Total value: $9,985.26

...

📊 FINAL SUMMARY
=================================================================

Performance:
  Total PnL: +$142.67
  Average PnL: +$14.27
  Std Dev: $23.45
  Sharpe ratio: 0.61

Action distribution:
  LONG: 4 (40.0%)
  FLAT: 3 (30.0%)
  SHORT: 2 (20.0%)
  HEDGE: 1 (10.0%)

✅ Log saved to: trading_log.csv
```

---

## 🎯 What Makes This Special?

### Not Just Another Trading Bot

1. **Physics-Based** - Hamiltonian mechanics, not ML heuristics
2. **Quantum-Inspired** - True superposition, not weighted averages  
3. **Mathematically Rigorous** - Preserves symplectic structure
4. **Empirically Validated** - Chapter 9 documents full validation journey
5. **Open Source** - Clone, run, verify, improve

### Why It Works

**Traditional systems**:
- Ad-hoc rules that break in new regimes
- Black-box ML with no interpretability
- Treat assets independently

**Quantum Hamiltonian system**:
- Universal physical principles that adapt
- Interpretable energy landscapes
- Natural multi-asset correlations via entanglement

---

## 🚀 Next Steps

1. **Run the demo** - See it working
2. **Read Chapter 9** - Understand the mathematics
3. **Modify parameters** - Experiment with Hamiltonian θ
4. **Add strategies** - Build on the framework
5. **Connect live data** - Use Phase 2 connectors
6. **Contribute** - Improve the system

---

## 📖 Learn More

- **Chapter 9**: `docs/book-of-mopati-chapter9-empirical-validation.md`
- **Phase 2 Data**: `experiments/markets/`
- **Source Code**: `src/quantum_trading/`
- **Repository**: https://github.com/Mopati123/universal-hamiltonian-framework

---

## ⚖️ Disclaimer

**FOR EDUCATIONAL PURPOSES ONLY**

This is a research project demonstrating mathematical principles.  
Not financial advice. Use at your own risk.

---

## 🎉 Credits

**Universal Hamiltonian Framework**  
Demonstrating how mathematics underpins reality through practical applications.

**Chapter 9: Empirical Validation**  
From theory to working trading software.

**Version**: 1.0.0  
**Status**: Production-ready demo  
**License**: MIT

---

**Clone it. Run it. See mathematics in action.** 🚀✨⚛️
