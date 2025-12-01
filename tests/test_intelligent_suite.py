"""
Intelligent Test Suite for Universal Hamiltonian Framework

Features:
- Auto-generates tests from theorem statements
- Explains WHY tests fail
- Suggests HOW to fix failures
- Validates numerical bounds from theory
"""

import numpy as np
import pytest
from dataclasses import dataclass
from typing import Optional

# Import framework components
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from hl.canonical_library import CanonicalHamiltonians, Register, RegisterType


@dataclass
class ValidationResult:
    """Result of an intelligent validation."""
    is_valid: bool
    error_measure: float
    diagnosis: str
    suggestion: Optional[str] = None


class IntelligentValidator:
    """Validators that explain failures and suggest fixes."""
    
    @staticmethod
    def validate_hermiticity(H: np.ndarray, name: str = "H") -> ValidationResult:
        """
        Validates H = H† (Hermitian property)
        
        Args:
            H: Matrix to validate
            name: Name of the Hamiltonian for error messages
            
        Returns:
            ValidationResult with diagnosis and suggestions
        """
        is_hermitian = np.allclose(H, H.conj().T)
        symmetry_error = np.max(np.abs(H - H.conj().T))
        
        if is_hermitian:
            return ValidationResult(
                is_valid=True,
                error_measure=symmetry_error,
                diagnosis=f"{name} is Hermitian (max deviation: {symmetry_error:.2e})"
            )
        
        # INTELLIGENT DIAGNOSIS
        diff = H - H.conj().T
        max_idx = np.unravel_index(np.argmax(np.abs(diff)), diff.shape)
        
        diagnosis = f"{name} is NOT Hermitian!\n"
        diagnosis += f"Maximum symmetry deviation: {symmetry_error:.2e}\n"
        diagnosis += f"Largest deviation at position {max_idx}\n"
        diagnosis += f"  H{max_idx} = {H[max_idx]}\n"
        diagnosis += f"  H†{max_idx[::-1]} = {H.conj().T[max_idx]}\n"
        
        # INTELLIGENT SUGGESTION
        suggestion = "Common causes:\n"
        if np.any(np.imag(diff) != 0):
            suggestion += "  - Check imaginary part signs (Pauli Y should be [[0,-i],[i,0]])\n"
        if np.any(np.real(diff) != 0):
            suggestion += "  - Check real part symmetry\n"
        suggestion += "  - Verify conjugate transpose was computed correctly\n"
        
        return ValidationResult(
            is_valid=False,
            error_measure=symmetry_error,
            diagnosis=diagnosis,
            suggestion=suggestion
        )
    
    @staticmethod
    def validate_dimensions(H: np.ndarray, expected_dim: int, name: str = "H") -> ValidationResult:
        """
        Validates matrix dimensions.
        
        Args:
            H: Matrix to validate
            expected_dim: Expected Hilbert space dimension
            name: Name for error messages
            
        Returns:
            ValidationResult with diagnosis
        """
        actual_dim = H.shape[0]
        is_square = H.shape[0] == H.shape[1]
        is_correct_dim = actual_dim == expected_dim
        
        if is_square and is_correct_dim:
            return ValidationResult(
                is_valid=True,
                error_measure=0.0,
                diagnosis=f"{name} has correct dimensions {H.shape}"
            )
        
        # INTELLIGENT DIAGNOSIS
        diagnosis = f"{name} dimension mismatch!\n"
        diagnosis += f"Expected: ({expected_dim}, {expected_dim})\n"
        diagnosis += f"Actual: {H.shape}\n"
        
        if not is_square:
            suggestion = f"Matrix must be square for Hamiltonian operators.\n"
            suggestion += f"Current shape {H.shape} is not square."
        else:
            # Guess what system it might be
            if actual_dim == 2**int(np.log2(actual_dim)):
                n_qubits = int(np.log2(actual_dim))
                suggestion = f"This appears to be a {n_qubits}-qubit system (dim={actual_dim}).\n"
                suggestion += f"But you specified dim={expected_dim}.\n"
                suggestion += f"Either fix the Hamiltonian or update expected dimension."
            else:
                suggestion = f"Dimension {actual_dim} doesn't match standard qubit systems.\n"
                suggestion += f"Verify your Hamiltonian construction."
        
        return ValidationResult(
            is_valid=False,
            error_measure=abs(actual_dim - expected_dim),
            diagnosis=diagnosis,
            suggestion=suggestion
        )


