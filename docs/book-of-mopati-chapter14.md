# Book of Mopati — Chapter 14: Governed Executability

> **Classification:** engineering_analogy  
> **Evidence:** The chapter describes architectural properties that are valid only when enforced by implementation and tests.  
> **Certification scope:** Replaces an over-broad invariant theorem with explicit, readable conditional safety properties.

## 14.1 Governed execution sequence

A system becomes governable when proposal generation is separated from authority to execute.

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
evidence
  ↓
reconcile
~~~

This diagram is an execution architecture, not a physical equation.

## 14.2 Hard invariants

Let $I_k(x,a)$ be the $k$th invariant check for state $x$ and proposed action $a$.

The admissible action set can be written as

$$
\mathcal A(x)
=
\left\{
a
\;\middle|\;
I_k(x,a)=\mathrm{true}
\text{ for every } k
\right\}.
$$

**Meaning:** an action is admissible only if every required hard invariant passes.

A soft score cannot override this condition.

## 14.3 Authority

Let $A_{\mathrm{auth}}(x,a)$ be an authorization predicate.

Execution requires

$$
a\in\mathcal A(x)
\quad\text{and}\quad
A_{\mathrm{auth}}(x,a)=\mathrm{true}.
$$

Both conditions are necessary.

A proposal can therefore be mathematically attractive and still be refused because authority is missing.

## 14.4 Refusal

A refusal is a valid execution result:

~~~text
candidate
   ↓
invariant or authority failure
   ↓
refusal evidence
   ↓
no external effect
~~~

Refusal must be explicit, testable, and auditable.

## 14.5 Non-sovereign agents

An agent may observe, reason, and propose while lacking the ability to mutate canonical state.

That separation reduces blast radius but does not guarantee safety unless the enforcement boundaries themselves are correct and non-bypassable.

## 14.6 Conditional invariant-preservation property

A precise claim is:

> If every state-changing path is mediated by complete invariant checks, authority checks cannot be bypassed, effect handlers faithfully enforce decisions, and the implementation is correct, then transitions that violate the encoded invariants are refused.

This is a conditional architectural safety property.

It is not a theorem about arbitrary software.

## 14.7 Proof obligations

For each invariant, certification should identify:
- state-changing entry points;
- enforcement code;
- allowed-transition tests;
- forbidden-transition tests;
- bypass analysis;
- refusal evidence;
- reconciliation behavior;
- rollback behavior where applicable.

## 14.8 Evidence model

A reconstructable evidence record should include:
- input identity;
- configuration;
- proposal;
- invariant results;
- authorization result;
- selected action;
- effects;
- output;
- hashes;
- reconciliation status.

## 14.9 Conclusion

> Governed execution is achieved by explicit separation of proposal, admissibility, authority, effects, evidence, and reconciliation, with every claimed invariant backed by implementation and tests.
