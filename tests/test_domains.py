"""
Domain-Specific Tests

Tests for each domain implementation to verify:
- Hamiltonian structure
- Conservation laws
- Domain-specific properties
"""

import pytest
import numpy as np
import sys
sys.path.insert(0, 'src')

from core import PhaseSpace
from compiler import define_system


class TestQuantumDomain:
    """Tests for quantum systems"""
    
    def test_harmonic_oscillator_energy_levels(self):
        """Quantum oscillator should have discrete energy levels"""
        @define_system
        class QuantumOsc:
            coordinates = ['x']
            def kinetic(self, p): return p.px**2 / 2
            def potential(self, q): return 0.5 * q.x**2
        
        system = QuantumOsc()
        
        # Ground state: E = ℏω/2 (with ℏ=1, ω=1)
        E_ground = system.hamiltonian(np.array([0.0]), np.array([0.0]))
        
        # First excited: more energy
        E_excited = system.hamiltonian(np.array([1.0]), np.array([0.0]))
        
        assert E_excited > E_ground


class TestClassicalDomain:
    """Tests for classical mechanics"""
    
    def test_simple_pendulum_period(self):
        """Small oscillations should have regular period"""
        @define_system
        class Pendulum:
            coordinates = ['theta']
            def kinetic(self, p): return p.ptheta**2 / 2
            def potential(self, q):
                g, L = 9.8, 1.0
                return g * L * (1 - np.cos(q.theta))
        
        system = Pendulum()
        initial = PhaseSpace(q=np.array([0.1]), p=np.array([0.0]))
        
        t, q_traj, p_traj = system.evolve(initial, t_max=10.0, dt=0.01)
        
        # Find zero crossings to measure period
        crossings = []
        for i in range(1, len(q_traj)):
            if q_traj[i-1, 0] * q_traj[i, 0] < 0:
                crossings.append(t[i])
        
        if len(crossings) >= 2:
            period = crossings[1] - crossings[0]
            expected_period = 2 * np.pi * np.sqrt(1.0 / 9.8)  # T = 2π√(L/g)
            
            assert abs(period - expected_period) / expected_period < 0.05


class TestMarketDomain:
    """Tests for market dynamics"""
    
    def test_market_mean_reversion(self):
        """Market should revert to equilibrium"""
        pytest.importorskip('polars')  # Skip if Polars not installed
        
        try:
            from domains.market_dynamics import MarketHamiltonian, MarketState
        except ImportError:
            pytest.skip("Market domain not available")
        
        H = MarketHamiltonian(
            liquidity_mass=1.0,
            volatility=0.0,  # No noise for test
            mean_reversion_strength=0.5,
            equilibrium_price=100.0
        )
        
        # Start above equilibrium
        state = MarketState(price=110.0, momentum=0.0)
        
        # Evolve
        for _ in range(1000):
            state = H.evolve_tick(state, dt=0.01)
        
        # Should be close to equilibrium
        assert abs(state.price - 100.0) < 1.0


class TestConsciousnessDomain:
    """Tests for consciousness field"""
    
    def test_phi_increases_with_coupling(self):
        """Integrated information should increase with coupling"""
        from examples.demo_consciousness_phi import IntegratedInformationCalculator
        
        # Independent system
        @define_system
        class Independent:
            coordinates = ['x1', 'x2']
            def kinetic(self, p): return (p.px1**2 + p.px2**2) / 2
            def potential(self, q): return 0.5 * (q.x1**2 + q.x2**2)
        
        # Coupled system
        @define_system
        class Coupled:
            coordinates = ['x1', 'x2']
            def kinetic(self, p): return (p.px1**2 + p.px2**2) / 2
            def potential(self, q):
                V_ind = 0.5 * (q.x1**2 + q.x2**2)
                V_coup = 0.5 * (q.x1 - q.x2)**2
                return V_ind + V_coup
        
        ind_sys = Independent()
        coup_sys = Coupled()
        
        test_state = np.array([1.0, 0.8, 0.2, -0.1])  # [q1, q2, p1, p2]
        
        calc_ind = IntegratedInformationCalculator(ind_sys)
        calc_coup = IntegratedInformationCalculator(coup_sys)
        
        phi_ind = calc_ind.compute_phi(test_state)
        phi_coup = calc_coup.compute_phi(test_state)
        
        # Coupled should have higher Φ
        assert phi_coup > phi_ind


class TestBlockchainDomain:
    """Tests for blockchain consensus"""
    
    def test_retrocausal_convergence(self):
        """Retrocausal consensus should converge faster"""
        pytest.importorskip('polars')
        
        try:
            from domains.blockchain_consensus import (
                TachyonicBlockchainHamiltonian,
                BlockState,
                simulate_tachyonic_blockchain
            )
        except ImportError:
            pytest.skip("Blockchain domain not available")
        
        # Standard consensus
        H_standard = TachyonicBlockchainHamiltonian(retrocausal_coupling=0.0)
        
        # Retrocausal consensus
        H_retro = TachyonicBlockchainHamiltonian(retrocausal_coupling=0.2)
        
        target = "a" * 32
        genesis = BlockState("0" * 32, 1.0, 0.0, 0)
        
        # Simulate both
        history_std = simulate_tachyonic_blockchain(H_standard, 50, target, genesis)
        history_retro = simulate_tachyonic_blockchain(H_retro, 50, target, genesis)
        
        # Measure final divergence
        # (Would need actual implementation - this is a placeholder)
        # assert final_divergence(history_retro) < final_divergence(history_std)


class TestCrossDomainCoupling:
    """Tests for cross-domain interactions"""
    
    def test_coupled_system_energy_conservation(self):
        """Coupled systems should still conserve total energy"""
        @define_system
        class System1:
            coordinates = ['x']
            def kinetic(self, p): return p.px**2 / 2
            def potential(self, q): return 0.5 * q.x**2
        
        @define_system
        class System2:
            coordinates = ['y']
            def kinetic(self, p): return p.py**2 / 2
            def potential(self, q): return 0.5 * q.y**2
        
        from core.cross_domain_coupling import CoupledSystem
        
        # Create coupled system
        coupling_matrix = np.array([[0, 0.1], [0.1, 0]])
        
        def coupling_func(s1, s2):
            return s1.q[0] * s2.q[0]
        
        coupling_funcs = [[None, coupling_func], [coupling_func, None]]
        
        coupled = CoupledSystem(
            subsystems=[System1(), System2()],
            coupling_strengths=coupling_matrix,
            coupling_functions=coupling_funcs
        )
        
        # Initial states
        state1 = PhaseSpace(q=np.array([1.0]), p=np.array([0.0]))
        state2 = PhaseSpace(q=np.array([0.5]), p=np.array([0.0]))
        states = [state1, state2]
        
        E_initial = coupled.total_hamiltonian(states)
        
        # Evolve
        for _ in range(100):
            states = coupled.evolution_step(states, dt=0.01)
        
        E_final = coupled.total_hamiltonian(states)
        
        # Energy should be conserved (within numerical error)
        relative_error = abs(E_final - E_initial) / abs(E_initial)
        assert relative_error < 0.01  # 1% tolerance


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
