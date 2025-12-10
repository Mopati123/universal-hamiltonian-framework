"""
Reproducible Benchmark Harness

Validates stack performance claims with controlled measurements.
Provides empirical evidence for Polars+Cython+Mojo stack superiority.

Usage:
    python benchmarks/harness.py --all
    python benchmarks/harness.py --polars-vs-pandas
    python benchmarks/harness.py --cython-speedup
"""

import time
import numpy as np
import pandas as pd
import polars as pl
from pathlib import Path
import json
import argparse
from datetime import datetime
import platform
import sys


class BenchmarkHarness:
    """
    Reproducible benchmark suite for quantum trading stack
    
    Measures actual performance to validate claims in TECH_STACK.md
    """
    
    def __init__(self, results_dir='results'):
        self.results_dir = Path(__file__).parent / results_dir
        self.results_dir.mkdir(exist_ok=True, parents=True)
        
        # Record system info
        self.system_info = {
            'platform': platform.platform(),
            'processor': platform.processor(),
            'python_version': sys.version,
            'numpy_version': np.__version__,
            'pandas_version': pd.__version__,
            'polars_version': pl.__version__,
        }
    
    def benchmark_polars_vs_pandas(self, n_rows=1_000_000, iterations=5):
        """
        Measure Polars vs Pandas on typical data workflow
        
        Tests lazy vs eager execution on:
        - Load (scan vs read)
        - Filter (lazy filter vs boolean indexing)
        - GroupBy (lazy aggregation vs eager)
        """
        
        print(f"\n{'='*60}")
        print(f"BENCHMARK: Polars vs Pandas ({n_rows:,} rows, {iterations} iterations)")
        print(f"{'='*60}\n")
        
        # Generate test data
        print("Generating test data...")
        data = {
            'timestamp': np.arange(n_rows, dtype=np.int64),
            'symbol': ['SPY'] * n_rows,
            'price': np.random.randn(n_rows) * 10 + 450,
            'volume': np.random.randint(100, 10000, n_rows).astype(np.int32)
        }
        
        pandas_times = []
        polars_times = []
        
        for i in range(iterations):
            print(f"Iteration {i+1}/{iterations}...")
            
            # Pandas (eager execution)
            t0 = time.perf_counter()
            df = pd.DataFrame(data)
            df = df[df['price'] > 450]
            result_pd = df.groupby('symbol').agg({'price': 'mean', 'volume': 'sum'})
            pandas_time = time.perf_counter() - t0
            pandas_times.append(pandas_time)
            
            # Polars (lazy execution)
            t0 = time.perf_counter()
            result_pl = (
                pl.LazyFrame(data)
                .filter(pl.col('price') > 450)
                .group_by('symbol')  # Note: group_by not groupby in newer Polars
                .agg([
                    pl.mean('price').alias('price_mean'),
                    pl.sum('volume').alias('volume_sum')
                ])
                .collect()
            )
            polars_time = time.perf_counter() - t0
            polars_times.append(polars_time)
        
        # Calculate statistics
        pandas_avg = np.mean(pandas_times)
        pandas_std = np.std(pandas_times)
        polars_avg = np.mean(polars_times)
        polars_std = np.std(polars_times)
        speedup = pandas_avg / polars_avg
        
        print(f"\nResults:")
        print(f"  Pandas: {pandas_avg:.4f}s ± {pandas_std:.4f}s")
        print(f"  Polars: {polars_avg:.4f}s ± {polars_std:.4f}s")
        print(f"  Speedup: {speedup:.2f}x")
        
        return {
            'test': 'polars_vs_pandas',
            'n_rows': n_rows,
            'iterations': iterations,
            'pandas_time_avg': pandas_avg,
            'pandas_time_std': pandas_std,
            'polars_time_avg': polars_avg,
            'polars_time_std': polars_std,
            'speedup': speedup,
            'timestamp': datetime.now().isoformat(),
            'system_info': self.system_info
        }
    
    def benchmark_cython_speedup(self, n=1_000_000, iterations=5):
        """
        Measure Cython vs Python for energy calculations
        
        Tests compiled vs interpreted performance on:
        - Hamiltonian energy calculations (hot loop)
        - Batch processing (vectorization)
        """
        
        print(f"\n{'='*60}")
        print(f"BENCHMARK: Cython vs Python ({n:,} calculations, {iterations} iterations)")
        print(f"{'='*60}\n")
        
        # Generate test data
        print("Generating test data...")
        S = np.random.randn(n) * 10 + 450
        p = np.random.randn(n) * 0.1
        sigma = np.ones(n) * 0.2
        
        # Python version (baseline)
        def python_energies(S, p, sigma):
            """Pure Python energy calculation (slow)"""
            energies = []
            for i in range(len(S)):
                T = 0.5 * sigma[i]**2 * S[i]**2 * p[i]**2
                V = 0.5 * 0.1 * (S[i] - 450.0)**2
                energies.append(T + V)
            return np.array(energies)
        
        python_times = []
        for i in range(iterations):
            print(f"Python iteration {i+1}/{iterations}...")
            t0 = time.perf_counter()
            energies_py = python_energies(S, p, sigma)
            python_time = time.perf_counter() - t0
            python_times.append(python_time)
        
        # Cython version (if available)
        cython_available = False
        cython_times = []
        
        try:
            # Try to import compiled Cython module
            sys.path.insert(0, str(Path(__file__).parent.parent / 'quantum_trading'))
            from hamiltonian_fast import HamiltonianEngineFast
            
            engine = HamiltonianEngineFast({
                'mean_reversion': 0.1,
                'equilibrium': 450.0,
                'drift': 0.0,
                'friction': 0.01
            })
            
            for i in range(iterations):
                print(f"Cython iteration {i+1}/{iterations}...")
                t0 = time.perf_counter()
                energies_cy = engine.batch_energies_fast(S, p, sigma)
                cython_time = time.perf_counter() - t0
                cython_times.append(cython_time)
            
            cython_available = True
            
        except ImportError as e:
            print(f"\n⚠️  Cython module not available: {e}")
            print("   Run: cd quantum_trading && python setup.py build_ext --inplace")
            cython_times = [None] * iterations
        
        # Calculate statistics
        python_avg = np.mean(python_times)
        python_std = np.std(python_times)
        
        if cython_available:
            cython_avg = np.mean(cython_times)
            cython_std = np.std(cython_times)
            speedup = python_avg / cython_avg
            
            print(f"\nResults:")
            print(f"  Python: {python_avg:.4f}s ± {python_std:.4f}s")
            print(f"  Cython: {cython_avg:.4f}s ± {cython_std:.4f}s")
            print(f"  Speedup: {speedup:.2f}x")
        else:
            cython_avg = None
            cython_std = None
            speedup = None
            
            print(f"\nResults:")
            print(f"  Python: {python_avg:.4f}s ± {python_std:.4f}s")
            print(f"  Cython: NOT AVAILABLE")
        
        return {
            'test': 'cython_speedup',
            'n': n,
            'iterations': iterations,
            'python_time_avg': python_avg,
            'python_time_std': python_std,
            'cython_time_avg': cython_avg,
            'cython_time_std': cython_std,
            'speedup': speedup,
            'cython_available': cython_available,
            'timestamp': datetime.now().isoformat(),
            'system_info': self.system_info
        }
    
    def benchmark_numpy_vectorized(self, n=1_000_000, iterations=5):
        """
        Measure NumPy vectorized vs pure Python
        
        Baseline reference for what vectorization alone achieves.
        """
        
        print(f"\n{'='*60}")
        print(f"BENCHMARK: NumPy Vectorized vs Python ({n:,} calculations, {iterations} iterations)")
        print(f"{'='*60}\n")
        
        # Generate test data
        S = np.random.randn(n) * 10 + 450
        p = np.random.randn(n) * 0.1
        sigma = np.ones(n) * 0.2
        
        # Python loop
        python_times = []
        for i in range(iterations):
            t0 = time.perf_counter()
            energies = []
            for j in range(n):
                T = 0.5 * sigma[j]**2 * S[j]**2 * p[j]**2
                energies.append(T)
            python_time = time.perf_counter() - t0
            python_times.append(python_time)
        
        # NumPy vectorized
        numpy_times = []
        for i in range(iterations):
            t0 = time.perf_counter()
            energies = 0.5 * sigma**2 * S**2 * p**2
            numpy_time = time.perf_counter() - t0
            numpy_times.append(numpy_time)
        
        python_avg = np.mean(python_times)
        numpy_avg = np.mean(numpy_times)
        speedup = python_avg / numpy_avg
        
        print(f"\nResults:")
        print(f"  Python: {python_avg:.4f}s")
        print(f"  NumPy: {numpy_avg:.4f}s")
        print(f"  Speedup: {speedup:.2f}x")
        
        return {
            'test': 'numpy_vectorized',
            'n': n,
            'iterations': iterations,
            'python_time_avg': python_avg,
            'numpy_time_avg': numpy_avg,
            'speedup': speedup,
            'timestamp': datetime.now().isoformat()
        }
    
    def run_all(self):
        """Run all benchmarks and save results"""
        
        print("\n" + "="*60)
        print(" " *15 + "BENCHMARK SUITE")
        print(" " * 10 + "Quantum Trading Stack Validation")
        print("="*60)
        
        results = []
        
        # Test 1: Polars vs Pandas
        results.append(self.benchmark_polars_vs_pandas())
        
        # Test 2: NumPy vectorized (reference)
        results.append(self.benchmark_numpy_vectorized())
        
        # Test 3: Cython speedup
        results.append(self.benchmark_cython_speedup())
        
        # Save results
        timestamp = int(time.time())
        output_file = self.results_dir / f'benchmark_results_{timestamp}.json'
        
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\n{'='*60}")
        print(f"Results saved to: {output_file}")
        print(f"{'='*60}")
        
        # Print summary
        self.print_summary(results)
        
        return results
    
    def print_summary(self, results):
        """Print summary of all benchmark results"""
        
        print("\n" + "="*60)
        print(" " * 20 + "SUMMARY")
        print("="*60)
        
        for r in results:
            print(f"\n{r['test']}:")
            if 'speedup' in r and r['speedup']:
                print(f"  Speedup: {r['speedup']:.2f}x")
                
                # Compare to claims
                if r['test'] == 'polars_vs_pandas':
                    claimed = 5.4
                    actual = r['speedup']
                    diff = ((actual - claimed) / claimed) * 100
                    print(f"  Claimed: {claimed}x")
                    print(f"  Difference: {diff:+.1f}%")
                
                elif r['test'] == 'cython_speedup':
                    claimed = 37.7
                    actual = r['speedup']
                    # This is just energy calc, not full pipeline
                    print(f"  Note: Energy calculation only (not full stack)")
            else:
                print(f"  Status: {r.get('cython_available', 'N/A')}")
        
        print("="*60 + "\n")


