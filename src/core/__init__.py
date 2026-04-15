"""Core module"""

from dataclasses import dataclass
import numpy as np
from typing import Tuple


@dataclass
class PhaseSpace:
	q: np.ndarray
	p: np.ndarray

	def __post_init__(self):
		self.q = np.asarray(self.q, dtype=np.float64)
		self.p = np.asarray(self.p, dtype=np.float64)

	def copy(self) -> "PhaseSpace":
		return PhaseSpace(q=self.q.copy(), p=self.p.copy())

	@property
	def ndof(self) -> int:
		return len(self.q)


class HamiltonianSystem:
	"""Base Hamiltonian system class with a symplectic integrator (Velocity Verlet)"""
	def __init__(self, n_dof: int = 1):
		self.n_dof = n_dof

	def kinetic(self, p: np.ndarray) -> float:
		"""Default kinetic energy (p^2 / 2m) with m=1"""
		return 0.5 * np.sum(p**2)

	def potential(self, q: np.ndarray) -> float:
		"""Default potential energy (zero)"""
		return 0.0

	def hamiltonian(self, q: np.ndarray, p: np.ndarray) -> float:
		return self.kinetic(p) + self.potential(q)

	def force(self, q: np.ndarray) -> np.ndarray:
		"""Numerical gradient of the potential: -∇V(q)"""
		epsilon = 1e-7
		grad = np.zeros_like(q)
		for i in range(len(q)):
			q[i] += epsilon
			V_plus = self.potential(q)
			q[i] -= 2*epsilon
			V_minus = self.potential(q)
			q[i] += epsilon
			grad[i] = -(V_plus - V_minus) / (2*epsilon)
		return grad

	def _verlet_step(self, state: PhaseSpace, dt: float) -> PhaseSpace:
		q = state.q.copy()
		p = state.p.copy()
		# Half-step for momentum
		p_half = p + 0.5 * dt * self.force(q)
		# Full-step position
		q_new = q + dt * p_half
		# Full-step force at new position
		f_new = self.force(q_new)
		# Full-step momentum
		p_new = p_half + 0.5 * dt * f_new
		return PhaseSpace(q=q_new, p=p_new)

	def _dH_dq(self, q: np.ndarray, p: np.ndarray) -> np.ndarray:
		"""Numerical gradient ∂H/∂q via finite differences"""
		epsilon = 1e-7
		grad = np.zeros_like(q, dtype=float)
		for i in range(len(q)):
			q_plus, q_minus = q.copy(), q.copy()
			q_plus[i] += epsilon
			q_minus[i] -= epsilon
			grad[i] = (self.hamiltonian(q_plus, p) - self.hamiltonian(q_minus, p)) / (2 * epsilon)
		return grad

	def _dH_dp(self, q: np.ndarray, p: np.ndarray) -> np.ndarray:
		"""Numerical gradient ∂H/∂p via finite differences"""
		epsilon = 1e-7
		grad = np.zeros_like(p, dtype=float)
		for i in range(len(p)):
			p_plus, p_minus = p.copy(), p.copy()
			p_plus[i] += epsilon
			p_minus[i] -= epsilon
			grad[i] = (self.hamiltonian(q, p_plus) - self.hamiltonian(q, p_minus)) / (2 * epsilon)
		return grad

	def dq_dt(self, q: np.ndarray, p: np.ndarray) -> np.ndarray:
		"""
		Compute ∂H/∂p - Hamilton's equation for q evolution.
		Returns numerical gradient by default; override for analytical derivatives.
		"""
		return self._dH_dp(q, p)

	def dp_dt(self, q: np.ndarray, p: np.ndarray) -> np.ndarray:
		"""
		Compute -∂H/∂q - Hamilton's equation for p evolution.
		Returns negative numerical gradient by default; override for analytical derivatives.
		"""
		return -self._dH_dq(q, p)

	def evolve(self, initial: PhaseSpace, t_max: float, dt: float) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
		n_steps = int(np.ceil(t_max / dt))
		t = np.linspace(0, n_steps * dt, n_steps + 1)
		q_traj = np.zeros((n_steps + 1, len(initial.q)))
		p_traj = np.zeros((n_steps + 1, len(initial.p)))

		state = initial.copy()
		q_traj[0] = state.q
		p_traj[0] = state.p

		for i in range(1, n_steps + 1):
			state = self._verlet_step(state, dt)
			q_traj[i] = state.q
			p_traj[i] = state.p

		return t, q_traj, p_traj

class DissipativeHamiltonian(HamiltonianSystem):
	"""
	Non-conservative Hamiltonian for open systems (markets, thermodynamics).
	
	Extends HamiltonianSystem with damping terms for modeling dissipative dynamics
	where energy is not conserved. Use for financial markets, friction, or thermal systems.
	"""
	
	def __init__(self, n_dof: int = 1, damping: float = 0.0):
		super().__init__(n_dof=n_dof)
		self.gamma = damping  # Damping coefficient
	
	def evolve_dissipative(self, state: PhaseSpace, dt: float, 
						   external_flow: float = 0.0) -> PhaseSpace:
		"""
		Langevin-like evolution with damping.
		
		Combines Hamiltonian dynamics with dissipative damping:
		- dq/dt = ∂H/∂p (Hamiltonian flow)
		- dp/dt = -∂H/∂q - γ·p + external_flow (damped + driven)
		"""
		q, p = state.q.copy(), state.p.copy()
		
		# Hamiltonian part
		dq = self.dq_dt(q, p) * dt
		dp = self.dp_dt(q, p) * dt
		
		# Dissipative damping
		p_damped = p * (1.0 - self.gamma * dt)
		
		# External flow (e.g., market order flow)
		p_new = p_damped + external_flow + dp
		q_new = q + dq
		
		return PhaseSpace(q=q_new, p=p_new)
	
	def entropy_production(self, state: PhaseSpace) -> float:
		"""
		Compute entropy production (dissipation measure).
		
		For damped systems: dS/dt ≈ γ·p² (energy dissipated as heat)
		"""
		return self.gamma * np.sum(state.p ** 2)
	
	def is_conservative(self) -> bool:
		"""Returns False - this is a dissipative system"""
		return self.gamma == 0.0


# Optional flags for components available
CYTHON_AVAILABLE = False
MOJO_AVAILABLE = False