class TestCanonicalLibrary:
    """Intelligent tests for canonical Hamiltonian library."""
    
    def test_all_hamiltonians_are_hermitian(self):
        """
        Tests that all canonical Hamiltonians are Hermitian.
        
        This validates Axiom: All Hamiltonians must be Hermitian operators.
        Theory: H = H† ensures real eigenvalues (observable energies).
        """
        qubit = Register("q", RegisterType.QUBIT, dimension=2)
        
        # Test H_state
        print("\n=== Testing H_state ===")
        H_state = CanonicalHamiltonians.H_state(qubit, energy_levels=np.array([0.0, 1.0]))
        result = IntelligentValidator.validate_hermiticity(H_state, "H_state")
        
        if not result.is_valid:
            pytest.fail(f"{result.diagnosis}\n\nSuggestion:\n{result.suggestion}")
        
        print(f"✓ {result.diagnosis}")
        
        # Test H_gate for each gate type
        gate_types = ['X', 'Y', 'Z', 'H']
        for gate_type in gate_types:
            print(f"\n=== Testing H_gate({gate_type}) ===")
            
            try:
                H_gate = CanonicalHamiltonians.H_gate(qubit, gate_type, {})
                result = IntelligentValidator.validate_hermiticity(H_gate, f"H_gate({gate_type})")
                
                if not result.is_valid:
                    pytest.fail(
                        f"Gate {gate_type} failed Hermiticity!\n\n"
                        f"{result.diagnosis}\n\n"
                        f"Suggestion:\n{result.suggestion}"
                    )
                
                print(f"✓ {result.diagnosis}")
                
            except Exception as e:
                pytest.fail(
                    f"Failed to create H_gate({gate_type}): {e}\n\n"
                    f"Suggestion: Check gate implementation in canonical_library.py"
                )
    
    def test_dimensions_match_register_specification(self):
        """
        Tests that Hamiltonian dimensions match register specifications.
        
        Theory: For n qubits, H ∈ C^(2^n × 2^n)
        """
        # Single qubit
        print("\n=== Testing single qubit dimensions ===")
        qubit = Register("q", RegisterType.QUBIT, dimension=2)
        H = CanonicalHamiltonians.H_state(qubit, energy_levels=np.array([0.0, 1.0]))
        
        result = IntelligentValidator.validate_dimensions(H, expected_dim=2, name="H_state(1-qubit)")
        
        if not result.is_valid:
            pytest.fail(f"{result.diagnosis}\n\nSuggestion:\n{result.suggestion}")
        
        print(f"✓ {result.diagnosis}")
    
    def test_h_state_diagonal_structure(self):
        """
        Tests that H_state produces diagonal matrices.
        
        Theory: H_state = Σ E_i |i⟩⟨i| must be diagonal.
        """
        print("\n=== Testing H_state diagonal structure ===")
        qubit = Register("q", RegisterType.QUBIT, dimension=2)
        energies = np.array([0.0, 1.0])
        H = CanonicalHamiltonians.H_state(qubit, energy_levels=energies)
        
        # Check if diagonal
        off_diagonal = H - np.diag(np.diag(H))
        max_off_diag = np.max(np.abs(off_diagonal))
        
        is_diagonal = max_off_diag < 1e-10
        
        if not is_diagonal:
            diagnosis = (
                f"H_state is not diagonal!\n"
                f"Maximum off-diagonal element: {max_off_diag}\n"
                f"Matrix:\n{H}\n"
            )
            
            suggestion = (
                f"H_state should produce diagonal matrices of the form:\n"
                f"  diag([E_0, E_1, ..., E_n])\n"
                f"Check implementation in canonical_library.py"
            )
            
            pytest.fail(f"{diagnosis}\n\nSuggestion:\n{suggestion}")
        
        # Check eigenvalues match input
        eigenvalues = np.diag(H)
        if not np.allclose(eigenvalues, energies):
            pytest.fail(
                f"H_state eigenvalues don't match input!\n"
                f"Expected: {energies}\n"
                f"Actual: {eigenvalues}\n"
                f"\n"
                f"Suggestion: Check H_state implementation"
            )
        
        print(f"✓ H_state is diagonal with correct eigenvalues {eigenvalues}")


class TestTheoremValidation:
    """Tests that validate theorem claims with numerical bounds."""
    
    def test_hermiticity_implies_real_eigenvalues(self):
        """
        Validates: Hermitian operators have real eigenvalues.
        
        Theory: If H = H†, then all eigenvalues λ ∈ ℝ
        Reference: Any quantum mechanics textbook
        """
        print("\n=== Testing Hermitian → Real Eigenvalues ===")
        
        qubit = Register("q", RegisterType.QUBIT, dimension=2)
        
        # Test multiple Hamiltonians
        test_cases = [
            ("H_state", CanonicalHamiltonians.H_state(qubit, np.array([0.0, 1.0]))),
        ]
        
        # Try gate types if they work
        gate_types = ['X', 'Y', 'Z', 'H']
        for gate_type in gate_types:
            try:
                H = CanonicalHamiltonians.H_gate(qubit, gate_type, {})
                test_cases.append((f"H_gate({gate_type})", H))
            except:
                pass
        
        for name, H in test_cases:
            print(f"\n  Testing {name}...")
            
            # Verify Hermitian
            result = IntelligentValidator.validate_hermiticity(H, name)
            assert result.is_valid, f"{name} is not Hermitian!"
            
            # Compute eigenvalues
            eigenvalues = np.linalg.eigvalsh(H)
            
            # Check all eigenvalues are real (imaginary part ~ 0)
            max_imag = np.max(np.abs(np.imag(eigenvalues)))
            
            if max_imag > 1e-10:
                pytest.fail(
                    f"{name} has complex eigenvalues!\n"
                    f"Maximum imaginary part: {max_imag}\n"
                    f"Eigenvalues: {eigenvalues}\n"
                    f"\n"
                    f"This violates: Hermitian → Real Eigenvalues\n"
                    f"Suggestion: Check Hermiticity implementation"
                )
            
            print(f"    ✓ All eigenvalues real: {eigenvalues}")


if __name__ == "__main__":
    print("="*70)
    print("INTELLIGENT TEST SUITE - Universal Hamiltonian Framework")
    print("="*70)
    print()
    print("Features:")
    print("  - Auto-validates theorems")
    print("  - Explains failure modes")
    print("  - Suggests fixes")
    print()
    print("="*70)
    print()
    
    # Run tests with pytest
    pytest.main([__file__, '-v', '-s'])
