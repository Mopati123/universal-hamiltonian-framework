"""
Domain-to-canonical adapter layer.

Converts domain Hamiltonians into HL canonical terms so they can be validated
and evolved with a uniform pipeline.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, List, Optional

import numpy as np

from hl.canonical_library import CanonicalHamiltonians, HLProgram, Register, RegisterType


@dataclass
class CanonicalAdapterResult:
    """Canonical representation plus classical state for invariant checks."""
    name: str
    program: HLProgram
    initial_q: np.ndarray
    initial_p: np.ndarray
    hamiltonian: Callable[[np.ndarray, np.ndarray], float]
    metadata: Dict[str, float]


class DomainAdapter:
    """Base adapter contract."""

    name: str

    def build(self) -> Optional[CanonicalAdapterResult]:
        raise NotImplementedError


class MarketDomainAdapter(DomainAdapter):
    """Adapter for a simple market Hamiltonian model."""

    name = "markets"

    def __init__(self, params: Optional[Dict[str, float]] = None):
        params = params or {}
        self.liquidity_mass = params.get("liquidity_mass", 1.0)
        self.volatility = params.get("volatility", 0.1)
        self.mean_reversion = params.get("mean_reversion", 0.5)
        self.equilibrium_price = params.get("equilibrium_price", 100.0)

    def _hamiltonian(self, q: np.ndarray, p: np.ndarray) -> float:
        price = float(q[0])
        momentum = float(p[0])
        kinetic = momentum**2 / (2.0 * self.liquidity_mass)
        potential = 0.5 * self.mean_reversion * (price - self.equilibrium_price) ** 2
        return kinetic + potential

    def build(self) -> Optional[CanonicalAdapterResult]:
        price = Register("price", RegisterType.CLASSICAL, 2)
        momentum = Register("momentum", RegisterType.CLASSICAL, 2)

        energy_levels = np.array([0.0, 1.0])
        H_price = CanonicalHamiltonians.H_state(price, energy_levels)
        H_momentum = CanonicalHamiltonians.H_state(momentum, energy_levels)
        H_coupling = CanonicalHamiltonians.H_interact(
            price, momentum, coupling=self.mean_reversion, interaction_type="ZZ"
        )

        program = HLProgram(
            name="market_canonical",
            registers=[price, momentum],
            hamiltonian_terms=[
                ("price_state", H_price, 1.0),
                ("momentum_state", H_momentum, 1.0),
                ("coupling", H_coupling, 1.0),
            ],
            schedule=lambda t: 1.0,
            total_time=1.0,
            dt=0.01,
        )

        return CanonicalAdapterResult(
            name=self.name,
            program=program,
            initial_q=np.array([self.equilibrium_price], dtype=float),
            initial_p=np.array([0.1], dtype=float),
            hamiltonian=self._hamiltonian,
            metadata={
                "liquidity_mass": self.liquidity_mass,
                "volatility": self.volatility,
                "mean_reversion": self.mean_reversion,
            },
        )


class BioenergeticDomainAdapter(DomainAdapter):
    """Adapter for bioenergetic consciousness Hamiltonian."""

    name = "bioenergetic_consciousness"

    def __init__(self, retention_days: float = 0.0):
        self.retention_days = retention_days

    def build(self) -> Optional[CanonicalAdapterResult]:
        try:
            from domains.bioenergetic_consciousness import BioenergticConsciousness
        except Exception:
            return None

        system = BioenergticConsciousness(retention_days=self.retention_days)

        psi = Register("psi", RegisterType.CLASSICAL, 4)
        energy = Register("energy", RegisterType.CLASSICAL, 2)

        energy_levels = np.array([0.0, 1.0, 2.0, 3.0])
        H_psi = CanonicalHamiltonians.H_state(psi, energy_levels)
        H_energy = CanonicalHamiltonians.H_state(energy, np.array([0.0, 1.0]))
        H_coupling = CanonicalHamiltonians.H_interact(
            psi, energy, coupling=0.25, interaction_type="ZZ"
        )

        program = HLProgram(
            name="bioenergetic_canonical",
            registers=[psi, energy],
            hamiltonian_terms=[
                ("psi_state", H_psi, 1.0),
                ("energy_state", H_energy, 1.0),
                ("coupling", H_coupling, 1.0),
            ],
            schedule=lambda t: 1.0,
            total_time=1.0,
            dt=0.01,
        )

        initial_q = np.array([0.1, -0.1, 0.2, -0.05, system.baseline_energy], dtype=float)
        initial_p = np.array([0.05, -0.02, 0.01, 0.03, 0.0], dtype=float)

        return CanonicalAdapterResult(
            name=self.name,
            program=program,
            initial_q=initial_q,
            initial_p=initial_p,
            hamiltonian=system.hamiltonian,
            metadata={
                "retention_days": self.retention_days,
                "baseline_energy": system.baseline_energy,
            },
        )


def default_adapters() -> List[DomainAdapter]:
    return [
        MarketDomainAdapter(),
        BioenergeticDomainAdapter(),
    ]
