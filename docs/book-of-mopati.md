# Book of Mopati — Chapter 1: Axiomatic Foundation

> **Classification:** `standard_physics`, `engineering_analogy`, `research_hypothesis`  
> **Evidence:** Established Hamiltonian mechanics is separated from UHF modeling conventions and speculative extensions.  
> **Certification scope:** This chapter defines the vocabulary and claim rules used by the rest of the book.

## 1.1 The Universal Hamiltonian Framework as a modeling language

UHF is a framework for representing dynamics, objectives, interactions, constraints, and evidence using a common vocabulary inspired in part by analytical mechanics.

It does **not** assume that every physical, informational, economic, biological, cognitive, or organizational system literally possesses canonical coordinates and momenta.

Instead, every mapping must answer three questions:

1. Is this an established Hamiltonian model?
2. Is this an engineering construction using Hamiltonian-inspired notation?
3. Is this a research hypothesis that still requires theoretical or empirical support?

## 1.2 Three mathematical pillars

### Canonical state

For a genuine Hamiltonian model, the state is represented by canonical variables ((q,p)) on a symplectic phase space.

For an engineering model, a state vector may be introduced for computational convenience, but it must not be called canonical unless the required structure is actually defined.

### Generator of evolution

For a Hamiltonian system,

[
dot q_i=rac{partial H}{partial p_i},
qquad
dot p_i=-rac{partial H}{partial q_i}.
]

For optimization, UHF uses an objective such as (J(x)) and an optimizer appropriate to the problem. The objective is not automatically a physical energy.

### Constraints and invariants

A hard invariant defines an admissibility boundary. A soft score ranks admissible candidates.

This distinction is constitutional throughout UHF:

[
	ext{admissibility before optimization}.
]

A candidate that violates a hard invariant is refused; it is not rescued by a favorable soft score.

## 1.3 The four claim classes

Every major model or claim in this repository must use one of four labels.

### `standard_physics`

Use when the relevant mathematical/physical structure is established within its stated assumptions.

Examples include canonical mechanics, the Schrödinger equation, symplectic geometry, and standard thermodynamic results.

### `engineering_analogy`

Use when physical language is deliberately repurposed as a computational abstraction.

Examples include a "market potential," a software "energy score," or "collapse" as deterministic candidate selection.

The analogy may be useful without implying literal physical equivalence.

### `research_hypothesis`

Use for falsifiable or formalizable proposals that are not established.

Examples include proposed cross-domain Hamiltonians, retrocausal computational models, or consciousness-related mappings.

### `empirically_validated`

Use only when a clearly stated claim has reproducible evidence under an appropriate protocol.

For market claims this requires, at minimum, out-of-sample data, realistic transaction costs, leakage controls, baselines, and reproducible data or fixtures.

## 1.4 Hard invariants versus soft scores

Suppose (C(x)) is a set of hard constraints and (J(x)) is a soft objective.

UHF treats the lawful region as

[
mathcal A={x:C(x)=	ext{true}}.
]

Optimization occurs only inside (mathcal A):

[
x^starinargmin_{xinmathcal A}J(x).
]

This is not Hamiltonian mechanics unless the model independently satisfies the Hamiltonian conditions. It is a governed optimization architecture.

## 1.5 Cross-domain mapping rule

A cross-domain mapping is valid only to the extent that the mapped quantities and equations preserve the properties being claimed.

Similarity of notation is not enough.

For example:

- price and order flow can be useful state features, but they are not automatically canonical conjugates;
- two coupled oscillators are not automatically quantum-entangled;
- a neural coupling score is not automatically IIT (Phi);
- information has physical processing costs, but information, energy, and consciousness are not interchangeable physical quantities.

## 1.6 Evidence-native interpretation

UHF separates proposal from evidence:

[
	ext{observe}
ightarrow
	ext{represent}
ightarrow
	ext{propose}
ightarrow
	ext{constrain}
ightarrow
	ext{authorize}
ightarrow
	ext{execute}
ightarrow
	ext{measure}
ightarrow
	ext{reconcile}.
]

A model can be mathematically valid and empirically poor. A useful engineering analogy can remain nonphysical. A failed empirical hypothesis must be revised or rejected rather than protected by the framework's terminology.

## 1.7 Foundational statement

The defensible UHF principle is:

> Use Hamiltonian mechanics exactly where its structure applies; use Hamiltonian-inspired abstractions explicitly where they are engineering choices; label speculative extensions as hypotheses; and promote empirical claims only when reproducible evidence supports them.

This principle replaces blanket statements that everything is literally Hamiltonian.
