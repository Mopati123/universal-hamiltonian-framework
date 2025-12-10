# Benchmarks
## Reproducible Performance Validation

This directory contains reproducible benchmarks to validate the performance claims in `TECH_STACK.md`.

---

## 🎯 **Purpose**

Provide empirical evidence for:
- Polars lazy execution speedup vs Pandas
- Cython compilation speedup vs Python
- Overall stack performance claims

**Philosophy**: "Science without measurement is philosophy. We choose both."

---

## ⚡ **Quick Start**

```bash
# Install dependencies
pip install -r ../quantum_trading/requirements.txt

# Run all benchmarks
python harness.py --all

# Run specific benchmarks
python harness.py --polars-vs-pandas
python harness.py --cython-speedup
```

---

## 📊 **What We Measure**

### **1. Polars vs Pandas**

**Workflow:**
1. Load 1M rows of market data
2. Filter by price > 450
3. GroupBy symbol and aggregate

**Hypothesis**: Polars lazy execution is ~5x faster

**Command:**
```bash
python harness.py --polars-vs-pandas --n-rows 1000000
```

---

### **2. Cython vs Python**

**Workflow:**
1. Calculate Hamiltonian energies for 1M market states
2. Compare pure Python loop vs Cython compiled

**Hypothesis**: Cython is ~30-50x faster

**Command:**
```bash
python harness.py --cython-speedup --n-rows 1000000
```

**Prerequisites:**
```bash
# Compile Cython module first
cd ../quantum_trading
python setup.py build_ext --inplace
```

---

### **3. NumPy Vectorized (Reference)**

**Workflow:**
1. Calculate energies using NumPy vectorization
2. Baseline for what vectorization alone achieves

**Command:**
```bash
python harness.py --numpy-vectorized
```

---

## 📁 **Results**

All results saved to `results/` with timestamps:
```
results/
├── benchmark_results_1733812345.json
├── benchmark_results_1733812890.json
└── ...
```

**Format:**
```json
{
  "test": "polars_vs_pandas",
  "n_rows": 1000000,
  "pandas_time_avg": 2.8456,
  "polars_time_avg": 0.5234,
  "speedup": 5.44,
  "timestamp": "2025-12-10T08:30:00",
  "system_info": {...}
}
```

---

## 🔬 **Reproducibility**

### **System Info Recorded:**
- Platform (OS, architecture)
- Python version
- Library versions (numpy, pandas, polars)
- Processor type

### **To Reproduce:**
1. Clone repo
2. Install exact versions: `pip install -r requirements.txt`
3. Run: `python harness.py --all`
4. Compare your results to `results/` directory

---

## 📈 **Current Results**

**Last run**: December 10, 2025

| Test | Claimed | Measured | Status |
|------|---------|----------|--------|
| Polars vs Pandas | 5.4x | TBD | ⏳ Pending |
| Cython speedup | 30-50x | TBD | ⏳ Pending |
| Combined stack | 37.7x | TBD | ⏳ Pending |

**Note**: Run `python harness.py --all` to populate actual measurements.

---

## 🎓 **Validation Philosophy**

This follows the framework's own principles:

**Three-Tier Logic:**
1. **First Order**: Measure actual performance
2. **Second Order**: Compare to claims (maintain honesty)
3. **Third Order**: Evolve claims based on data

**Self-Evolution:**
1. **Detect**: Claims exceed evidence
2. **Measure**: Build benchmark harness
3. **Update**: Align claims with reality
4. **Iterate**: Continuous validation

---

## 🛠️ **Adding New Benchmarks**

```python
def benchmark_your_test(self, n=1_000_000):
    """Your benchmark description"""
    
    # Generate test data
    data = ...
    
    # Measure baseline
    t0 = time.perf_counter()
    result_baseline = baseline_implementation(data)
    baseline_time = time.perf_counter() - t0
    
    # Measure optimized
    t0 = time.perf_counter()
    result_optimized = optimized_implementation(data)
    optimized_time = time.perf_counter() - t0
    
    speedup = baseline_time / optimized_time
    
    return {
        'test': 'your_test',
        'n': n,
        'baseline_time': baseline_time,
        'optimized_time': optimized_time,
        'speedup': speedup,
        'timestamp': datetime.now().isoformat()
    }
```

---

## 📖 **References**

- Main docs: `../TECH_STACK.md`
- Validation status: `../VALIDATION_STATUS.md`
- Quantum trading code: `../quantum_trading/`

---

_"Measurement is the bridge between philosophy and truth."_ ✨
