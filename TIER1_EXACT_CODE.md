# TIER 1 IMPLEMENTATION: Exact Code to Add

## Ready to Execute Phase 1

This document contains the **exact code** to add to fix Tier 1 (60 lines total).

---

## FILE 1: examples/domain_markets.py

### Current State
The file has functions like `black_scholes_hamiltonian()` and `hamiltons_equations()` but no class wrapper.

### What to Add
Insert this class definition **after the imports and before the function definitions**:

```python
class BlackScholesHamiltonian:
    """
    Black-Scholes Hamiltonian System
    
    Represents financial market dynamics in canonical phase space:
    - q = Stock price S
    - p = Price momentum p_S
    
    H(S, p_S) = (1/2)σ²S²p_S² + rSp_S
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
        """
        return self.sigma**2 * q**2 * p + self.r * q
    
    def dp_dt(self, q: float, p: float) -> float:
        """
        Hamilton's equation: dp_S/dt = -∂H/∂S
        
        Canonical derivative of momentum w.r.t. time.
        """
        return -(self.sigma**2 * q * p**2 + self.r * p)
```

**Location**: After line 9 (after imports), before `def black_scholes_hamiltonian()` function.

**Lines added**: 42

---

## FILE 2: examples/domain_consciousness.py

### Current State
Has functions like `attention_hamiltonian()` but no class wrapper.

### What to Add

```python
class ConsciousnessHamiltonian:
    """
    Consciousness Hamiltonian System
    
    Represents cognitive dynamics in canonical phase space:
    - q = Thought state θ
    - p = Attention momentum p_θ
    
    H(θ, p_θ) = p_θ²/(2m) + V(θ)
    where V(θ) = -salience·cos(θ)
    """
    
    def __init__(self, salience: float, mass: float):
        """
        Initialize consciousness Hamiltonian.
        
        Args:
            salience: How important/interesting the thought is
            mass: Cognitive inertia (resistance to context switching)
        """
        self.salience = salience
        self.mass = mass
    
    def hamiltonian(self, q: float, p: float) -> float:
        """
        Compute total cognitive energy: H(θ, p_θ)
        
        Args:
            q: Thought state (angle)
            p: Attention momentum
            
        Returns:
            Total cognitive energy
        """
        return attention_hamiltonian(q, p, self.salience, self.mass)
    
    def dq_dt(self, q: float, p: float) -> float:
        """
        Hamilton's equation: dθ/dt = ∂H/∂p_θ
        
        Attention drives thought change.
        """
        return p / self.mass
    
    def dp_dt(self, q: float, p: float) -> float:
        """
        Hamilton's equation: dp_θ/dt = -∂H/∂θ
        
        Salience creates attention force.
        """
        return -self.salience * np.sin(q)
```

**Location**: After line 10 (after imports), before `def attention_hamiltonian()` function.

**Lines added**: 42

---

## FILE 3: examples/domain_blockchain.py

### Current State
Has the `BlockState` class and functions but no Hamiltonian class wrapper.

### What to Add

```python
class BlockchainHamiltonian:
    """
    Blockchain Consensus Hamiltonian System
    
    Represents distributed ledger dynamics in canonical phase space:
    - q = Consensus state (per node)
    - p = Validation momentum (per node)
    
    H = Σᵢ[pᵢ²/(2m) + V(qᵢ)] + coupling·Σᵢⱼ(qᵢ - qⱼ)²
    """
    
    def __init__(self, n_nodes: int, coupling: float = 1.0, mass: float = 1.0):
        """
        Initialize blockchain Hamiltonian.
        
        Args:
            n_nodes: Number of nodes in network
            coupling: Strength of consensus force
            mass: Node "mass" (validation difficulty)
        """
        self.n_nodes = n_nodes
        self.coupling = coupling
        self.mass = mass
    
    def hamiltonian(self, q: np.ndarray, p: np.ndarray) -> float:
        """
        Compute total network energy: H(state, momentum)
        
        Args:
            q: State vector (one entry per node)
            p: Momentum vector (one entry per node)
            
        Returns:
            Total network Hamiltonian
        """
        return consensus_hamiltonian(q, p, self.coupling)
    
    def dq_dt(self, q: np.ndarray, p: np.ndarray) -> np.ndarray:
        """
        Hamilton's equation: dq/dt = ∂H/∂p
        
        Momentum drives state change.
        """
        return p / self.mass
    
    def dp_dt(self, q: np.ndarray, p: np.ndarray) -> np.ndarray:
        """
        Hamilton's equation: dp/dt = -∂H/∂q
        
        State disagreement creates consensus force.
        """
        N = len(q)
        force = np.zeros(N)
        
        # Coupling forces from other nodes
        for i in range(N):
            for j in range(N):
                if i != j:
                    force[i] += 2 * self.coupling * (q[i] - q[j])
        
        return -force
```

**Location**: After line 12 (after imports), before `class BlockState()` class.

**Lines added**: 47

---

## TOTAL CODE TO ADD

```
File 1: 42 lines
File 2: 42 lines
File 3: 47 lines
─────────────────
Total: 131 lines

Wait! This is more than 60 lines I said...
But it's still simple class wrappers.
Error: I underestimated slightly. Actual is ~130 lines.
This is still QUICK work (< 1 hour to code).
```

---

## How to Add This Code

### Option A: Manual (Recommended First Time)

1. Open `examples/domain_markets.py` in VS Code
2. Find line 9 (after imports)
3. Press Enter to create new line
4. Copy-paste the `BlackScholesHamiltonian` class
5. Repeat for consciousness and blockchain files

### Option B: I'll Do It (Tell me "EXECUTE" and I'll add it immediately)

---

## Verification After Adding

Once you add the code, run:

```powershell
cd "c:\Users\ramaologam\Hamiltonian_beta_test\universal-hamiltonian-framework"
python test_axioms.py
```

**Expected output after Tier 1 additions**:
```
AXIOM 1: Canonical Pairs
----------------------------------------------------------------------
  ✓ Markets: (q=100.0, p=0.5) → unique evolution
  ✓ Consciousness: (q=0.5, p=1.0) → unique evolution
  ✓ Blockchain: 3 (q,p) pairs → unique evolution

AXIOM 1 STATUS: ✅ PASS

AXIOM 2: Hamiltonian Generator
----------------------------------------------------------------------
  ✓ Harmonic oscillator: H → Hamilton's equations verified
  ✓ Markets: H(q,p) = 5.4500 is well-defined scalar

AXIOM 2 STATUS: ✅ PASS
```

---

## Code Quality Checklist

✅ Type hints included (float, np.ndarray)
✅ Docstrings comprehensive
✅ Follows existing code style
✅ No breaking changes
✅ Uses existing functions (clean integration)
✅ Simple, readable, maintainable

---

## Next: Tier 2 (After Tier 1 Passes)

Once Tier 1 works, we add ~100 lines to `test_axioms.py` to validate:
- Energy conservation
- Symplectic structure
- Liouville's theorem
- Noether's theorem

But first: **Get Tier 1 working.**

---

## Ready?

I can:

1. **Add this code immediately** (if you say "EXECUTE")
2. **Guide you to add it manually** (step-by-step)
3. **Explain any part** (if unclear)

What's your preference?

Type: `EXECUTE` or `MANUAL` or `EXPLAIN`
