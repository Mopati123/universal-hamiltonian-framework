# Book of Mopati — Chapter 3: Domain Mappings

> **Classification:** `standard_physics`, `engineering_analogy`, `research_hypothesis`
> **Evidence:** Physical Hamiltonians are standard where stated; nonphysical mappings are explicit constructions.
> **Certification scope:** Defines when cross-domain reuse is structural, analogous, or speculative.

## 3.1 One notation does not imply one ontology

A common notation can make different systems easier to compare, but writing

[
H(q,p)
]

for two domains does not prove that those domains have the same physical ontology.

UHF therefore distinguishes **formal reuse** from **physical identity**.

## 3.2 Established Hamiltonian domains

Classical mechanics supplies canonical examples such as

[
H(q,p)=rac{p^2}{2m}+V(q).
]

Quantum mechanics uses Hamiltonian operators,

[
ihbarpartial_t|psiangle=hat H|psiangle.
]

Classical field theory and general relativity also admit Hamiltonian formulations under appropriate constructions and constraints.

These are `standard_physics` within their assumptions.

## 3.3 Harmonic oscillators

Near a stable equilibrium, many physical systems can be approximated by quadratic dynamics. The harmonic oscillator is therefore widely useful.

That does not imply that any observed oscillation in markets, neural activity, or organizations is literally a physical harmonic oscillator. In those domains, oscillator language is an `engineering_analogy` unless a defensible model is specified and validated.

## 3.4 Classical coupling is not quantum entanglement

Two classical oscillators can be coupled through an interaction term, for example

[
H
=
H_1+H_2+rac{k}{2}(q_1-q_2)^2.
]

This produces correlated classical dynamics.

Quantum entanglement instead requires a quantum state that cannot be factorized into subsystem states. A classical interaction term alone does not establish entanglement.

This distinction is mandatory throughout UHF.

## 3.5 Markets

A market model may define a state from price, order flow, liquidity, volatility, inventory, or regime features.

A scalar objective or potential may then be constructed for inference or control.

Such a model is an `engineering_analogy` unless a true symplectic structure and canonical equations are independently justified.

Usefulness must be established empirically, not inferred from Hamiltonian terminology.

## 3.6 Biology and cognition

Biological systems obey established physics and thermodynamics at their physical level, but higher-level biological or cognitive variables are not automatically canonical coordinates.

A proposed "biological Hamiltonian" or "cognitive potential" is therefore a modeling hypothesis unless derived from a defined physical or mathematical model and supported by evidence.

## 3.7 Domain translation contract

A valid UHF domain mapping states:

- the state variables;
- the units or semantics of those variables;
- whether variables are canonical or merely features;
- the generator or update rule;
- hard constraints;
- soft objectives;
- observables;
- assumptions;
- classification;
- evidence status.

If any of these are omitted, the mapping is incomplete.

## 3.8 Implementation contract

Documentation examples must match the repository's actual public API.

If a code fragment is incomplete, conceptual, or depends on undefined helpers, it is pseudocode and must be labeled as such rather than advertised as runnable Python.

Executable examples belong under tested examples or tests and must run in CI.

## 3.9 Cross-domain conclusion

The defensible UHF claim is not that the same physical law literally governs markets, cognition, software, and mechanics.

It is:

> A common state/operator/constraint/evidence vocabulary can support disciplined comparison and engineering reuse across domains, while preserving the distinction between exact physics, analogy, and hypothesis.
