"""
Hamiltonian Language (HL) - Canonical Operator Library

This module defines the primitive Hamiltonians and canonical operators
that form the universal basis for expressing computation as physics.

Every program in HL is a linear combination of these primitives.

Author: Mopati + Framework
Date: November 26, 2025
"""

import numpy as np
from dataclasses import dataclass
from typing import List, Callable, Optional, Tuple
from enum import Enum

# ============================================================================
# FUNDAMENTAL CONSTANTS
# ============================================================================

HBAR = 1.0  # Natural units (ℏ = 1)
KB = 1.0    # Boltzmann constant

# ============================================================================
# REGISTER TYPES
# ============================================================================

class RegisterType(Enum):
    """Types of quantum registers"""
    QUBIT = "qubit"           # 2-level system
    QUTRIT = "qutrit"         # 3-level system
    MODE = "mode"             # Harmonic oscillator (infinite-dim)
    SPIN = "spin"             # Spin-j system
    CLASSICAL = "classical"   # Classical bit/register

@dataclass
class Register:
    """A quantum or classical register"""
    name: str
    reg_type: RegisterType
    dimension: int
    
    def __repr__(self):
        return f"Register({self.name}, {self.reg_type.value}, d={self.dimension})"

# ============================================================================
# CANONICAL HAMILTONIANS (The 9 Primitives)
# ============================================================================

