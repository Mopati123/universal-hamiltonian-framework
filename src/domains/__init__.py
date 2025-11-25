"""
Universal Hamiltonian Framework - Domains Package

This package contains domain-specific Hamiltonian implementations across:
- Quantum mechanics
- Classical physics
- Financial markets
- Consciousness/neural fields
- Blockchain consensus

Each domain shares the same mathematical foundation but represents
different physical/abstract systems.
"""

# Python implementations (ready to use)
try:
    from .market_dynamics import (
        MarketHamiltonian,
        MarketState,
        PolarsMarketSimulator,
        create_order_book_potential
    )
except ImportError:
    MarketHamiltonian = None

try:
    from .blockchain_consensus import (
        TachyonicBlockchainHamiltonian,
        BlockState,
        PolarsBlockchainHistory,
        simulate_tachyonic_blockchain
    )
except ImportError:
    TachyonicBlockchainHamiltonian = None

# Mojo implementations (requires Mojo runtime)
# These will be available when Mojo package manager is ready
MOJO_AVAILABLE = False

try:
    # Future: import from compiled Mojo modules
    # from .quantum_systems import QuantumHarmonicOscillator, EntangledPair
    # from .consciousness_field import ConsciousnessFieldHamiltonian, compute_phi
    pass
except:
    pass

# Cython implementations (requires compilation)
CYTHON_AVAILABLE = False

try:
    # After building: python setup.py build_ext --inplace
    # from .classical_mechanics import NBodyGravity, CoupledOscillators, DoublePendulum
    pass
except:
    pass

__all__ = [
    # Market dynamics
    'MarketHamiltonian',
    'MarketState',
    'PolarsMarketSimulator',
    'create_order_book_potential',
    
    # Blockchain
    'TachyonicBlockchainHamiltonian',
    'BlockState',
    'PolarsBlockchainHistory',
    'simulate_tachyonic_blockchain',
]

# Status flags
__domain_status__ = {
    'market': MarketHamiltonian is not None,
    'blockchain': TachyonicBlockchainHamiltonian is not None,
    'quantum': MOJO_AVAILABLE,
    'classical': CYTHON_AVAILABLE,
    'consciousness': MOJO_AVAILABLE,
}

def list_available_domains():
    """Return list of currently available domains"""
    available = []
    for domain, is_available in __domain_status__.items():
        if is_available:
            available.append(domain)
    return available

def domain_status():
    """Print status of all domain implementations"""
    print("Domain Implementation Status:")
    print("-" * 40)
    for domain, status in __domain_status__.items():
        symbol = "✓" if status else "✗"
        print(f"  {symbol} {domain.capitalize()}")
    
    if not MOJO_AVAILABLE:
        print("\nNote: Mojo domains require Mojo runtime")
    if not CYTHON_AVAILABLE:
        print("Note: Cython domains require compilation")
        print("  Run: python setup.py build_ext --inplace")
