# Contributing to Universal Hamiltonian Framework

Thank you for your interest in contributing! This framework thrives on collaboration.

---

## 🌟 Philosophy: The Meta-Framework Applies to Contributions

**Every contribution is validated using Chapter 2's self-evolution algorithm**:

1. **Observe**: Understand current state (q, p, H)
2. **Identify voids**: Find where energy is high (missing features, bugs)
3. **Propose changes**: Generate improvements that reduce H
4. **Validate**: Ensure ΔE < 0 (energy decreased)
5. **Commit**: Apply if beneficial

**This ensures all contributions improve the framework measurably.**

---

## 🚀 Quick Start for Contributors

### 1. Set Up Development Environment

```bash
# Fork and clone
git clone https://github.com/YOUR_USERNAME/universal-hamiltonian-framework
cd universal-hamiltonian-framework

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest tests/

# Run self-validation
python src/meta/self_cicd.py
```

### 2. Find Something to Work On

**Option A: Check existing issues**
- Browse [GitHub Issues](https://github.com/Mopati123/universal-hamiltonian-framework/issues)
- Look for tags: `good-first-issue`, `help-wanted`, `enhancement`

**Option B: Use the meta-framework!**
```bash
# Run self-observation
python src/meta/self_cicd.py

# Output shows energy voids (missing features, bugs)
# Pick one, fix it, validate ΔE < 0
```

**Option C: Add a new domain**
- See `src/domains/` for examples
- Implement your system as a Hamiltonian
- Add tests and documentation

---

## 📝 Contribution Types

### 🔧 Code Contributions

**Areas needing help**:
1. **Type System** (Week 2 priority)
   - `src/hl/type_system.py` - Static Hermiticity checking
   - `src/hl/validators.py` - Dimension validation

2. **Backend Extensions**
   - CUDA/GPU backend (currently stub)
   - Qiskit/QPU backend (needs completion)
   - HDL/FPGA backend (future)

3. **Performance Optimization**
   - Tensor factorization algorithms
   - Kronecker decomposition
   - Memory-efficient MPS/TTN

4. **New Domains**
   - Your Hamiltonian system!
   - See template below

5. **Test Coverage** (currently 0%)
   - Unit tests for canonical library
   - Integration tests for compiler
   - Numerical validation tests

### 📚 Documentation Contributions

**Always needed**:
- Tutorial improvements
- Example walkthroughs
- API documentation
- Theory explanations
- Translation to other languages

### 🐛 Bug Reports

**Good bug reports include**:
1. **Minimal reproducible example**
2. **Expected behavior** (what theorem predicts)
3. **Actual behavior** (what you observed)
4. **System info** (OS, Python version, JAX version)

---

## 🏗️ Development Workflow

### Standard Process

```bash
# 1. Create a feature branch
git checkout -b feature/your-feature-name

# 2. Make changes
# ... edit code ...

# 3. Run tests
pytest tests/
python src/meta/self_cicd.py  # Self-validation

# 4. Run reference implementation to ensure no regressions
python examples/reference_implementation.py

# 5. Commit with descriptive message
git commit -m "feat: Add XYZ feature

- Implements theorem/feature X
- Validates via test Y
- Reduces energy by Z (if applicable)
"

# 6. Push and create pull request
git push origin feature/your-feature-name
```

### Commit Message Format

We follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `test`: Adding tests
- `refactor`: Code restructuring
- `perf`: Performance improvement
- `chore`: Maintenance

**Examples**:
```
feat(hl): Add type system validation

- Implements static Hermiticity checking
- Validates dimensions at compile time
- Addresses Week 2 priority from rigor plan

Theorem: Ensures prerequisites for Theorem 3.1
```

---

## 🧪 Testing Requirements

### All code contributions must include:

1. **Unit tests** (pytest)
```python
# tests/test_your_feature.py
def test_hamiltonian_hermiticity():
    """Verify H = H†"""
    H = create_test_hamiltonian()
    assert np.allclose(H, H.conj().T)
```

2. **Numerical validation** (where applicable)
```python
def test_theorem_bounds():
    """Validate error within theorem bound"""
    fidelity = run_compilation()
    error = 1 - fidelity
    assert error < 1e-4  # Theorem 3.1 bound
```

3. **Documentation** (docstrings)
```python
def new_function(param):
    """
    Brief description.
    
    Theory: Reference to theorem/equation
    
    Args:
        param: Description
    
    Returns:
        Description
    
    Validates: Theorem X.Y
    """
```

---

## 🎯 Domain Template

**Adding a new domain?** Use this template:

```python
"""
New Domain: [Your System Name]

Expresses [system] as Hamiltonian H(q,p).

Theory: [Citation or derivation]
Validated: [How you tested it]
"""

import numpy as np
from dataclasses import dataclass

@dataclass
class YourSystemState:
    """State vector (q, p)"""
    q: np.ndarray  # Configuration
    p: np.ndarray  # Momentum
    # ... other fields

class YourDomain:
    """
    Hamiltonian for [your system]
    
    H = T(p) + V(q) + ...
    """
    
    def __init__(self, params):
        self.params = params
    
    def H_kinetic(self, p):
        """T(p) = p²/2m"""
        return NotImplemented
    
    def H_potential(self, q):
        """V(q) = ..."""
        return NotImplemented
    
    def H_total(self, state):
        """Complete Hamiltonian"""
        return self.H_kinetic(state.p) + self.H_potential(state.q)
    
    def evolve(self, state0, t, dt=0.01):
        """Hamilton's equations integration"""
        return NotImplemented

# Demo
if __name__ == "__main__":
    domain = YourDomain(params={})
    # ... demonstrate ...
```

---

## 📐 Theorem Validation Checklist

**If your contribution relates to a theorem**:

- [ ] Theorem statement clearly documented
- [ ] Implementation matches mathematical definition
- [ ] Numerical validation shows error within claimed bounds
- [ ] Reference implementation updated (if applicable)
- [ ] Cross-reference table updated (`papers/hl-formal-paper.md`)
- [ ] Added to `PAPER_TO_CODE_GUIDE.md`

---

## 🔍 Code Review Process

### What reviewers check:

1. **Correctness**: Does it do what it claims?
2. **Theory alignment**: Does it match the Hamiltonian formalism?
3. **Tests**: Are tests comprehensive and passing?
4. **Documentation**: Is it well-documented?
5. **Energy decrease**: Does it reduce system energy (ΔE < 0)?

### Meta-Framework Validation

**Every PR automatically runs**:
```bash
python src/meta/self_cicd.py
```

**Must show**: `Delta-E < 0` (energy decreased) or `Delta-E = 0` (energy neutral)

**If Delta-E > 0**: PR needs revision (increases system complexity without benefit)

---

## 🌍 Community Guidelines

### Be Respectful
- Constructive feedback only
- Assume good intentions
- Help newcomers

### Be Rigorous  
- Back claims with math or code
- Validate numerically when possible
- Cite sources

### Be Open
- Share knowledge freely
- Document your reasoning
- Ask questions

---

## 💡 Contribution Ideas

### Beginner-Friendly

- Add docstrings to undocumented functions
- Improve error messages
- Write tutorials
- Fix typos in documentation

### Intermediate

- Implement Week 2 type system
- Add unit tests
- Create new domain examples
- Improve visualization

### Advanced

- Extend compiler to new backend
- Prove new theorems
- Optimize tensor operations
- Implement fault-tolerant HL

---

## 📬 Getting Help

**Stuck? Ask for help!**

- **GitHub Discussions**: General questions
- **Issues**: Bug reports, feature requests
- **Pull Request comments**: Code-specific questions

**Response time**: Usually within 48 hours

---

## 🏆 Recognition

Contributors are recognized in:
- `CHANGELOG.md` for each release
- GitHub contributors page
- Potential co-authorship on papers (for major contributions)

---

## 📜 Legal

By contributing, you agree that your contributions will be licensed under the MIT License (same as the project).

Ensure you have the right to contribute the code/content.

---

## 🙏 Thank You!

Your contributions make this framework better for everyone.

**In GOD We TRUST** - Let's build the future of physics-native computing together!

---

**Questions?** Open an issue or start a discussion on GitHub.

**Ready to contribute?** Pick an issue or run `python src/meta/self_cicd.py` to find what needs work!