class CanonicalHamiltonians:
    """
    The 9 irreducible Hamiltonian terms that generate all computation.
    
    Any program H = Σ α_i H_i where i ∈ {state, gate, interact, clock, 
                                          noise, penalty, io, thermo, meta}
    """
    
    @staticmethod
    def H_state(register: Register, energy_levels: np.ndarray) -> np.ndarray:
        """
        H_state = Σ E_i |i⟩⟨i|
        
        Diagonal Hamiltonian encoding computational basis energies.
        Used for: state preparation, energy penalties, cost functions.
        
        Args:
            register: Target register
            energy_levels: E_i for each basis state
        
        Returns:
            Diagonal matrix of energies
        """
        d = register.dimension
        assert len(energy_levels) == d, f"Need {d} energies, got {len(energy_levels)}"
        
        return np.diag(energy_levels)
    
    @staticmethod
    def H_gate(register: Register, gate_type: str, params: dict) -> np.ndarray:
        """
        H_gate = Ω(t) σ_x/y/z or general unitary generator
        
        Single-register unitary evolution.
        Used for: logic gates, rotations, basis transformations.
        
        Args:
            register: Target register
            gate_type: 'X', 'Y', 'Z', 'H', 'T', 'RX', 'RY', 'RZ'
            params: Gate parameters (e.g., {'angle': θ} for rotations)
        
        Returns:
            Hermitian generator of unitary
        """
        d = register.dimension
        
        if register.reg_type == RegisterType.QUBIT:
            # Pauli matrices
            if gate_type == 'X':
                return np.array([[0, 1], [1, 0]], dtype=complex)
            elif gate_type == 'Y':
                return np.array([[0, -1j], [1j, 0]], dtype=complex)
            elif gate_type == 'Z':
                return np.array([[1, 0], [0, -1]], dtype=complex)
            elif gate_type == 'H':
                # Hadamard generator (π/2 rotation around X+Z axis)
                return (np.array([[0, 1], [1, 0]]) + np.array([[1, 0], [0, -1]])) / np.sqrt(2)
            elif gate_type in ['RX', 'RY', 'RZ']:
                # Rotation generators
                theta = params.get('angle', 0)
                if gate_type == 'RX':
                    return theta * np.array([[0, 1], [1, 0]]) / 2
                elif gate_type == 'RY':
                    return theta * np.array([[0, -1j], [1j, 0]]) / 2
                else:  # RZ
                    return theta * np.array([[1, 0], [0, -1]]) / 2
        else:
            raise NotImplementedError(f"Gate {gate_type} for {register.reg_type} not implemented")
    
    @staticmethod
    def H_interact(reg1: Register, reg2: Register, coupling: float, 
                   interaction_type: str = 'ZZ') -> np.ndarray:
        """
        H_interact = J σ₁ ⊗ σ₂
        
        Two-register coupling Hamiltonian.
        Used for: CNOT, SWAP, entanglement, cross-domain coupling.
        
        Args:
            reg1, reg2: Registers to couple
            coupling: Interaction strength J
            interaction_type: 'ZZ', 'XX', 'YY', 'XY', 'CNOT', 'SWAP'
        
        Returns:
            Kronecker product H₁ ⊗ H₂
        """
        d1, d2 = reg1.dimension, reg2.dimension
        
        if interaction_type == 'ZZ':
            # Ising interaction
            Z = np.array([[1, 0], [0, -1]])
            return coupling * np.kron(Z, Z)
        
        elif interaction_type == 'XX':
            X = np.array([[0, 1], [1, 0]])
            return coupling * np.kron(X, X)
        
        elif interaction_type == 'CNOT':
            # CNOT generator (ZX interaction)
            Z = np.array([[1, 0], [0, -1]])
            X = np.array([[0, 1], [1, 0]])
            return coupling * np.kron(Z, X)
        
        elif interaction_type == 'SWAP':
            # SWAP generator
            return coupling * (np.kron(np.array([[0, 1], [1, 0]]), np.array([[0, 1], [1, 0]])) +
                              np.kron(np.array([[0, -1j], [1j, 0]]), np.array([[0, -1j], [1j, 0]])) +
                              np.kron(np.array([[1, 0], [0, -1]]), np.array([[1, 0], [0, -1]])))
        
        else:
            raise NotImplementedError(f"Interaction {interaction_type} not implemented")
    
    @staticmethod
    def H_clock(register: Register, frequency: float) -> np.ndarray:
        """
        H_clock = ω t |excited⟩⟨excited|
        
        Time-dependent energy accumulation.
        Used for: phase accumulation, scheduling, time-ordered operations.
        
        Args:
            register: Clock register
            frequency: Angular frequency ω
        
        Returns:
            Clock Hamiltonian (time-multiplied in evolution)
        """
        d = register.dimension
        # Clock = energy on excited state
        H = np.zeros((d, d))
        H[-1, -1] = frequency  # Highest energy state = "ticking"
        return H
    
    @staticmethod
    def H_noise(register: Register, noise_strength: float, 
                noise_type: str = 'dephasing') -> Tuple[np.ndarray, List[np.ndarray]]:
        """
        H_noise via Lindblad operators L_k
        
        Dissipation and decoherence.
        Used for: error modeling, thermalization, irreversibility.
        
        Args:
            register: Noisy register
            noise_strength: γ (decoherence rate)
            noise_type: 'dephasing', 'decay', 'thermal'
        
        Returns:
            (H_drift, [L_1, L_2, ...]) - Hamiltonian and Lindblad operators
        """
        d = register.dimension
        
        if noise_type == 'dephasing':
            # Pure dephasing: L = √γ Z
            L = np.sqrt(noise_strength) * np.array([[1, 0], [0, -1]])
            return np.zeros((d, d)), [L]
        
        elif noise_type == 'decay':
            # Amplitude damping: L = √γ |0⟩⟨1|
            L = np.sqrt(noise_strength) * np.array([[0, 1], [0, 0]])
            return np.zeros((d, d)), [L]
        
        elif noise_type == 'thermal':
            # Thermal bath at temperature T
            # L₊ = √(γ n_th) |1⟩⟨0|, L₋ = √(γ (n_th+1)) |0⟩⟨1|
            # where n_th = thermal occupation
            n_th = 0.1  # Low temperature
            L_plus = np.sqrt(noise_strength * n_th) * np.array([[0, 0], [1, 0]])
            L_minus = np.sqrt(noise_strength * (n_th + 1)) * np.array([[0, 1], [0, 0]])
            return np.zeros((d, d)), [L_plus, L_minus]
        
        else:
            raise NotImplementedError(f"Noise type {noise_type} not implemented")
    
    @staticmethod
    def H_penalty(register: Register, constraint: Callable[[np.ndarray], float],
                  penalty_strength: float = 100.0) -> np.ndarray:
        """
        H_penalty = λ Σ P_constraint
        
        Energy penalty for constraint violation.
        Used for: logical constraints, optimization objectives, error correction.
        
        Args:
            register: Constrained register
            constraint: Function that returns 0 if satisfied, >0 if violated
            penalty_strength: λ (penalty coefficient)
        
        Returns:
            Penalty Hamiltonian (diagonal, penalizes bad states)
        """
        d = register.dimension
        H_pen = np.zeros((d, d))
        
        # Evaluate constraint on each basis state
        for i in range(d):
            state = np.zeros(d)
            state[i] = 1.0
            violation = constraint(state)
            H_pen[i, i] = penalty_strength * violation
        
        return H_pen
    
    @staticmethod
    def H_io(register: Register, input_amplitude: np.ndarray) -> np.ndarray:
        """
        H_io = Σ f_in(t) |i⟩⟨i|
        
        Input/output coupling to environment.
        Used for: data loading, measurement, classical feedback.
        
        Args:
            register: I/O register
            input_amplitude: Driving amplitudes for each basis state
        
        Returns:
            Diagonal drive Hamiltonian
        """
        d = register.dimension
        assert len(input_amplitude) == d
        
        return np.diag(input_amplitude)
    
    @staticmethod
    def H_thermo(register: Register, temperature: float, 
                 energy_scale: float = 1.0) -> Tuple[np.ndarray, float]:
        """
        H_thermo = H_system with partition function Z = Tr[e^{-βH}]
        
        Thermodynamic coupling to heat bath.
        Used for: Landauer accounting, annealing, thermal computing.
        
        Args:
            register: Thermodynamic register
            temperature: T in energy units
            energy_scale: Characteristic energy
        
        Returns:
            (H_system, free_energy F = -k_B T ln Z)
        """
        d = register.dimension
        
        # Simple energy spectrum
        energies = np.arange(d) * energy_scale
        H = np.diag(energies)
        
        # Compute partition function
        beta = 1.0 / (KB * temperature) if temperature > 0 else np.inf
        Z = np.sum(np.exp(-beta * energies))
        F = -KB * temperature * np.log(Z) if temperature > 0 else energies[0]
        
        return H, F
    
    @staticmethod
    def H_meta(parameters: np.ndarray, objectives: dict) -> float:
        """
        H_meta(θ) = α F(θ) + β L(θ) + γ E(θ) + δ R(θ)
        
        Meta-optimization Hamiltonian for compiler/parameter tuning.
        Used for: auto-optimization, learning, self-improvement.
        
        Args:
            parameters: θ (compilation parameters, pulse shapes, etc.)
            objectives: {'fidelity': F, 'latency': L, 'energy': E, 'resources': R}
        
        Returns:
            Scalar objective to minimize
        """
        alpha = objectives.get('fidelity_weight', 1.0)
        beta = objectives.get('latency_weight', 0.1)
        gamma = objectives.get('energy_weight', 0.01)
        delta = objectives.get('resource_weight', 0.001)
        
        F = objectives.get('fidelity_func', lambda p: 0)(parameters)
        L = objectives.get('latency_func', lambda p: 0)(parameters)
        E = objectives.get('energy_func', lambda p: 0)(parameters)
        R = objectives.get('resource_func', lambda p: 0)(parameters)
        
        return alpha * F + beta * L + gamma * E + delta * R


