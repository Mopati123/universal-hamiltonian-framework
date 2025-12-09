#!/usr/bin/env python3
"""
Quantum Trading System - Quick Start Demo

This script demonstrates the practical application of the
Universal Hamiltonian Framework for Markets (Chapter 9).

Run this after cloning the repository to see it in action!
"""

import sys
from pathlib import Path

# Add paths for imports
sys.path.insert(0, str(Path(__file__).parent))

from experiments.markets.quantum_trading.execution.system import TradingSystem


def main():
    """Run demo trading system"""
    
    print("\n" + "="*80)
    print(" " * 15 + "QUANTUM-INSPIRED TRADING SYSTEM")
    print(" " * 5 + "Chapter 9: Practical Application of Universal Hamiltonian Framework")
    print(" " * 20 + "Markets Domain")
    print("="*80)
    
    print("\n📚 This demonstrates Chapter 9: Empirical Validation")
    print("    How mathematics underpins trading through:")
    print("    1. Hamiltonian mechanics for market modeling")
    print("    2. Quantum-inspired decision layer")
    print("    3. QUBO optimization for portfolio allocation")
    print()
    
    # Create trading system
    print("🔧 Initializing trading system...")
    system = TradingSystem(
        universe=['SPY', 'QQQ', 'IWM'],  # Trade 3 ETFs
        capital=10000.0,                  # $10,000 capital
        mode='simulation'                  # Simulation mode (no real money!)
    )
    
    print("✅ System initialized")
    print(f"   Universe: {system.universe}")
    print(f"   Capital: ${system.capital:,.2f}")
    print(f"   Mode: {system.mode}")
    print()
    
    # Run trading system
    print("🚀 Running quantum trading system...")
    print("   (This will take ~10 seconds)\n")
    
    system.run(
        iterations=10,   # 10 decision cycles
        delay=0.5        # 0.5 seconds between iterations
    )
    
    print("\n" + "="*80)
    print("✅ DEMO COMPLETE!")
    print("="*80)
    print()
    print("📊 Results saved to: trading_log.csv")
    print()
    print("📖 What you just saw:")
    print("   • Hamiltonian engine calculated market energies")
    print("   • Quantum wavefunction represented superposition of trading actions")
    print("   • VQE optimization minimized expected energy")
    print("   • QUBO solver found optimal portfolio")
    print("   • System executed trades based on quantum measurement")
    print()
    print("🎯 This is mathematics underpinning reality!")
    print("   Not theory - actual working trading software.")
    print()
    print("📚 Learn more:")
    print("   • docs/book-of-mopati-chapter9-empirical-validation.md")
    print("   • experiments/markets/quantum_trading/ (source code)")
    print("   • experiments/markets/data_sources/ (multi-source data)")
    print("   • GitHub: https://github.com/Mopati123/universal-hamiltonian-framework")
    print()
    print("="*80 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Demo interrupted by user.")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        print("\nIf you see import errors, make sure to install dependencies:")
        print("  pip install -r experiments/markets/quantum_trading/requirements.txt")
