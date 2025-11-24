"""
Universal Hamiltonian Framework (UHF)

 An operational Theory of Everything:
All systems are Hamiltonians. All algorithms are propagators. All intelligence is phase-space control.

Usage:
    from uvh import define_system, PhaseSpace
    
    @define_system
    class MySystem:
        coordinates = ['x']
        
        def kinetic(self, p):
            return p.px**2 / 2
        
        def potential(self, q):
            return 0.5 * q.x**2
    
    system = MySystem()
    trajectory = system.evolve(...)
"""

__version__ = "0.1.0"
__author__ = "Mopati Labs"

# Core phase-space mechanics
from .core import PhaseSpace, HamiltonianSystem, CYTHON_AVAILABLE, MOJO_AVAILABLE

# Universal compiler DSL
from .compiler import (
    define_system,
    hamiltonian_system,
    SymbolicHamiltonian,
    harmonic_oscillator_hamiltonian,
    coupled_oscillators_hamiltonian,
)

# Domain-specific Hamiltonians (Python interfaces)
try:
    from .domains.market_dynamics import MarketHamiltonian, PolarsMarketSimulator
    from .domains.blockchain_consensus import TachyonicBlockchainHamiltonian, PolarsBlockchainHistory
    DOMAINS_AVAILABLE = True
except ImportError:
    DOMAINS_AVAILABLE = False

# Visualization
try:
    from .viz.phase_space_viz import PhaseSpaceApp
    VIZ_AVAILABLE = True
except ImportError:
    VIZ_AVAILABLE = False


__all__ = [
    # Core
    'PhaseSpace',
    'HamiltonianSystem',
    
    # Compiler
    'define_system',
    'hamiltonian_system',
    'SymbolicHamiltonian',
    'harmonic_oscillator_hamiltonian',
    'coupled_oscillators_hamiltonian',
    
    # Status flags
    'CYTHON_AVAILABLE',
    'MOJO_AVAILABLE',
    'DOMAINS_AVAILABLE',
    'VIZ_AVAILABLE',
]


def info():
    """Print system information"""
    print("="*60)
    print("UNIVERSAL HAMILTONIAN FRAMEWORK v" + __version__)
    print("="*60)
    print(f"Cython extensions: {'✓' if CYTHON_AVAILABLE else '✗'}")
    print(f"Mojo backend:      {'✓' if MOJO_AVAILABLE else '✗ (not yet available)'}")
    print(f"Domain modules:    {'✓' if DOMAINS_AVAILABLE else '✗'}")
    print(f"Visualization:     {'✓' if VIZ_AVAILABLE else '✗'}")
    print("="*60)
    print("\nPhilosophy:")
    print("  Everything that exists can be expressed as a Hamiltonian.")
    print("  Once cast into (q, p) variables, any system becomes:")
    print("    • Simulatable")
    print("    • Optimizable")
    print("    • Controllable")
    print("    • Quantizable")
    print("\nThis is the language of quantum computers, markets,")
    print("neural dynamics, cosmology, and consciousness itself.")
    print("="*60)
