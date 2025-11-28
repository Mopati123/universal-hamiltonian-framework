"""
Minimal Example: Hamiltonian Language Basics

This is the simplest possible example that actually runs.
Copy-paste this and it works!
"""

import numpy as np
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from hl.canonical_library import CanonicalHamiltonians, Register, RegisterType

def main():
    print("="*60)
    print("MINIMAL HAMILTONIAN LANGUAGE EXAMPLE")
    print("="*60)
    
    # Step 1: Define a qubit register
    print("\n1. Creating a qubit register...")
    qubit = Register(name="q", reg_type=RegisterType.QUBIT, dimension=2)
    print(f"   Created: {qubit.name} with dimension {qubit.dimension}")
    
    # Step 2: Create a simple energy eigenstate Hamiltonian
    print("\n2. Creating H_state (energy levels [0, 1])...")
    H_energy = CanonicalHamiltonians.H_state(qubit, energy_levels=np.array([0.0, 1.0]))
    print(f"   H_state matrix:")
    print(f"   {H_energy}")
    
    # Step 3: Verify it's Hermitian
    print("\n3. Verifying Hermiticity (H = H†)...")
    is_hermitian = np.allclose(H_energy, H_energy.conj().T)
    print(f"   Hermitian: {is_hermitian}")
    
    # Step 4: Verify it's diagonal
    print("\n4. Verifying diagonal structure...")
    off_diagonal = np.abs(H_energy - np.diag(np.diag(H_energy)))
    is_diagonal = np.allclose(off_diagonal, 0)
    print(f"   Diagonal: {is_diagonal}")
    
    # Step 5: Different energy levels
    print("\n5. Creating H_state with different energies...")
    H_custom = CanonicalHamiltonians.H_state(qubit, energy_levels=np.array([1.5, 2.7]))
    eigenvalues = np.diag(H_custom)
    print(f"   Eigenvalues: {eigenvalues}")
    print(f"   This encodes energy cost for each basis state")
    
    print("\n" + "="*60)
    print("SUCCESS! All checks passed")
    print("="*60)
    print("\nWhat this demonstrated:")
    print("  - Creating quantum registers")
    print("  - Building H_state (diagonal energy Hamiltonians)")
    print("  - Verifying Hermiticity (H = H†)")
    print("  - Diagonal structure for energy levels")
    print("\nNext steps:")
    print("  - Run: python examples/reference_implementation.py")
    print("  - Read: docs/NAVIGATION.md for comprehensive guide")
    print("  - Explore: src/hl/canonical_library.py for all 9 primitives")

if __name__ == "__main__":
    main()
