"""Compiler package exports the DSL and Symbolic Engine APIs.

This module re-exports the primary compiler interfaces used by tests and
the top-level package (define_system, SymbolicHamiltonian, etc.).
"""

from .hamiltonian_dsl import define_system, hamiltonian_system
from .symbolic_engine import (
	SymbolicHamiltonian,
	harmonic_oscillator_hamiltonian,
	coupled_oscillators_hamiltonian,
)

__all__ = [
	'define_system',
	'hamiltonian_system',
	'SymbolicHamiltonian',
	'harmonic_oscillator_hamiltonian',
	'coupled_oscillators_hamiltonian',
]