"""
Universal Hamiltonian Framework - Core Module

Python interface to Mojo/Cython backends with high-level API.
"""

__version__ = "0.1.0"

# Core phase-space structures (Python wrappers for Mojo types)
import numpy as np
from dataclasses import dataclass
from typing import Callable, Tuple, Optional

@dataclass
class PhaseSpace:
    """
    Phase-space point representation: (q, p)
    
    Attributes:
        q: Generalized coordinates (positions)
        p: Generalized momenta
    """
    q: np.ndarray
    p: np.ndarray
    
    def __post_init__(self):
        """Ensure q and p are numpy arrays of same shape"""
        self.q = np.asarray(self.q, dtype=np.float64)
        self.p = np.asarray(self.p, dtype=np.float64)
        assert self.q.shape == self.p.shape, "q and p must have same shape"
    
    @property
    def ndof(self) -> int:
        """Number of degrees of freedom"""
        return len(self.q)
    
    def copy(self) -> 'PhaseSpace':
        """Create deep copy"""
        return PhaseSpace(q=self.q.copy(), p=self.p.copy())
    
    def energy(self, hamiltonian: Callable) -> float:
        """Compute H(q, p)"""
        return hamiltonian(self.q, self.p)


class HamiltonianSystem:
    """
    Base class for Hamiltonian systems.
    
    Subclass and implement:
    - kinetic(p): Kinetic energy T(p)
    - potential(q): Potential energy V(q)
    - force(q): Force = -∇V(q)
    """
    
    def __init__(self, n_dof: int, mass: Optional[np.ndarray] = None):
        self.n_dof = n_dof
        self.mass = mass if mass is not None else np.ones(n_dof)
    
    def kinetic(self, p: np.ndarray) -> float:
        """Kinetic energy: T = Σ p²/(2m)"""
        return np.sum(p**2 / (2 * self.mass))
    
    def potential(self, q: np.ndarray) -> float:
        """Potential energy V(q) - override in subclass"""
        raise NotImplementedError("Subclass must implement potential(q)")
    
    def force(self, q: np.ndarray) -> np.ndarray:
        """Force F = -∇V - override in subclass or compute numerically"""
        # Numerical gradient
        epsilon = 1e-7
        grad = np.zeros_like(q)
        for i in range(len(q)):
            q[i] += epsilon
            V_plus = self.potential(q)
            q[i] -= 2*epsilon
            V_minus = self.potential(q)
            q[i] += epsilon  # Restore
            grad[i] = -(V_plus - V_minus) / (2*epsilon)
        return grad
    
    def hamiltonian(self, q: np.ndarray, p: np.ndarray) -> float:
        """Total energy: H = T + V"""
        return self.kinetic(p) + self.potential(q)
    
    def evolve(
        self,
        initial_state: PhaseSpace,
        t_max: float,
        dt: float = 0.01,
        method: str = 'verlet'
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Evolve system from initial state.
        
        Args:
            initial_state: Starting phase-space point
            t_max: Maximum time
            dt: Timestep
            method: Integration method ('verlet', 'rk4')
        
        Returns:
            (times, q_trajectory, p_trajectory)
        """
        n_steps = int(t_max / dt)
        times = np.linspace(0, t_max, n_steps)
        
        q_traj = np.zeros((n_steps, self.n_dof))
        p_traj = np.zeros((n_steps, self.n_dof))
        
        state = initial_state.copy()
        
        for i in range(n_steps):
            q_traj[i] = state.q
            p_traj[i] = state.p
            
            if method == 'verlet':
                state = self._verlet_step(state, dt)
            else:
                raise ValueError(f"Unknown method: {method}")
        
        return times, q_traj, p_traj
    
    def _verlet_step(self, state: PhaseSpace, dt: float) -> PhaseSpace:
        """Symplectic Verlet integration step"""
        q, p = state.q.copy(), state.p.copy()
        
        # Half-step momentum
        F = self.force(q)
        p += 0.5 * dt * F
        
        # Full-step position
        q += dt * p / self.mass
        
        # Half-step momentum
        F = self.force(q)
        p += 0.5 * dt * F
        
        return PhaseSpace(q=q, p=p)


# Attempt to import Cython extensions
try:
    from .canonical_transforms import (
        poisson_bracket,
        action_angle_variables,
        symplectic_gradient,
        is_canonical_transform
    )
    CYTHON_AVAILABLE = True
except ImportError:
    CYTHON_AVAILABLE = False
    print("Warning: Cython extensions not built. Run 'python setup.py build_ext --inplace'")

# Attempt to import Mojo modules (when available)
try:
    # from .hamiltonian_engine import HamiltonianSystem as MojoHamiltonianSystem
    MOJO_AVAILABLE = False  # Set to True when Mojo is ready
except ImportError:
    MOJO_AVAILABLE = False

__all__ = [
    'PhaseSpace',
    'HamiltonianSystem',
    'CYTHON_AVAILABLE',
    'MOJO_AVAILABLE',
]
