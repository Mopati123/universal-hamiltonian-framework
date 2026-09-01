# Book of Mopati — Chapter 14: Governed Executability

> **Classification:** engineering_analogy  
> **Evidence:** The chapter describes architectural properties that are valid only when enforced by implementation and tests.  
> **Certification scope:** Replaces an over-broad “Invariant Preservation Theorem” with explicit conditional safety properties.

## 14.1 From proposal to governed execution

A system becomes governable when proposal generation is separated from authority to execute.

The canonical sequence is:

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
	ext{evidence}
ightarrow
	ext{reconcile}.
]

No generative component is sovereign by default.

## 14.2 Schemas as structural constraints

Schemas can define structural admissibility:

- required fields;
- types;
- ranges;
- relationships;
- identifiers.

Schema validity is necessary for structured execution, but a schema alone does not prove semantic correctness, safety, or truth.

## 14.3 Hard invariants

A hard invariant must be enforced by code at the relevant boundary.

Examples include:

- authorization required before execution;
- forbidden state transitions;
- risk limits;
- immutable evidence requirements;
- deterministic reconciliation conditions.

An invariant stated only in documentation is not enforced.

## 14.4 Refusal

Refusal is a valid execution outcome.

When a candidate violates an invariant, the correct transition may be:

[
	ext{candidate}
ightarrow
	ext{refusal evidence}
]

with no execution effect.

Refusal must be explicit and testable.

## 14.5 Non-sovereign agents

An agent may observe, reason, and propose while lacking authority to mutate canonical state.

This separation reduces the blast radius of model errors.

It does not make the overall system automatically safe; the authority boundary, tool permissions, effect handlers, and tests must actually enforce the separation.

## 14.6 Conditional invariant-preservation property

The earlier chapter called its architectural claim an “Invariant Preservation Theorem.”

That wording was too strong.

A defensible conditional property is:

> If every state-changing path is mediated by complete invariant checks, authority checks cannot be bypassed, effect handlers faithfully enforce decisions, and the implementation is correct, then transitions that violate the encoded invariants are refused.

This is an architectural safety property with proof obligations.

It is not a theorem about arbitrary agents or arbitrary software.

## 14.7 Proof obligations

For an invariant (I), certification should identify:

- every state-changing entry point;
- the enforcement function;
- tests for allowed transitions;
- tests for forbidden transitions;
- bypass analysis;
- evidence emitted on refusal;
- reconciliation behavior;
- rollback behavior where applicable.

## 14.8 Audit evidence

Evidence should make execution reconstructable:

- input identity;
- configuration;
- proposal;
- invariant results;
- authorization;
- selected action;
- effects;
- output;
- hashes;
- reconciliation status.

Evidence increases auditability; it does not replace correct implementation.

## 14.9 Conclusion

The durable result of Chapter 14 is:

> Governed execution is achieved by explicit separation of proposal, admissibility, authority, effects, evidence, and reconciliation, with each claimed invariant backed by implementation and tests.
