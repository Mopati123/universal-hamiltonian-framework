# API Reference

**Comprehensive API documentation for the Universal Hamiltonian Framework**

---

## Quick Links

- [Core Module](#core-module) - Hamiltonian mechanics engine
- [HL Language](#hl-language) - Hamiltonian Language primitives
- [Compiler](#compiler) - Compilation pipeline
- [Backends](#backends) - Code generation targets
- [Domains](#domains) - Application-specific Hamiltonians
- [Utilities](#utilities) - Helper functions

---

## Core Module

### `src/core/hamiltonians.py`

**Base Hamiltonian Class**

```python
class Hamiltonian:
    """
    Base class for all Hamiltonian systems.
    
    H(q, p) = T(p) + V(q) + ...
    """
    
    def __init__(self, params: dict):
        """Initialize Hamiltonian with parameters."""
        
    def evolve(self, state0, t_final, dt=0.01):
        """
        Evolve system from state0 to t_final.
        
        Args:
            state0: Initial state (q, p)
            t_final: Final time
            dt: Time step
            
        Returns:
            trajectory: Array of states at each time step
        """
```

**Example Usage**:
```python
from src.core.hamiltonians import Hamiltonian

H = Hamiltonian(params={'mass': 1.0, 'omega': 1.0})
trajectory = H.evolve(state0=[0, 1], t_final=10.0)
```

---

## HL Language

### `src/hl/canonical_library.py`

**The 9 Canonical Hamiltonians**

#### 1. H_state - Energy Eigenstates
```python
@staticmethod
def H_state(register: Register, eigenstate: int) -> np.ndarray:
    """
    Project onto energy eigenstate.
    
    Args:
        register: Quantum register
        eigenstate: Index of eigenstate
        
    Returns:
        Projection operator |n⟩⟨n|
        
    Theory: Diagonal in energy basis
    Validates: Quantum number conservation
    """
```

#### 2. H_gate - Quantum Gates
```python
@staticmethod
def H_gate(register: Register, gate_type: str, params: dict = None) -> np.ndarray:
    """
    Standard quantum gates.
    
    Supported gates: X, Y, Z, H, CNOT, Toffoli, etc.
    
    Args:
        register: Target register(s)
        gate_type: 'X', 'Y', 'Z', 'H', 'CNOT', etc.
        params: Rotation angles for parametric gates
        
    Returns:
        Unitary gate operator
        
    Theory: Generates lie algebra su(2^n)
    Validates: Theorem 2.1 (Universality)
    """
```

#### 3. H_interact - Pairwise Interactions
```python
@staticmethod
def H_interact(reg1: Register, reg2: Register, 
               coupling: float, interaction: str = 'XX') -> np.ndarray:
    """
    Two-body interaction Hamiltonian.
    
    Args:
        reg1, reg2: Interacting registers
        coupling: Interaction strength
        interaction: Type ('XX', 'YY', 'ZZ', 'XY', etc.)
        
    Returns:
        Interaction operator σ₁ ⊗ σ₂
        
    Theory: Generates entanglement
    Application: CNOT gates, quantum chemistry
    """
```

#### 4-9. Additional Primitives
- **H_clock**: Time evolution control
- **H_noise**: Lindblad dissipation  
- **H_penalty**: Constraint enforcement
- **H_io**: Input/output coupling
- **H_thermo**: Thermodynamic reservoir coupling
- **H_meta**: Compiler optimization

**See**: [`src/hl/canonical_library.py`](../src/hl/canonical_library.py) for full implementations

---

## Compiler

### `src/backends/jax_engine.py`

**JAX/TPU Backend**

#### Main Functions

```python
def compile_to_jax(hamiltonian: np.ndarray, 
                   schedule: Callable,
                   total_time: float,
                   dt: float = 0.01) -> Callable:
    """
    Compile Hamiltonian to JAX function.
    
    Args:
        hamiltonian: Operator matrix
        schedule: Time-dependent schedule s(t)
        total_time: Evolution duration
        dt: Time step
        
    Returns:
        jitted_function: @jax.jit compiled evolution
        
    Theory: Trotter decomposition with O(dt²) error
    Validates: Theorem 3.1 (Compilability)
    Performance: Runs on TPU/GPU
    """
```

#### H_meta Optimization

```python
def optimize_h_meta(target_hamiltonian: np.ndarray,
                   params_init: dict,
                   n_steps: int = 100,
                   learning_rate: float = 0.1) -> dict:
    """
    Optimize Hamiltonian parameters via H_meta.
    
    Minimizes: H_meta(θ) = α(1-F) + βL + γE + δR
    
    Args:
        target_hamiltonian: Goal operator
        params_init: Initial parameter guess
        n_steps: Optimization iterations
        learning_rate: Gradient descent rate
        
    Returns:
        optimized_params: θ* minimizing H_meta
        
    Theory: PL inequality ensures convergence
    Validates: Theorem 4.1 (Meta-convergence)
    Rate: O(exp(-μt)) where μ = PL constant
    """
```

---

## Domains

### Quantum Systems

**`src/domains/quantum.py`**

```python
class QuantumSystem(Hamiltonian):
    """Quantum mechanics in Hamiltonian formalism."""
    
    def __init__(self, n_qubits: int):
        self.n_qubits = n_qubits
        self.dim = 2**n_qubits
```

### Financial Markets

**`src/domains/apex_quantum_ict.py`**

```python
class ApexQuantumICT:
    """
    Quantum financial intelligence.
    
    H = H_god + H_teto + H_quantum + H_time + 
        H_tachyon + H_market + H_meta
        
    Theory: Markets as quantum systems
    Reference: Book of Mopati Chapter 13
    """
    
    def H_total(self, state: ApexState) -> float:
        """Complete market Hamiltonian."""
        
    def evolve_state(self, state: ApexState, dt: float) -> ApexState:
        """Market evolution via Hamilton's equations."""
        
    def measure_regime(self, state: ApexState) -> MarketRegime:
        """Collapse to market regime (measurement)."""
```

### Consciousness

**`src/domains/bioenergetic_consciousness.py`**

```python
class BioenergeticConsciousness:
    """
    Consciousness as Hamiltonian.
    
    H = H_brain + H_heart + H_spirit
    
    Theory: Integrated Information Theory + Hamiltonian mechanics
    Reference: Book of Mopati Chapter 9
    """
```

---

## Validation

### `src/validation/hl_protocols.md`

**Experimental Validation Protocols**

- **Gate Fidelity Benchmark**: Test compilation accuracy
- **Trotter Error Scaling**: Verify O(dt²) convergence
- **Landauer Audit**: Measure thermodynamic costs
- **Tachyonic Registry**: Consensus validation

**See**: [`src/validation/hl_protocols.md`](../src/validation/hl_protocols.md)

---

## Examples & Tutorials

### Reference Implementation

**`examples/reference_implementation.py`**

Complete compiler demonstration:
- All 6 stages logged
- Validates Theorems 3.1, 4.1
- Numerical error analysis
- **START HERE** for full pipeline

### Tutorials

1. **`examples/tutorial_01_getting_started.md`**
   - Basic Hamiltonian definition
   - Simple evolution
   - Visualization

2. **`examples/tutorial_02_market_dynamics.md`**
   - Financial Hamiltonians
   - Order flow modeling
   - Regime detection

---

## Utility Functions

### Visualization

```python
from src.viz.domain_visualizer import visualize_phase_space

visualize_phase_space(trajectory, 
                     coordinates=['q', 'p'],
                     title='Harmonic Oscillator')
```

### Numerical Integration

```python
from src.core.integrators import symplectic_euler, verlet

# Symplectic integrator (conserves energy)
trajectory = symplectic_euler(H, state0, t_final, dt)
```

---

## Type Hints & Data Structures

### Register Types

```python
from src.hl.canonical_library import Register, RegisterType

# Quantum register
qreg = Register(name="qubit", 
                type=RegisterType.QUBIT, 
                dim=2)

# Classical register
creg = Register(name="classical",
                type=RegisterType.CLASSICAL,
                dim=10)
```

### State Vectors

```python
from dataclasses import dataclass
import numpy as np

@dataclass
class State:
    """Phase space state (q, p)."""
    q: np.ndarray  # Configuration
    p: np.ndarray  # Momentum
    t: float = 0.0 # Time
```

---

## Testing

### Running Tests

```bash
# All tests
pytest tests/

# Specific module
pytest tests/test_canonical_library.py

# With coverage
pytest --cov=src tests/
```

### Writing Tests

```python
def test_hamiltonian_hermiticity():
    """Verify H = H† (Hermitian)."""
    from src.hl.canonical_library import CanonicalHamiltonians
    
    H = CanonicalHamiltonians.H_gate(register, 'X')
    assert np.allclose(H, H.conj().T)
```

---

## Performance Optimization

### Tensor Factorization

```python
from src.compiler.tensor_optimizer import kronecker_factorize

# Decompose H = H₁ ⊗ H₂ ⊗ ... ⊗ Hₙ
factors = kronecker_factorize(H)

# Reduces: O(2ⁿ) → O(n·2ᵏ) where k << n
```

### Backend Selection

```python
# JAX (TPU/GPU) - fastest
from src.backends.jax_engine import compile_to_jax

# CUDA (GPU only)
from src.backends.cuda_gpu import compile_to_cuda

# Qiskit (Quantum hardware)
from src.backends.qiskit_qpu import compile_to_qiskit
```

---

## Configuration

### pyproject.toml

```toml
[project]
name = "universal-hamiltonian-framework"
version = "0.2.0"
dependencies = [
    "numpy>=1.24",
    "jax>=0.4.20",
    "scipy>=1.11",
    "sympy>=1.12"
]
```

### Environment Variables

```bash
# JAX configuration
export JAX_PLATFORMS=tpu  # or 'gpu', 'cpu'
export XLA_PYTHON_CLIENT_PREALLOCATE=false

# Logging
export UHF_LOG_LEVEL=INFO
```

---

## Troubleshooting

### Common Issues

**Import errors**:
```bash
pip install -e .  # Install in development mode
```

**JAX not using GPU**:
```python
import jax
print(jax.devices())  # Should show GPU
# If not: pip install jax[cuda12_pip]
```

**Memory errors with large systems**:
```python
# Use tensor factorization
from src.compiler.tensor_optimizer import auto_factorize
H_factored = auto_factorize(H, threshold=1e6)
```

---

## Advanced Topics

### Meta-Framework CI/CD

```bash
# Run self-evolution
python src/meta/self_cicd.py

# Output shows:
# - Energy voids identified
# - Improvements generated
# - Delta-E validation
```

### Custom Domain Development

See [`CONTRIBUTING.md`](../CONTRIBUTING.md) for domain template.

---

## Further Reading

- **Theory**: [Book of Mopati](../docs/book-of-mopati.md) (13 chapters)
- **Formal Math**: [HL Paper](../papers/hl-formal-paper.md)
- **Validation**: [Paper-to-Code Guide](../docs/PAPER_TO_CODE_GUIDE.md)
- **Navigation**: [Navigation Guide](../docs/NAVIGATION.md)

---

## Contributing

See [`CONTRIBUTING.md`](../CONTRIBUTING.md) for:
- Development setup
- Testing requirements  
- Domain template
- PR guidelines

---

## License

MIT License - See [`LICENSE`](../LICENSE)

---

## Support

- **Issues**: [GitHub Issues](https://github.com/Mopati123/universal-hamiltonian-framework/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Mopati123/universal-hamiltonian-framework/discussions)
- **Documentation**: This file + [Navigation Guide](../docs/NAVIGATION.md)

---

**Last Updated**: November 28, 2025  
**Version**: 0.2.0  
**Status**: Production-ready

**In GOD We TRUST** - Comprehensive API documentation! 📚