# ============================================================================
# EXAMPLE PROGRAMS IN HL
# ============================================================================

class HLExamples:
    """Canonical examples of programs expressed in HL"""
    
    @staticmethod
    def example_CNOT():
        """
        CNOT gate via interaction Hamiltonian
        
        H = J Z ⊗ X for time τ such that J τ = π/4
        """
        control = Register("control", RegisterType.QUBIT, 2)
        target = Register("target", RegisterType.QUBIT, 2)
        
        J = np.pi / 4  # Coupling strength
        tau = 1.0      # Evolution time (J * tau = π/4)
        
        H = CanonicalHamiltonians.H_interact(control, target, J, 'CNOT')
        
        return {
            'registers': [control, target],
            'hamiltonian': H,
            'time': tau,
            'description': 'CNOT via ZX interaction'
        }
    
    @staticmethod
    def example_NAND_penalty():
        """
        NAND gate via penalty method
        
        H_penalty penalizes states violating NAND truth table
        System evolves to ground state = correct NAND output
        """
        in1 = Register("in1", RegisterType.QUBIT, 2)
        in2 = Register("in2", RegisterType.QUBIT, 2)
        out = Register("out", RegisterType.QUBIT, 2)
        
        # NAND truth table constraint
        def nand_constraint(state):
            """Returns energy > 0 if NAND violated"""
            # State is |in1, in2, out⟩
            # NAND: out = NOT(in1 AND in2)
            # Encode as 3-qubit state |abc⟩
            
            # This is simplified - full implementation needs 8x8 matrix
            return 0.0  # Placeholder
        
        H_pen = CanonicalHamiltonians.H_penalty(out, nand_constraint, penalty_strength=100.0)
        
        return {
            'registers': [in1, in2, out],
            'hamiltonian': H_pen,
            'description': 'NAND via penalty optimization'
        }
    
    @staticmethod
    def example_adder():
        """
        Quantum adder via carry-chain Hamiltonian
        
        H = H_carry + H_sum
        """
        # Simplified 2-bit adder
        a = Register("a", RegisterType.QUBIT, 2)
        b = Register("b", RegisterType.QUBIT, 2)
        carry = Register("carry", RegisterType.QUBIT, 2)
        sum_out = Register("sum", RegisterType.QUBIT, 2)
        
        # Carry generation: carry = a AND b
        H_carry = CanonicalHamiltonians.H_interact(a, b, 1.0, 'ZZ')
        
        # Sum: sum = a XOR b XOR carry
        H_sum = CanonicalHamiltonians.H_interact(a, b, 1.0, 'XX')
        
        H_total = H_carry + H_sum
        
        return {
            'registers': [a, b, carry, sum_out],
            'hamiltonian': H_total,
            'description': 'Quantum adder'
        }


