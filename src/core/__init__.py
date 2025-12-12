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

# Optional flags for components available
CYTHON_AVAILABLE = False
MOJO_AVAILABLE = False
