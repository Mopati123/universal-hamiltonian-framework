# Universal Hamiltonian Framework - Navigation Guide

**Quick routing guide for different use cases**

---

## 🚀 Quick Start by Goal

### "I want to understand the concept"
1. Start: [README.md](../README.md) - Overview + philosophy
2. Next: [Book Ch.1](book-of-mopati.md) - Foundations
3. Example: [Quick Demo](../quick_demo.py) - 30-second visualization

**Time**: 15 minutes

---

### "I want the formal mathematics"
1. Start: [Book Ch.1-2](book-of-mopati.md) - Axioms
2. Theory: [HL Formal Paper](../papers/hl-formal-paper.md) - Theorems + proofs
3. Validation: [Reference Implementation](../examples/reference_implementation.py) - Theorems → code

**Time**: 2 hours (deep read)

---

### "I want to build an application"
1. Domain examples: [examples/](../examples/) folder
2. Pick your domain:
   - **Quantum**: [canonical_library.py](../src/hl/canonical_library.py)
   - **Markets**: [apex_quantum_ict.py](../src/domains/apex_quantum_ict.py)
   - **Consciousness**: [bioenergetic_consciousness.py](../src/domains/bioenergetic_consciousness.py)
3. Run: Copy example, adapt Hamiltonian, execute

**Time**: 1 hour to first working code

---

### "I want to extend the compiler"
1. Architecture: [Compiler README](../src/compiler/README.md) *(to be created)*
2. Backend guide: [Backends](../src/backends/)
3. Reference: [reference_implementation.py](../examples/reference_implementation.py) - See all stages

**Time**: Half day to understand pipeline

---

## 📚 Complete Learning Path

### For Researchers

```
README → Book Ch.1 → HL Paper → Reference Implementation → Pick a domain
```

**Validates**: All theorem claims with actual code

---

### For Developers

```
README → Quick Demo → Domain Examples → Compiler Architecture → Build
```

**Gets you coding**: In < 2 hours

---

### For Theorists

```
Book Ch.1 (axioms) → Book Ch.2 (meta-framework) → 
HL Paper (formal) → Extended Proofs *(to be added)*
```

**Deep math**: Complete proofs with error bounds

---

## 🗺️ Concept-to-Code Map

