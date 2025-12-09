"""
Quantum-Inspired Trading System

A production-ready trading system combining:
1. Hamiltonian mechanics for market modeling
2. Quantum-inspired decision layer for regime adaptation
3. Multi-source data infrastructure
4. Risk-aware execution

This is the practical application of the Universal Hamiltonian Framework
demonstrating how mathematics underpins trading.
"""

__version__ = "1.0.0"
__author__ = "Universal Hamiltonian Framework"

from .hamiltonian.engine import HamiltonianEngine
from .quantum.wavefunction import QuantumDecisionLayer
from .optimization.qubo import QUBOOptimizer
from .execution.system import TradingSystem

__all__ = [
    'HamiltonianEngine',
    'QuantumDecisionLayer',
    'QUBOOptimizer',
    'TradingSystem'
]
