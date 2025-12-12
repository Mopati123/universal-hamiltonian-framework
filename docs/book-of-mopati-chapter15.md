# Book of Mopati - Chapter 15: Phase 2 — Real Market Data Migration & Axiomatic Discovery

## Overview

This chapter documents the Phase 2 migration and validation work that unified real market data ingestion, canonical representation, and Hamiltonian validation across the framework. It explains the practical engineering fixes, their theoretical interpretation, and how they reveal irreducible axiomatic structure (first-order), symplectic invariants (second-order), and the emergent metadata and gauge structure (third-order).

---

## I. What We Changed — Practical Summary

- Migrated data pipeline from Pandas to Polars for faster, memory-efficient DataFrame handling across the framework.
- Handled yfinance's newer MultiIndex column format by flattening (Price, Ticker) -> Price to restore the canonical naming convention.
- Added explicit dtype conversions to float64 for numeric columns before performing logarithmic and volatility computations.
- Updated examples and validation scripts: `examples/phase2_enhanced_framework.py`, `examples/phase2_advanced_calibration.py` to use Polars and to robustly extract numeric price arrays.
- Replaced unicode emoji in CLI output with ASCII-safe warnings to avoid encoding errors in cross-platform terminals.
- Ran benchmarks and tests to verify that the canonical Hamiltonian machinery yields consistent results across the new pipeline.

**Why these changes matter**: The codebase now reliably produces numeric, canonical price arrays for the Hamiltonian pipeline so computations (log returns, calibrations, simulations) are mathematically sound and numerically stable.

---

## II. First-Order Principles: Irreducible Canonical Axioms

In Phase 2 we discovered and enforced several foundational axioms that must be true for any implementation:

### Axiom 15.1: Data-Phase-Space Canonical Pairing
Raw inputs and typed representations form conjugate variables: `(raw_data, typed_data)`.
- Template: `Prices (q)` and `Type/Scale (p)`.
- Enforced by: Explicit dtype conversion of price columns and flattening of multi-index columns.

### Axiom 15.2: Representation as a Gauge Choice
Data format (Pandas vs Polars) is a gauge choice; physics (Hamiltonian) should be gauge invariant.
- Operationally: Transformations must preserve the information required to compute the Hamiltonian (prices, returns, realized volatility).

### Axiom 15.3: Canonical Measurement Consistency
Log-transforms and derivative computations require numeric (float64) fields—these are canonical basis selections.
- `np.log`, `np.diff`, and statistics assume continuous coordinates — cast to float64 to ensure conjugate variables are well-defined.

**Why this is irreducible**: Without these constraints, the Hamiltonian generator is ill-defined (non-numeric arguments), so time evolution and parameter estimation are invalid.

---

## III. Second-Order Principles: Symplectic Invariants & Conjugate Evolution

Second-order principles capture the invariants we have to maintain:

### Principle 15.1: Symplectic Preservation
Canonical transformations done by our pipeline (parsing/flattening, dtype casting) must preserve the symplectic structure, i.e., $ q, p  = 1$ across representation changes.
- Checks: Unit tests verify returns & volatility derived from Polars = those from Pandas (within numerical tolerances).

### Principle 15.2: Liouville Invariance for Data Pipelines
Probability mass in the price-return phase space must be preserved under basis changes from Pandas → Polars.
- Evidence: Benchmarks and rolling-window backtests produce consistent realized vol and calibration results.

### Principle 15.3: Poisson Bracket & Observable Consistency
Poisson brackets formed from pipeline outputs (prices, flows) are numerically stable and consistent across domains once dtype gauge is fixed.
- Conjugate pairs shift from raw price to returns to meta-parameters during calibration but preserve canonical form.

---

## IV. Third-Order Principles: Metadata & Meta-Evolution

Third-order insights concern what the data pipeline reveals about the system and what it allows us to build:

### Meta-Principle 15.1: Implementation-Agnostic Hamiltonians
The framework's Hamiltonian structure is invariant under implementation details. Observations we made:
- Data ingest changes do not change the Hamiltonian form, only the representation.
- This enables multi-backend support and future optimizations without altering physics.

### Meta-Principle 15.2: Type Information as Hidden Symmetry
Type encoding (datetime vs numeric, integer vs float) is a hidden Z(1)-like symmetry that must be broken (gauge-fixing) before calculations.
- Gauge-fixing: dtype=float64 or `prices.astype(np.float64)`.

### Meta-Principle 15.3: Cross-domain ETO Coupling Parameters
From calibration runs we can now extract stable meta-parameters:
- Example: Realized vol and ETO (λ) rough empirical estimates per asset across the validation window.
- These become the domain-bridges used by Phase 3 to couple markets to other Hamiltonian domains.

**Operational metadata** collected during Phase 2**:
- Price ranges and realized volatility per asset
- Calibrated ETO λ values per asset (SPY: ~0.03, QQQ: ~0.04, IWM: ~0.011)
- MLE/LS calibration results (drift p0, noise amplitude) for exploratory use in Phase 3

---

## V. Practical Guidance for Phase 3 Integration

To carry Phase 2 insights forward into Phase 3 (multi-domain synthesis), follow these rules:

1. **Always fix the type gauge early**: Convert input columns to `float64` and ensure timestamps remain typed as datetimes.
2. **Flatten external MultiIndex columns** and maintain canonical names (Close, Open, High, Low, Volume). This preserves domain-linguistic invariants for the Hamiltonian.
3. **Record ETO & meta-parameters**: Persist Λ, realized vol, drift estimates per asset into canonical metadata JSON (`examples/tier3_validation_results.json`).
4. **Unit test all transformations**: For each backend (Pandas/Polars/Arrow), verify numeric equivalence for key derived observables (returns, volatility, RMSE).
5. **Preserve Liouville invariants** when coupling domains — do not allow representation conversions to leak information across the coupling boundary.

---

## VI. Appendix: Code Snippets (Canonical) — How To Convert Correctly

By convention we prefer Polars pipelines in Phase 3 with explicit typing:

```python
import polars as pl
import numpy as np

# Generic conversion to float
if isinstance(data.columns, pd.MultiIndex):
    data.columns = [c[0] for c in data.columns]
data = data.reset_index()
for col in data.columns:
    if col not in ['Date', 'Datetime']:
        try:
            data[col] = data[col].astype(np.float64)
        except Exception:
            pass

prices = np.asarray(data.select('Close').to_numpy().flatten(), dtype=np.float64)

# Compute returns and realized vol
returns = np.diff(np.log(prices))
realized_vol = np.std(returns) * np.sqrt(252)
```

---

## VII. Action Items & Checkpoints for Phase 3

- Persist Phase 2 metadata for each domain as a canonical JSON.
- Extend ETO calibration to multi-asset portfolios and simulated cross-domain coupling (econ ↔ neural ↔ blockchain).
- Add serialization of calibration results to a `examples/tier3_validation_results.json` file.

---

## VIII. Footnotes & Cross-References

- See `examples/phase2_enhanced_framework.py` and `examples/phase2_advanced_calibration.py` for working examples and exact calibrations.
- See `docs/BOOK_INDEX.md` for the canonical chapter index and navigational structure.

---

**End of Chapter 15: Phase 2 — Real Market Data Migration & Axiomatic Discovery**