def main():
    """Command-line interface"""
    
    parser = argparse.ArgumentParser(description='Run quantum trading benchmarks')
    parser.add_argument('--all', action='store_true', help='Run all benchmarks')
    parser.add_argument('--polars-vs-pandas', action='store_true', help='Polars vs Pandas only')
    parser.add_argument('--cython-speedup', action='store_true', help='Cython speedup only')
    parser.add_argument('--numpy-vectorized', action='store_true', help='NumPy vectorized only')
    parser.add_argument('--iterations', type=int, default=5, help='Iterations per test')
    parser.add_argument('--n-rows', type=int, default=1_000_000, help='Number of rows')
    
    args = parser.parse_args()
    
    harness = BenchmarkHarness()
    
    if args.all or not any([args.polars_vs_pandas, args.cython_speedup, args.numpy_vectorized]):
        harness.run_all()
    else:
        results = []
        
        if args.polars_vs_pandas:
            results.append(harness.benchmark_polars_vs_pandas(
                n_rows=args.n_rows,
                iterations=args.iterations
            ))
        
        if args.numpy_vectorized:
            results.append(harness.benchmark_numpy_vectorized(
                n=args.n_rows,
                iterations=args.iterations
            ))
        
        if args.cython_speedup:
            results.append(harness.benchmark_cython_speedup(
                n=args.n_rows,
                iterations=args.iterations
            ))
        
        # Save results
        timestamp = int(time.time())
        output_file = harness.results_dir / f'benchmark_results_{timestamp}.json'
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\nResults saved to: {output_file}")
        harness.print_summary(results)


if __name__ == "__main__":
    main()