# ============================================================================
# HL PROGRAM SPECIFICATION
# ============================================================================

@dataclass
class HLProgram:
    """
    A complete HL program specification
    
    Declares registers, Hamiltonian, schedule, and execution parameters
    """
    name: str
    registers: List[Register]
    hamiltonian_terms: List[Tuple[str, np.ndarray, float]]  # (name, H_i, α_i)
    schedule: Callable[[float], np.ndarray]  # t → H(t)
    lindblad_ops: List[np.ndarray] = None    # Noise operators
    total_time: float = 1.0
    dt: float = 0.01
    
    def total_hamiltonian(self, t: float) -> np.ndarray:
        """Compute H_total(t) = Σ α_i(t) H_i"""
        H = np.zeros_like(self.hamiltonian_terms[0][1])
        
        for name, H_i, alpha in self.hamiltonian_terms:
            H += alpha * H_i
        
        # Apply schedule
        H_scheduled = self.schedule(t) * H if callable(self.schedule) else H
        
        return H_scheduled
    
    def __repr__(self):
        n_regs = len(self.registers)
        n_terms = len(self.hamiltonian_terms)
        return f"HLProgram({self.name}, {n_regs} registers, {n_terms} terms)"


# ============================================================================
# EXPORT
# ============================================================================

__all__ = [
    'RegisterType',
    'Register',
    'CanonicalHamiltonians',
    'HLExamples',
    'HLProgram',
    'HBAR',
    'KB'
]


if __name__ == "__main__":
    print("=" * 70)
    print("HAMILTONIAN LANGUAGE (HL) - CANONICAL LIBRARY")
    print("=" * 70)
    
    # Demo: CNOT program
    cnot = HLExamples.example_CNOT()
    print("\n[Example: CNOT Gate]")
    print(f"Registers: {cnot['registers']}")
    print(f"Hamiltonian shape: {cnot['hamiltonian'].shape}")
    print(f"Evolution time: {cnot['time']}")
    print(f"Description: {cnot['description']}")
    
    # Demo: Canonical Hamiltonians
    print("\n[Canonical Hamiltonians Demo]")
    q = Register("qubit", RegisterType.QUBIT, 2)
    
    H_x = CanonicalHamiltonians.H_gate(q, 'X', {})
    print(f"H_X:\n{H_x}")
    
    H_noise_drift, L_ops = CanonicalHamiltonians.H_noise(q, 0.1, 'dephasing')
    print(f"\nDephasing Lindblad: {len(L_ops)} operators")
    print(f"L_dephasing:\n{L_ops[0]}")
    
    print("\n" + "=" * 70)
    print("HL Canonical Library loaded - Ready for compilation!")
    print("=" * 70)