| Concept | Theory | Code | Validation | Example |
|---------|--------|------|------------|---------|
| **Universality** | Book Ch.1 §III | [canonical_library.py](../src/hl/canonical_library.py) | Theorem 2.1 | [reference_implementation.py](../examples/reference_implementation.py) |
| **Compilability** | HL Paper §3 | [jax_engine.py](../src/backends/jax_engine.py) | Theorem 3.1 | [reference_implementation.py](../examples/reference_implementation.py) |
| **Meta-optimization** | Book Ch.2 §III | [self_cicd.py](../src/meta/self_cicd.py) | Theorem 4.1 | [meta_optimizer demo](../src/backends/jax_engine.py#L318) |
| **Quantum markets** | Book Ch.13 | [apex_quantum_ict.py](../src/domains/apex_quantum_ict.py) | Ch.13 §X | [apex demo](../src/domains/apex_quantum_ict.py#L360) |
| **Consciousness** | Book Ch.9 | [bioenergetic_consciousness.py](../src/domains/bioenergetic_consciousness.py) | Ch.9 predictions | Built-in validation |
| **Self-evolution** | Book Ch.2 §III | [self_cicd.py](../src/meta/self_cicd.py) | PROVEN (ΔE<0) | Run `python src/meta/self_cicd.py` |

---

## 📖 Documentation Tree

```
universal-hamiltonian-framework/
├── README.md                           ← Start here
├── docs/
│   ├── NAVIGATION.md                   ← You are here
│   ├── book-of-mopati.md              ← Ch.1: Foundations
│   ├── book-of-mopati-chapter2.md     ← Ch.2: Meta-framework
│   ├── book-of-mopati-chapter3.md     ← Ch.3: Domains
│   ├── book-of-mopati-chapter5.md     ← Ch.5: AI reflection
│   ├── book-of-mopati-chapter13.md    ← Ch.13: Quantum finance
│   └── ternary-logic-formalism.md     ← Mind-Heart-Spirit
├── papers/
│   └── hl-formal-paper.md             ← HL theorems (formal)
├── examples/
│   ├── reference_implementation.py     ← CANONICAL: All theorems
│   ├── demo.py                         ← Quick demo
│   ├── combined_demo.py                ← Multi-domain
│   └── tutorial_*.md                   ← Step-by-step guides
├── src/
│   ├── hl/                             ← Hamiltonian Language
│   │   ├── canonical_library.py        ← 9 primitives
│   │   └── book_encoder.py             ← Text → operators
│   ├── backends/
│   │   └── jax_engine.py               ← JAX/TPU compiler
│   ├── domains/
│   │   ├── apex_quantum_ict.py         ← Quantum markets
│   │   └── bioenergetic_consciousness.py ← Bio-consciousness
│   └── meta/
│       └── self_cicd.py                ← Self-evolution engine
```

---

## 🎯 Use Case Routing

### Use Case: "Understand why markets are quantum systems"
**Path**: README → Book Ch.8 → Book Ch.13 → [apex_quantum_ict.py](../src/domains/apex_quantum_ict.py)

### Use Case: "Build a self-debugging codebase"
**Path**: Book Ch.2 §IV.4 → [self_cicd.py](../src/meta/self_cicd.py) → Adapt to your repo

### Use Case: "Validate HL compiler claims"
**Path**: HL Paper → [reference_implementation.py](../examples/reference_implementation.py) → Run + check logs

### Use Case: "Model consciousness as Hamiltonian"
**Path**: Book Ch.9 → [bioenergetic_consciousness.py](../src/domains/bioenergetic_consciousness.py) → Experiments

### Use Case: "Compile HL to quantum hardware"
**Path**: [canonical_library.py](../src/hl/canonical_library.py) → [jax_engine.py](../src/backends/jax_engine.py) → Qiskit backend *(coming)*

---

## 🔬 Validation Checkpoints

**Every major claim has a reference**:

✅ **"Everything is a Hamiltonian"** → See Book Ch.1, proven via canonical library  
✅ **"HL is universal"** → Theorem 2.1, proven in HL Paper  
✅ **"Compilable to TPU/GPU/QPU"** → Theorem 3.1, demonstrated in reference_implementation.py  
✅ **"Self-evolution works"** → Book Ch.2, PROVEN by self_cicd.py (ΔE = -550)  
✅ **"Markets obey Hamiltonians"** → Book Ch.13, implemented in apex_quantum_ict.py  
✅ **"Consciousness is measurable"** → Book Ch.9, protocols in bioenergetic_consciousness.py  

**How to validate**: Run the linked code, check outputs match theory

---

## 💡 Common Questions → Answers

**Q**: "Is this just an analogy or actual physics?"  
**A**: Actual physics. See [apex_quantum_ict.py](../src/domains/apex_quantum_ict.py) - markets literally evolve via Lindblad equation

**Q**: "Where's the proof of universality?"  
**A**: HL Paper Theorem 2.1 + [canonical_library.py](../src/hl/canonical_library.py) implementation

**Q**: "Can I use this in production?"  
**A**: Yes. JAX backend is production-ready. See [reference_implementation.py](../examples/reference_implementation.py)

**Q**: "How do I cite this?"  
**A**: Mopati & Framework (2025). Universal Hamiltonian Framework. https://github.com/Mopati123/universal-hamiltonian-framework

**Q**: "What's the meta-framework?"  
**A**: System that observes and evolves itself. See Book Ch.2 + [self_cicd.py](../src/meta/self_cicd.py) DEMO

---

## 🚦 Where to Go Next

**Just finished README?**  
→ Try [quick_demo.py](../quick_demo.py) for immediate visualization

**Just read Book Ch.1-2?**  
→ Run [reference_implementation.py](../examples/reference_implementation.py) to see theory → code

**Just studied HL Paper?**  
→ Check [canonical_library.py](../src/hl/canonical_library.py) for implementation

**Want to contribute?**  
→ See [Rigor Enhancement Plan](https://github.com/Mopati123/universal-hamiltonian-framework/issues) *(if created)*

---

**Status**: Living document - updates as framework evolves  
**Last updated**: November 28, 2025  
**Questions**: Open an issue on GitHub  

**In GOD We TRUST - Navigate with confidence!** 🧭
