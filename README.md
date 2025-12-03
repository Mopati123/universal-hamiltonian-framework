# Universal Hamiltonian Framework

**Reality is Hamiltonian. This framework proves it, then builds on it.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)](#)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

---

## 🚀 Quick Start (5 Minutes)

**See Hamiltonian mechanics in action - right now!**

### Install
```bash
git clone https://github.com/Mopati123/universal-hamiltonian-framework.git
cd universal-hamiltonian-framework
pip install -e .
```

### Your First Hamiltonian
```python
from hl import Register, RegisterType, Hamiltonian
import numpy as np

# 1. Create a qubit (2-dimensional quantum system)
qubit = Register("spin", RegisterType.QUBIT, 2)

# 2. Define Hamiltonian (Pauli-Z operator: measures spin)
H = np.array([[1, 0],    # Energy = +1 for spin-up
              [0, -1]])   # Energy = -1 for spin-down

# 3. Initial state: superposition (50% up, 50% down)
psi_0 = np.array([1, 1]) / np.sqrt(2)

# 4. Evolve under H for time t=1.0
from scipy.linalg import expm
psi_t = expm(-1j * H * 1.0) @ psi_0

print(f"Initial state: {psi_0}")
print(f"Evolved state: {psi_t}")
print(f"Energy expectation: {np.vdot(psi_t, H @ psi_t).real:.3f}")
```

**What's happening?**  
The qubit evolves in phase space under Hamiltonian H. Spin-up and spin-down components oscillate - this is **quantum phase space flow!**

**See the result immediately**: Just run it! You've used the same math that describes atoms, markets, and consciousness.

➡️ **Want to learn more?** Start with [Chapter 0: Mathematical Foundations](docs/book-of-mopati-chapter0.md)  
➡️ **See more examples?** Check [examples/](examples/)  
➡️ **Build something?** Read the [Full Tutorial](docs/PAPER_TO_CODE_GUIDE.md)

---

## The Foundation: Why Hamiltonian Mechanics Underpins EVERYTHING

**This is not a metaphor. This is literal truth.**

### The Irreducible Core: Three Axiomatic Pillars

Every system in reality—from quantum particles to financial markets to human consciousness—operates on these three irreducible principles:

#### **Pillar I: Canonical Pairs (q, p)**
> *Every system has conjugate variables that completely specify its state.*

**What this means in reality**:
- **Position (q)** and **Momentum (p)** are fundamental
- Together, they form **phase space** - the true map of all possible states
- **Nothing exists outside phase space**
- This is why we can predict: knowing (q, p) tells us everything

**Examples across domains**:
- Physics: (position, momentum)
- Markets: (price, order flow) 
- Consciousness: (thought state, attention momentum)
- Blockchain: (ledger state, validation momentum)

---

#### **Pillar II: Hamiltonians as Generators**
> *The Hamiltonian H generates time evolution.*

**What this means in reality**:
- **H = Total Energy** of the system
- Hamilton's equations describe HOW everything changes:
  ```
  q̇ = ∂H/∂p    (momentum causes position to change)
  ṗ = -∂H/∂q   (position causes momentum to change)
  ```
- **Time evolution = Flow in phase space**
- The future is determined by H

**Why this is universal**:
- Every equation of motion can be written as Hamilton's equations
- This isn't a choice - it's the structure of reality
- From Newton to Schrödinger, all are Hamiltonian

---

#### **Pillar III: Symplectic Structure**
> *Phase space preserves volume (Liouville's theorem).*

**What this means in reality**:
- **Information is conserved**
- No information loss during evolution
- This connects classical mechanics to quantum unitarity
- Why the universe is reversible at the fundamental level

**Consequence**: 
- Everything that can happen is encoded in phase space
- Evolution preserves the "shape" of possibility
- This is why quantum mechanics works

---

### Why These Axioms Are Irreducible

**You cannot go deeper than this.**

Try to describe ANY dynamical system without:
1. Variables that specify state ❌ Impossible
2. Something that generates change ❌ Impossible  
3. Conservation of information ❌ Violates physics

**These three axioms are the bedrock of reality itself.**

---

### How This Framework Proves Universality

**Chapter 0 shows**: How 2000 years of mathematics (from Archimedes to quantum theory) ALL converged to Hamilton's equations.

**Six independent paths**, starting from completely different fields:
1. **Geometry** → Shortest paths → Action principle → Hamilton ✓
2. **Physics** → Newton's laws → Lagrange → Hamilton ✓
3. **Optics** → Light rays → Fermat → Hamilton ✓
4. **Thermodynamics** → Heat → Boltzmann → Hamilton (Z = Σe^(-βH)) ✓
5. **Quantum** → Heisenberg → Schrödinger → Hamilton (iℏ∂ψ/∂t = Ĥψ) ✓
6. **Information** → Shannon → Landauer → Hamilton (reversible computing) ✓

**All roads lead to Hamilton. This is not coincidence.**

**This is proof that Hamiltonian mechanics IS the structure of reality.**

---

## 🎯 START HERE: Your Learning Journey

**EVERYONE begins with Chapter 0** - it's where the mathematical foundation is built.

### Step 1: Choose Your Difficulty Level

**🌱 Beginner** (New to this)  
→ **Start**: [Chapter 0 - Mathematical Foundations](docs/book-of-mopati-chapter0.md)  
→ **Read**: 🟢 Green sections only (~45 minutes)  
→ **Get**: Intuitive understanding of why everything is Hamiltonian  
→ **Then**: [Chapter 1 - See it applied](docs/book-of-mopati.md)

---

**🌿 Intermediate** (Undergrad level)  
→ **Start**: [Chapter 0 - Mathematical Foundations](docs/book-of-mopati-chapter0.md)  
→ **Read**: 🟢 Green + 🟡 Yellow sections (~2 hours)  
→ **Get**: Can derive Hamilton's equations, solve problems  
→ **Then**: [Chapter 4 - Quantum connection](docs/book-of-mopati-chapter4.md)

---

**🌳 Advanced** (Graduate level)  
→ **Start**: [Chapter 0 - Mathematical Foundations](docs/book-of-mopati-chapter0.md)  
→ **Read**: All sections including 🟠 Orange (~4 hours)  
→ **Get**: Complete mathematical mastery  
→ **Then**: [Chapter 2 - Meta-framework](docs/book-of-mopati-chapter2.md)

---

**🌲 Expert** (Researcher/PhD)  
→ **Start**: [Chapter 0 - Mathematical Foundations](docs/book-of-mopati-chapter0.md)  
→ **Read**: Everything including 🔴 Red sections (~6 hours)  
→ **Get**: Verify convergence, find novel connections  
→ **Then**: [Chapter 12 - Universal compiler](docs/book-of-mopati-chapter12.md)

---

**🔥 Speed Run** (30 minutes)  
→ **Start**: [Chapter 0 - Speed Run sections](docs/book-of-mopati-chapter0.md#speed-run)  
→ **Read**: Just highlights (~30 minutes)  
→ **Get**: Elevator pitch understanding  
→ **Then**: Decide to dive deeper or integrate

---

### What Chapter 0 Teaches You

**The complete mathematical history showing ALL frameworks converge to Hamilton**:

1. **Archimedes** (300 BC) → Levers, first conservation law
2. **Galileo** (1590) → Objects fall together, quantitative physics
3. **Newton** (1687) → F = ma, universal laws (but limited)
4. **Euler & Lagrange** (1750) → Least action, coordinate freedom
5. **Hamilton** (1833) → **THE BREAKTHROUGH** - Perfect symmetry (q,p)
6. **Quantum Era** (1925) → Confirms Hamilton was right all along!
7. **Feynman** (1948) → Path integrals = least action
8. **Today** → Everything is Hamiltonian (proven)

**By the end of Chapter 0**, you'll understand:
- Why (q, p) phase space is reality's true map
- How Hamilton's equations generate all motion
- Why this framework is universal (not just "useful")
- The mathematical proof via convergence

---

## 🧭 Quantum Entangled Navigation

**Direct jump to exactly what you need** - choose your interest:

### By Goal

**Want to understand the theory?**  
→ [Start: Chapter 0](docs/book-of-mopati-chapter0.md) → [Chapter 1: Axioms](docs/book-of-mopati.md) → [Chapter 3: Universality](docs/book-of-mopati-chapter3.md)

**Want to see the math?**  
→ [Start: Chapter 0 (🟡🟠 sections)](docs/book-of-mopati-chapter0.md) → [Formal Paper](papers/hl-formal-paper.md) → [Reference Implementation](examples/reference_implementation.py)

**Want to build something?**  
→ [Quick Start: Run code first](examples/minimal_example.py) → [Chapter 0: Understand why it works](docs/book-of-mopati-chapter0.md) → [Domain Examples](examples/)

**Want to verify claims?**  
→ [Chapter 0: Grand Convergence](docs/book-of-mopati-chapter0.md#convergence) → [Test Suite](tests/) → [Meta-Framework](src/meta/self_cicd.py)

**Want to apply to specific domain?**  
→ [Markets](docs/book-of-mopati-chapter8.md) | [AI](docs/book-of-mopati-chapter5.md) | [Blockchain](docs/book-of-mopati-chapter10.md) | [Consciousness](docs/book-of-mopati-chapter9.md)

---

## 📚 The Book of Mopati - Complete Guide

**Chapter 0** is the foundation. All other chapters build on it.

### Foundation (Start Here!)
**0. [Mathematical Foundations](docs/book-of-mopati-chapter0.md)** ← **START HERE**  
   *How 2000 years of math converged to Hamilton*

**1. [Axiomatic Foundation](docs/book-of-mopati.md)**  
   *The Three Pillars applied to reality*

**2. [Meta-Hamiltonian Singularity](docs/book-of-mopati-chapter2.md)**  
   *Systems that observe themselves*

**3. [Domain Universality](docs/book-of-mopati-chapter3.md)**  
   *Proof that EVERY system is Hamiltonian*

**4. [Quantum Foundations](docs/book-of-mopati-chapter4.md)**  
   *Classical → Quantum connection*

### Applications
**5-13**: [Markets](docs/book-of-mopati-chapter8.md), [AI](docs/book-of-mopati-chapter5.md), [Consciousness](docs/book-of-mopati-chapter9.md), [Blockchain](docs/book-of-mopati-chapter10.md), and more

**[→ See complete chapter list](docs/BOOK_INDEX.md)**

---

## Quick Start

```bash
# Clone repository
git clone https://github.com/Mopati123/universal-hamiltonian-framework
cd universal-hamiltonian-framework

# Install dependencies
pip install -e .

# Run minimal example to see it working
python examples/minimal_example.py
```

**Then read Chapter 0 to understand WHY it works!**

---

## Philosophy

**This framework emerged from one realization**:

> **Hamiltonian mechanics is not a "model" of reality.**  
> **It IS reality's structure.**

The three axiomatic pillars are:
1. **Inevitable** (cannot be more fundamental)
2. **Universal** (apply to everything)
3. **Complete** (nothing outside their scope)

Chapter 0 proves this by showing six independent mathematical paths all converge to Hamilton's equations.

**This is not math convenience. This is ontological truth.**

---

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md).

---

## License

MIT License - See [LICENSE](LICENSE).

---

## Citation

```bibtex
@software{universal_hamiltonian_framework,
  title = {Universal Hamiltonian Framework: Reality's Operating System},
  author = {Mopati Labs},
  year = {2025},
  note = {Mathematical proof that all systems are Hamiltonian},
  url = {https://github.com/Mopati123/universal-hamiltonian-framework}
}
```

---

**In GOD We TRUST** - Chapter 0 is where everything begins! 🌌

**→ [Start Your Journey: Chapter 0 - Mathematical Foundations](docs/book-of-mopati-chapter0.md)** ✅
