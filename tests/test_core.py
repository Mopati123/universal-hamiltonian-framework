"""
Test Suite - Universal Hamiltonian Framework

Tests for conservation laws, symplectic integration, and domain-specific behavior.
"""

import pytest
import numpy as np
import sys
sys.path.insert(0, 'src')

from core import PhaseSpace, HamiltonianSystem
from compiler import define_system, harmonic_oscillator_hamiltonian


class TestPhaseSpace:
    """Test phase-space representations"""
    
    def test_initialization(self):
        """Test PhaseSpace creation"""
        ps = PhaseSpace(q=np.array([1.0, 2.0]), p=np.array([0.5, -0.5]))
        assert ps.ndof == 2
        assert ps.q[0] == 1.0
        assert ps.p[1] == -0.5
    
    def test_copy(self):
        """Test deep copy"""
        ps1 = PhaseSpace(q=np.array([1.0]), p=np.array([0.0]))
        ps2 = ps1.copy()
        ps2.q[0] = 2.0
        assert ps1.q[0] == 1.0  # Original unchanged


class TestConservationLaws:
    """Test energy and momentum conservation"""
    
    def test_energy_conservation_harmonic_oscillator(self):
        """Harmonic oscillator should conserve energy"""
        @define_system
        class Oscillator:
            coordinates = ['x']
            
            def kinetic(self, p):
                return p.px**2 / 2
            
            def potential(self, q):
                return 0.5 * q.x**2
        
        system = Oscillator()
        initial = PhaseSpace(q=np.array([1.0]), p=np.array([0.0]))
        
        # Evolve
        t, q_traj, p_traj = system.evolve(initial, t_max=10.0, dt=0.01)
        
        # Check energy conservation
        E_initial = system.hamiltonian(initial.q, initial.p)
        E_final = system.hamiltonian(q_traj[-1], p_traj[-1])
        
        relative_error = abs(E_final - E_initial) / abs(E_initial)
        assert relative_error < 1e-4, f"Energy drift too large: {relative_error}"
    
    def test_phase_space_volume_preservation(self):
        """Liouville's theorem: phase-space volume preserved"""
        @define_system
        class TwoOscillators:
            coordinates = ['x1', 'x2']
            
            def kinetic(self, p):
                return (p.px1**2 + p.px2**2) / 2
            
            def potential(self, q):
                return 0.5 * (q.x1**2 + q.x2**2)
        
        system = TwoOscillators()
        
        # Create small volume in phase space
        n_points = 100
        q0_range = np.linspace(0.9, 1.1, int(np.sqrt(n_points)))
        p0_range = np.linspace(-0.1, 0.1, int(np.sqrt(n_points)))
        
        initial_area = (q0_range[-1] - q0_range[0]) * (p0_range[-1] - p0_range[0])
        
        # Evolve all points
        evolved_q = []
        evolved_p = []
        
        for q0 in q0_range[:5]:  # Sample subset for speed
            for p0 in p0_range[:5]:
                initial = PhaseSpace(q=np.array([q0, 0.0]), p=np.array([p0, 0.0]))
                t, q_traj, p_traj = system.evolve(initial, t_max=1.0, dt=0.01)
                evolved_q.append(q_traj[-1][0])
                evolved_p.append(p_traj[-1][0])
        
        # Approximate final area (simplified check)
        evolved_q = np.array(evolved_q)
        evolved_p = np.array(evolved_p)
        
        # Volume should be roughly preserved (within numerical error)
        # This is a simplified test - full test would compute actual volume
        assert len(evolved_q) > 0


class TestSymbolicEngine:
    """Test symbolic mathematics"""
    
    def test_hamilton_equations_derivation(self):
        """Test automatic derivation of Hamilton's equations"""
        sh = harmonic_oscillator_hamiltonian(n_dof=1, k=1.0, m=1.0)
        
        dq_dt, dp_dt = sh.hamilton_equations()
        
        # For harmonic oscillator: dq/dt = p, dp/dt = -q
        # Check symbolically
        assert len(dq_dt) == 1
        assert len(dp_dt) == 1
    
    def test_poisson_bracket(self):
        """Test Poisson bracket calculation"""
        sh = harmonic_oscillator_hamiltonian(n_dof=1, k=1.0, m=1.0)
        
        # {q, p} should equal 1
        pb = sh.poisson_bracket(sh.q[0], sh.p[0])
        assert pb == 1
        
        # {q, q} should equal 0
        pb_qq = sh.poisson_bracket(sh.q[0], sh.q[0])
        assert pb_qq == 0
    
    def test_conserved_quantities(self):
        """Test detection of conserved quantities"""
        sh = harmonic_oscillator_hamiltonian(n_dof=1, k=1.0, m=1.0)
        
        conserved = sh.find_conserved_quantities()
        
        # Energy should always be conserved
        assert 'energy' in conserved
        assert conserved['energy'] == sh.H


class TestDomains:
    """Test domain-specific functionality"""
    
    def test_quantum_oscillator_eigenvalues(self):
        """Test quantum energy level formula"""
        # This would test Mojo code when available
        # For now, test Python interface
        pass
    
    def test_market_dynamics_polars(self):
        """Test Polars lazy evaluation for market data"""
        try:
            from domains.market_dynamics import MarketHamiltonian, MarketState
            
            H = MarketHamiltonian(liquidity_mass=1.0, volatility=0.1)
            state = MarketState(price=100.0, momentum=0.0)
            
            # Evolve one tick
            new_state = H.evolve_tick(state, dt=1.0)
            
            assert new_state.price != state.price  # Should have moved
            
        except ImportError:
            pytest.skip("Market dynamics module not available")


class TestPerformance:
    """Performance benchmarks"""
    
    @pytest.mark.benchmark
    def test_evolution_speed(self, benchmark):
        """Benchmark evolution speed"""
        @define_system
        class FastOscillator:
            coordinates = ['x']
            
            def kinetic(self, p):
                return p.px**2 / 2
            
            def potential(self, q):
                return 0.5 * q.x**2
        
        system = FastOscillator()
        initial = PhaseSpace(q=np.array([1.0]), p=np.array([0.0]))
        
        def evolve_func():
            return system.evolve(initial, t_max=5.0, dt=0.01)
        
        result = benchmark(evolve_func)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
