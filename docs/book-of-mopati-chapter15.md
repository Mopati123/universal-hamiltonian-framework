# Book of Mopati — Chapter 15: Empirical Validation and Evidence

> **Classification:** engineering_analogy, empirically_validated  
> **Evidence:** The validation protocol itself is an engineering specification. Individual domain claims become empirically validated only when their evidence packages satisfy the protocol.  
> **Certification scope:** Makes empirical claims falsifiable, keeps JSON examples valid, and explains precisely how evidence changes claim status.

## 15.1 Validation is external to the claim

A model produces predictions, classifications, actions, or other outputs.

An empirical system provides observations.

Validation compares model output with observed evidence under a declared protocol.

A successful software run is not automatically validation of the external scientific or market claim represented by that software.

## 15.2 Evidence can revise scientific models

Scientific assumptions and hypotheses must remain revisable when evidence contradicts them.

Governance invariants are different: authorization boundaries or evidence-integrity rules require an explicit authorized governance process to change.

Therefore:
- scientific hypotheses are falsifiable and revisable;
- engineering parameters may be updated through controlled procedures;
- governance invariants require explicit authority to modify.

## 15.3 Claim record

Every major empirical claim should identify:
- claim ID;
- classification;
- assumptions;
- dataset or experimental source;
- protocol;
- metrics;
- baselines;
- uncertainty;
- result;
- evidence artifact;
- code commit;
- configuration hash;
- limitations.

Without those fields, the claim is not ready for empirically validated status.

## 15.4 Trading protocol

Trading validation requires at least:

### Data separation

Chronological train, validation, and test partitions.

The final test set must not influence model selection.

### Leakage controls

Features, labels, preprocessing, normalization, and parameter selection must use only information available at the relevant historical time.

### Costs

Include relevant commissions, bid–ask spread, slippage, financing, borrow costs, and latency assumptions.

### Baselines

Compare against meaningful alternatives such as:
- buy-and-hold where appropriate;
- simple momentum;
- simple mean reversion;
- naive or random policies where appropriate;
- an existing baseline system where available.

### Reproducibility

Record exact data identity, code commit, parameters, random seeds where relevant, and deterministic evidence artifacts.

## 15.5 Metric examples

If returns are $r_1,\ldots,r_n$, the sample mean is

$$
\bar r
=
\frac{1}{n}
\sum_{i=1}^{n}
r_i.
$$

A Sharpe-like ratio may be estimated as

$$
S
=
\frac{\bar r-r_f}{s_r},
$$

where:
- $r_f$ is the return of the chosen risk-free benchmark over the same period convention;
- $s_r$ is the sample standard deviation of returns.

Any annualization convention must be stated explicitly.

A metric is not evidence by itself; the data-generation and validation protocol matter.

## 15.6 Valid JSON

Artifacts advertised as JSON must parse as standard JSON.

JavaScript-style comments beginning with two slashes are invalid inside standard JSON and therefore belong outside the JSON block.

The following is a valid illustrative example:

~~~json
{
  "claim_id": "example_market_claim",
  "classification": "engineering_analogy",
  "status": "illustrative_only",
  "dataset": {
    "identity": "synthetic_fixture_v1",
    "out_of_sample": true
  },
  "controls": {
    "transaction_costs": true,
    "leakage_checks": true,
    "baselines": true
  },
  "result": null,
  "evidence_hash": null
}
~~~

No performance result is asserted.

## 15.7 Failure taxonomy

### Refusal

The candidate violated a pre-execution invariant.

### Failed hypothesis

The candidate was admissible, but empirical performance did not satisfy the declared criterion.

### Measurement anomaly

The measurement infrastructure failed or produced unusable evidence.

### Implementation defect

The code failed to implement the declared model or protocol.

These outcomes have different meanings and must not be collapsed into one generic failure state.

## 15.8 Promotion to empirically validated

The claim-state transition is

~~~text
research hypothesis or engineering claim
              +
      reproducible evidence
              ↓
empirically validated claim
within the stated scope
~~~

This is a governance and evidence transition, not a physical equation.

Validation is always scoped. It does not prove a model universally true.

## 15.9 Book certification

The Book of Mopati may be truth-certified only when:
1. all chapters declare classification and evidence boundaries;
2. mathematical statements are internally consistent;
3. equations render correctly and their symbols are understandable;
4. physical claims distinguish established theory from hypothesis;
5. advertised executable code runs in CI;
6. pseudocode is labeled as pseudocode;
7. empirical claims point to reproducible evidence;
8. implementation names and APIs match the repository;
9. navigation and chapter counts derive from one canonical manifest;
10. claim-language validation passes;
11. documentation, implementation, tests, and evidence agree.

## 15.10 Final principle

> Certification means that the Book states what is known, what is engineered, what is hypothesized, and what has been empirically demonstrated without allowing notation or presentation defects to blur those boundaries.
