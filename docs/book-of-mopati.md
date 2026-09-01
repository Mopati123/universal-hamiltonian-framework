# Book of Mopati — Chapter 1: Axiomatic Foundation

> **Classification:** standard_physics, engineering_analogy, research_hypothesis  
> **Evidence:** Established Hamiltonian mechanics is separated from UHF modeling conventions and speculative extensions.  
> **Certification scope:** This chapter defines the vocabulary, optimization rules, and claim classes used by the rest of the book.

## 1.1 UHF as a modeling language

The Universal Hamiltonian Framework (UHF) is a common language for representing state, dynamics, objectives, interactions, constraints, authority, observables, and evidence.

It does **not** assume that every physical, informational, economic, biological, cognitive, or organizational system literally has canonical coordinates and momenta.

Every mapping must answer:

1. Is this established Hamiltonian physics?
2. Is this a Hamiltonian-inspired engineering construction?
3. Is this a research hypothesis that still requires proof or evidence?

## 1.2 Canonical evolution

For a genuine Hamiltonian system,

$$
\dot q_i
=
\frac{\partial H}{\partial p_i},
\qquad
\dot p_i
=
-\frac{\partial H}{\partial q_i}.
$$

**Where:**
- $q_i$ and $p_i$ are canonical coordinate–momentum pairs;
- $H$ is the Hamiltonian;
- the overdot means differentiation with respect to time.

If a proposed domain does not define the required canonical structure, these equations must not be asserted literally for that domain.

## 1.3 Hard constraints and soft objectives

Let $C(x)$ be a predicate that is true only when state $x$ satisfies every hard constraint. The admissible set is

$$
\mathcal A
=
\{x \mid C(x)=\mathrm{true}\}.
$$

Let $J(x)$ be a soft objective to be minimized. Governed optimization then has the form

$$
x^\star
\in
\operatorname*{arg\,min}_{x\in\mathcal A}
J(x).
$$

**Where:**
- $\mathcal A$ is the admissible region;
- $J(x)$ is the soft score or objective;
- $x^\star$ is an optimal admissible candidate, if one exists.

The order matters:

> **admissibility first, optimization second.**

A candidate that violates a hard invariant is refused even if it has an attractive soft score.

## 1.4 Four claim classes

### standard_physics

Use when the mathematical or physical structure is established within stated assumptions.

Examples include canonical Hamiltonian mechanics, the Schrödinger equation, symplectic geometry, and standard thermodynamics.

### engineering_analogy

Use when physical language is deliberately repurposed as a computational abstraction.

Examples include:
- a market "potential";
- a software "energy score";
- "collapse" as deterministic candidate selection.

The analogy may be useful without implying literal physical equivalence.

### research_hypothesis

Use for a formalizable proposal that is not yet established.

Examples include:
- a proposed cross-domain Hamiltonian;
- a retrocausal computational model;
- a consciousness-related mapping.

### empirically_validated

Use only when a scoped claim has reproducible evidence under an appropriate protocol.

For trading, that includes out-of-sample data, realistic costs, leakage controls, baselines, and reproducible evidence.

## 1.5 Cross-domain mapping rule

Similarity of notation is not proof of physical identity.

For example:
- price and order flow may be useful state features, but they are not automatically canonical conjugates;
- two coupled oscillators are not automatically quantum-entangled;
- a neural coupling score is not automatically IIT $\Phi$;
- information, energy, and consciousness are not interchangeable physical quantities.

## 1.6 Evidence-native execution

UHF separates proposal from execution and evidence:

~~~text
observe
  ↓
represent
  ↓
propose
  ↓
constrain
  ↓
authorize
  ↓
execute
  ↓
measure
  ↓
reconcile
~~~

This is a governance architecture, not a physical law.

A mathematically consistent model can still be empirically wrong. A useful analogy can remain nonphysical. A failed empirical hypothesis must be revised or rejected.

## 1.7 Foundational statement

> Use Hamiltonian mechanics exactly where its mathematical structure applies; use Hamiltonian-inspired abstractions explicitly where they are engineering choices; label speculative extensions as hypotheses; and promote empirical claims only when reproducible evidence supports their stated scope.
