# Book of Mopati — Chapter 15: Empirical Validation and Evidence

> **Classification:** engineering_analogy, empirically_validated  
> **Evidence:** The validation protocol itself is an engineering specification. Individual domain claims are empirically validated only when their evidence packages satisfy the protocol.  
> **Certification scope:** Makes empirical claims falsifiable and allows scientific assumptions to be revised in response to evidence while protecting governance boundaries from accidental optimization.

## 15.1 Validation is external to the claim

A model produces predictions, classifications, actions, or other outputs.

An empirical system provides observations.

Validation compares the two under a declared protocol.

A successful software run is not automatically validation of the physical or market claim encoded by the software.

## 15.2 Evidence can revise scientific models

An earlier version of this chapter stated that empirical outcomes could never affect the framework's axioms.

That is too strong for science.

Scientific assumptions and models must remain revisable when evidence contradicts them.

What should remain protected from accidental empirical feedback are governance invariants such as authorization boundaries, evidence immutability rules, or safety constraints—unless an authorized governance change process deliberately revises them.

Therefore:

- scientific hypotheses are falsifiable and revisable;
- engineering parameters may be updated under controlled procedures;
- governance invariants require explicit authority to change.

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

Without these fields, the claim is not ready for empirically_validated status.

## 15.4 Trading protocol

A trading validation must include at least:

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
- random or naive policy where appropriate;
- an existing production baseline if available.

### Reproducibility

Record exact data identity, code commit, parameters, random seeds where relevant, and deterministic evidence artifacts.

## 15.5 Worked examples must be labeled correctly

Synthetic examples may explain the evidence schema.

They must use labels such as:

- illustrative;
- synthetic;
- pseudocode;
- example-only.

Synthetic Sharpe ratios, win rates, or drawdowns must never appear as measured strategy performance.

## 15.6 Valid JSON

Artifacts advertised as JSON must parse as JSON.

Comments such as

[
	ext{// comment}
]

are invalid in standard JSON and must not appear in executable JSON examples.

Explanatory comments belong outside the JSON code block.

## 15.7 Failure taxonomy

A useful validation system distinguishes:

### Refusal

The candidate violated a pre-execution invariant.

### Failed hypothesis

The candidate was admissible but empirical performance did not satisfy the declared criterion.

### Measurement anomaly

The measurement infrastructure failed or produced unusable evidence.

### Implementation defect

The code failed to implement the declared model or protocol.

These outcomes have different meanings and should not be collapsed into one generic failure state.

## 15.8 Example evidence object

The following is valid illustrative JSON:

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

## 15.9 Promotion to empirically validated

A claim changes classification only after the evidence package exists and the validation gate passes.

The appropriate transition is:

[
	ext{research or engineering claim}
+
	ext{reproducible evidence}
ightarrow
	ext{empirically validated claim within stated scope}.
]

Validation is always scoped.

It does not prove a model universally true.

## 15.10 Book certification

The Book of Mopati may be truth-certified only when:

1. all chapters declare their classification and evidence boundary;
2. mathematical statements are internally consistent;
3. physical claims distinguish established theory from hypothesis;
4. advertised executable code is executed in CI;
5. pseudocode is labeled as pseudocode;
6. empirical claims point to reproducible evidence;
7. implementation names and APIs match the repository;
8. navigation and chapter counts are generated from one canonical manifest;
9. claim-language validation passes;
10. the documentation, implementation, and tests agree.

That is the final truth contract for the Book.
