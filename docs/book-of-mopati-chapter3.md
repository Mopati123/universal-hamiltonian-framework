# Book of Mopati — Chapter 3: Domain Mappings

> **Classification:** standard_physics, engineering_analogy, research_hypothesis  
> **Evidence:** Physical Hamiltonians are standard where stated; nonphysical mappings are explicit constructions.  
> **Certification scope:** Defines when cross-domain reuse is structural, analogous, or speculative.

## 3.1 One notation does not imply one ontology

Writing

$$
H(q,p)
$$

in two different domains does not prove that the domains have the same physical ontology.

The notation says only that we have defined some function $H$ of variables $q$ and $p$. Whether $q$ and $p$ are genuinely canonical variables must be established separately.

## 3.2 Classical Hamiltonian example

For a particle of mass $m$ moving in a potential $V(q)$,

$$
H(q,p)
=
\frac{p^2}{2m}
+
V(q).
$$

**Where:**
- $q$ is position;
- $p$ is canonical momentum;
- $m$ is mass;
- $V(q)$ is potential energy.

This is standard classical mechanics.

## 3.3 Quantum Hamiltonian example

Quantum time evolution satisfies the Schrödinger equation

$$
i\hbar
\frac{\partial}{\partial t}
|\psi(t)\rangle
=
\hat H |\psi(t)\rangle.
$$

Here $\hat H$ is an operator acting on a quantum state. This is not the same mathematical object as an arbitrary scalar objective function in software or finance.

## 3.4 Coupled classical oscillators

Two classical oscillators can interact through

$$
H
=
H_1
+
H_2
+
\frac{k}{2}(q_1-q_2)^2.
$$

**Where:**
- $H_1$ and $H_2$ are the uncoupled subsystem Hamiltonians;
- $k$ is a classical coupling constant;
- $q_1$ and $q_2$ are oscillator coordinates.

This interaction can create correlated classical motion, synchronization, and normal modes.

It does **not** by itself create quantum entanglement.

## 3.5 Markets

A market model may use price, order flow, liquidity, volatility, inventory, and regime variables as features.

A potential-like or Hamiltonian-inspired score can then be constructed for inference or control.

Such a construction is an **engineering analogy** unless the model defines and justifies a true symplectic structure and canonical equations.

## 3.6 Biology and cognition

Biological systems obey established physics at their physical level, but high-level variables such as "attention," "cognitive load," or "integration" are not automatically canonical coordinates.

A proposed biological or cognitive Hamiltonian must therefore specify:
- state variables;
- units or semantics;
- equations of motion;
- assumptions;
- observables;
- falsifiable predictions.

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

## 3.8 Implementation contract

Documentation examples must match the repository's actual public API.

Incomplete or conceptual code is pseudocode and must be labeled as such. Executable examples belong under tests or tested examples and must run in CI.

## 3.9 Conclusion

> A common state/operator/constraint/evidence vocabulary can support disciplined comparison and engineering reuse across domains, while preserving the distinction between exact physics, analogy, and hypothesis.
