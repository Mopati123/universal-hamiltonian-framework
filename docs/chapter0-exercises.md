# Chapter 0 Exercises — Truth-Aligned Edition

These exercises test the distinctions that the Book of Mopati now treats as foundational.

## Exercise 1 — Hamiltonian conservation

Consider

[
H(q,p)=rac{p^2}{2m}+rac{kq^2}{2}.
]

Using Hamilton's equations, show that for time-independent (H),

[
rac{dH}{dt}=0.
]

### Solution

Hamilton's equations give

[
dot q=rac{p}{m},
qquad
dot p=-kq.
]

Then

[
rac{dH}{dt}
=
rac{partial H}{partial q}dot q
+
rac{partial H}{partial p}dot p
=
(kq)rac{p}{m}
+
rac{p}{m}(-kq)
=0.
]

The oscillator moves along a constant-energy curve. It does not minimize (H).

---

## Exercise 2 — Gradient flow

Let

[
J(x)=rac12x^2
]

and define

[
dot x=-rac{dJ}{dx}=-x.
]

Show that (J) decreases.

### Solution

[
rac{dJ}{dt}
=
rac{dJ}{dx}dot x
=
x(-x)
=
-x^2
le 0.
]

This is objective minimization. It is a gradient flow, not canonical Hamiltonian flow.

---

## Exercise 3 — Dissipation

A damped oscillator satisfies

[
mddot q+bdot q+kq=0
]

with (b>0).

For the mechanical energy

[
E=rac12mdot q^2+rac12kq^2,
]

show that

[
rac{dE}{dt}=-bdot q^2le0.
]

### Solution

Differentiate:

[
rac{dE}{dt}
=
mdot qddot q+kqdot q
=
dot q(mddot q+kq).
]

Using the equation of motion,

[
mddot q+kq=-bdot q,
]

so

[
rac{dE}{dt}=-bdot q^2le0.
]

The decrease comes from dissipation.

---

## Exercise 4 — Stationary action

Why is “stationary action” more precise than “nature always minimizes action”?

### Solution

The variational principle requires

[
delta S=0.
]

A stationary point may be a local minimum, maximum, or saddle point depending on the system and boundary conditions. “Least action” is historical terminology, but minimization is not the universal mathematical statement.

---

## Exercise 5 — Classical coupling versus entanglement

Consider two classical oscillators coupled by

[
H
=
H_1+H_2+rac{k_c}{2}(q_1-q_2)^2.
]

Does the coupling term prove quantum entanglement?

### Solution

No. It produces interacting classical dynamics and can create classical correlations and normal modes.

Quantum entanglement is defined for quantum states. For a bipartite pure state, entanglement requires

[
|Psiangle_{AB}

eq
|psiangle_Aotimes|phiangle_B.
]

Classical coupling and quantum entanglement are different concepts.

---

## Exercise 6 — Engineering analogy

Suppose a software project defines

[
J
=
10N_{	ext{failed-tests}}
+
2N_{	ext{cycles}}
+
0.1N_{	ext{warnings}}.
]

Is (J) a physical Hamiltonian?

### Solution

No.

It is a designer-defined engineering objective. Its coefficients express priorities selected by the designer. It may be optimized, but Hamiltonian terminology is only an analogy unless a genuine canonical structure is separately established.

---

## Exercise 7 — Hard constraints and soft scores

A trading candidate has an excellent expected-return score but violates a maximum-position invariant.

Should it be selected?

### Solution

No.

Hard admissibility is evaluated before soft optimization. If (mathcal A) is the lawful action set, selection has the form

[
a^starinargmin_{ainmathcal A}J(a).
]

An inadmissible candidate is refused regardless of its score.

---

## Exercise 8 — Future data and retrocausality

A model uses tomorrow's closing price as an input when predicting today's trade.

Does strong backtest performance demonstrate retrocausal prediction?

### Solution

No.

It demonstrates information leakage. The model had access to future information in its input.

A valid trading experiment must restrict features to information available at decision time.

---

## Exercise 9 — Consciousness proxy

A program computes

[
C=rac{	ext{sum of pairwise coupling weights}}{	ext{number of nodes}}.
]

Can the program call (C) IIT (Phi)?

### Solution

Not merely from that definition.

IIT uses specific formal definitions of integrated information. A custom coupling statistic should be named according to what it computes, such as an integration proxy, unless it actually implements the relevant IIT formalism.

---

## Exercise 10 — Chaos and cryptography

A deterministic chaotic map has sensitive dependence on initial conditions.

Does this prove cryptographic security?

### Solution

No.

Cryptographic security requires a threat model and properties such as pseudorandomness, indistinguishability, one-wayness, collision resistance, or other formally defined guarantees appropriate to the construction.

Chaotic sensitivity alone proves none of them.

---

## Exercise 11 — Trading evidence

A strategy reports Sharpe (1.8) on the same data used to choose its parameters. No costs or baseline are supplied.

May the Book call the strategy empirically validated?

### Solution

No.

At minimum the claim still needs:

- out-of-sample testing;
- leakage controls;
- realistic transaction costs;
- baselines;
- reproducible data or fixtures;
- disclosed parameter selection.

The in-sample metric is insufficient.

---

## Exercise 12 — Symplectic integrator

Does using a symplectic integrator guarantee exact conservation of numerical energy at every step?

### Solution

No.

Symplectic integrators preserve a discrete symplectic structure and often show good long-horizon energy behavior, but the computed energy generally oscillates around the true value rather than remaining exactly constant. Stability also depends on the problem and step size.

---

## Exercise 13 — Scientific revision

An experiment repeatedly contradicts a research hypothesis while the measurements and implementation survive independent checks.

Should the scientific hypothesis be write-protected from revision?

### Solution

No.

Scientific models must remain falsifiable and revisable.

Governance controls such as authorization or evidence-integrity rules may require explicit authority to change, but empirical hypotheses should respond to evidence.

---

## Exercise 14 — Claim classification

Classify each statement.

1. “For an autonomous canonical Hamiltonian system, (dH/dt=0).”
2. “We model liquidity concentration using a potential-like penalty.”
3. “A two-boundary temporal model may produce testable retrocausal predictions.”
4. “Our strategy improved net Sharpe out of sample after costs relative to declared baselines, with reproducible evidence.”

### Solution

1. standard_physics.
2. engineering_analogy.
3. research_hypothesis.
4. potentially empirically_validated, but only if the referenced evidence actually satisfies the protocol.

---

## Exercise 15 — Certification invariant

Why is a disclaimer at the top of a chapter insufficient if the chapter body later says the speculative claim has been proven?

### Solution

Because classification is semantic, not cosmetic.

The body and metadata must agree. A truth-certification gate must reject contradictions inside the chapter rather than treating a banner as permission to overclaim.

---

## Exercise 16 — Final synthesis

Complete the statement:

> UHF should use Hamiltonian mechanics ________, Hamiltonian-inspired engineering abstractions ________, research hypotheses ________, and empirical claims ________.

### Solution

A truth-aligned completion is:

> UHF should use Hamiltonian mechanics **where its mathematical structure applies**, Hamiltonian-inspired engineering abstractions **where their construction is explicit**, research hypotheses **where uncertainty and falsifiability are preserved**, and empirical claims **only where reproducible evidence supports their stated scope**.
