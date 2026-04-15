"""
Invariant Inversion Algebra

Implements the mathematical framework for treating invariants as
exploratory manifolds rather than boolean gates.

Key objects:
- Ĩ: Relaxed invariant fields [0, 1]
- Φ: Violation potential (scalar)
- J_I: Inversion operator (gradient dual)
- ∂Ω: Boundary manifold
- T_x(Ω): Tangent space (lawful directions)
- N_x(Ω): Normal space (violation directions)
"""

import numpy as np
from typing import Callable, Dict, List, Tuple, Protocol, Optional


class Invariant(Protocol):
    """Protocol for invariant functions"""
    def __call__(self, x: np.ndarray) -> float: ...


class RelaxedInvariant:
    """
    Ĩ_i(x): Relaxed invariant mapping to [0, 1]
    
    1 = fully satisfied
    0 = fully violated
    intermediate = proximity to boundary
    """
    
    def __init__(self, hard_invariant: Callable, 
                 relaxation: str = "sigmoid", 
                 steepness: float = 5.0):
        self.hard = hard_invariant
        self.relaxation = relaxation
        self.k = steepness
    
    def __call__(self, x: np.ndarray) -> float:
        # Get hard constraint value
        h = self.hard(x)
        
        # Apply relaxation
        if self.relaxation == "sigmoid":
            return 1.0 / (1.0 + np.exp(-self.k * h))
        elif self.relaxation == "tanh":
            return 0.5 * (1.0 + np.tanh(self.k * h))
        elif self.relaxation == "relu":
            return min(1.0, max(0.0, h))
        else:
            return float(h > 0)  # Boolean fallback


class ViolationPotential:
    """
    Φ(x) = Σ w_i * (1 - Ĩ_i(x))
    
    Scalar violation potential measuring distance from lawful region.
    Φ = 0 → fully lawful
    Φ > 0 → degree of violation
    """
    
    def __init__(self, invariants: List[RelaxedInvariant], 
                 weights: Optional[np.ndarray] = None):
        self.invariants = invariants
        self.weights = weights if weights is not None else np.ones(len(invariants))
    
    def __call__(self, x: np.ndarray) -> float:
        values = np.array([Ĩ(x) for Ĩ in self.invariants])
        return np.sum(self.weights * (1.0 - values))
    
    def gradient(self, x: np.ndarray, epsilon: float = 1e-6) -> np.ndarray:
        """
        ∇Φ(x) = -Σ w_i * ∇Ĩ_i(x)
        
        Returns gradient pointing toward violation.
        """
        grad = np.zeros_like(x, dtype=float)
        
        for i, (Ĩ, w) in enumerate(zip(self.invariants, self.weights)):
            # Numerical gradient of relaxed invariant
            g = np.zeros_like(x)
            for j in range(len(x)):
                x_plus, x_minus = x.copy(), x.copy()
                x_plus[j] += epsilon
                x_minus[j] -= epsilon
                g[j] = (Ĩ(x_plus) - Ĩ(x_minus)) / (2 * epsilon)
            
            grad -= w * g
        
        return grad


class InversionOperator:
    """
    J_I(x) = (x, ∇Ĩ_1(x), ..., ∇Ĩ_n(x))
    
    Transforms invariants into directional signals.
    Maps to cotangent space for exploration.
    """
    
    def __init__(self, invariants: List[RelaxedInvariant]):
        self.invariants = invariants
    
    def __call__(self, x: np.ndarray, epsilon: float = 1e-6) -> Tuple[np.ndarray, np.ndarray]:
        """
        Returns:
            x: original state
            gradients: matrix of invariant gradients [n_invariants, n_dims]
        """
        n_inv = len(self.invariants)
        n_dims = len(x)
        gradients = np.zeros((n_inv, n_dims))
        
        for i, Ĩ in enumerate(self.invariants):
            for j in range(n_dims):
                x_plus, x_minus = x.copy(), x.copy()
                x_plus[j] += epsilon
                x_minus[j] -= epsilon
                gradients[i, j] = (Ĩ(x_plus) - Ĩ(x_minus)) / (2 * epsilon)
        
        return x, gradients


class LawfulManifold:
    """
    Ω = {x ∈ X | ∀I_i ∈ I, I_i(x) = 1}
    
    Represents the lawful region with tangent and normal spaces.
    """
    
    def __init__(self, invariants: List[RelaxedInvariant]):
        self.invariants = invariants
        self.phi = ViolationPotential(invariants)
    
    def is_on_manifold(self, x: np.ndarray, tolerance: float = 1e-6) -> bool:
        """Check if x ∈ Ω (Φ(x) ≈ 0)"""
        return abs(self.phi(x)) < tolerance
    
    def tangent_space_basis(self, x: np.ndarray) -> np.ndarray:
        """
        Compute basis for T_x(Ω): directions v where ∇Ĩ_i · v = 0
        
        Returns orthonormal basis vectors for tangent space.
        """
        # Get all invariant gradients at x
        gradients = []
        for Ĩ in self.invariants:
            g = np.zeros_like(x)
            for j in range(len(x)):
                x_plus, x_minus = x.copy(), x.copy()
                x_plus[j] += 1e-6
                x_minus[j] -= 1e-6
                g[j] = (Ĩ(x_plus) - Ĩ(x_minus)) / 2e-6
            gradients.append(g)
        
        # Stack gradients as rows
        G = np.array(gradients)  # [n_invariants, n_dims]
        
        # Null space of G is tangent space
        # Use SVD to find orthonormal basis
        if G.shape[0] < G.shape[1]:
            U, S, Vt = np.linalg.svd(G)
            # Null space basis: columns of V corresponding to zero singular values
            null_mask = (S < 1e-10)
            if null_mask.sum() > 0:
                basis = Vt[null_mask].T  # [n_dims, dim_null]
                return basis
        
        # If full rank or no null space, return empty
        return np.zeros((len(x), 0))
    
    def normal_space_basis(self, x: np.ndarray) -> np.ndarray:
        """
        N_x(Ω) = span{∇Ĩ_i(x)}
        
        Returns basis for normal space (violation directions).
        """
        gradients = []
        for Ĩ in self.invariants:
            g = np.zeros_like(x)
            for j in range(len(x)):
                x_plus, x_minus = x.copy(), x.copy()
                x_plus[j] += 1e-6
                x_minus[j] -= 1e-6
                g[j] = (Ĩ(x_plus) - Ĩ(x_minus)) / 2e-6
            gradients.append(g)
        
        # Gram-Schmidt to get orthonormal basis
        G = np.array(gradients)
        basis = []
        for i in range(len(G)):
            v = G[i].copy()
            for b in basis:
                v -= np.dot(v, b) * b
            norm = np.linalg.norm(v)
            if norm > 1e-10:
                basis.append(v / norm)
        
        return np.array(basis) if basis else np.zeros((len(x), 0))
