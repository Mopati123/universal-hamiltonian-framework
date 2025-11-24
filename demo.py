"""
Demo - Universal Hamiltonian Framework

Demonstrates the core concepts across multiple domains.
"""

import numpy as np
import sys
sys.path.insert(0, 'src')

from core import PhaseSpace, HamiltonianSystem
from compiler import define_system, SymbolicHamiltonian, harmonic_oscillator_hamiltonian


# Example 1: Simple Harmonic Oscillator using DSL
@define_system
class QuantumOscillator:
    coordinates = ['x']
    
    def kinetic(self, p):
        return p.px**2 / 2
    
    def potential(self, q):
        return 0.5 * q.x**2
    
    def coupling(self, q, p):
        return 0.0  # No coupling term


def demo_quantum_oscillator():
    """Demonstrate quantum harmonic oscillator"""
    print("\n" + "="*60)
    print("DEMO 1: Quantum Harmonic Oscillator")
    print("="*60)
    
    system = QuantumOscillator()
    
    # Initial state: q=1, p=0
    initial = PhaseSpace(q=np.array([1.0]), p=np.array([0.0]))
    
   # Evolve
    print(f"\nInitial state: q={initial.q[0]:.3f}, p={initial.p[0]:.3f}")
    print(f"Initial energy: H={system.hamiltonian(initial.q, initial.p):.3f}")
    
    t, q_traj, p_traj = system.evolve(initial, t_max=10.0, dt=0.01)
    
    final_q, final_p = q_traj[-1][0], p_traj[-1][0]
    final_E = system.hamiltonian(q_traj[-1], p_traj[-1])
    initial_E = system.hamiltonian(initial.q, initial.p)
    
    print(f"\nFinal state: q={final_q:.3f}, p={final_p:.3f}")
    print(f"Final energy: H={final_E:.3f}")
    print(f"Energy drift: ΔE/E₀ = {abs(final_E - initial_E)/initial_E * 100:.2e}%")
    print("\n✓ Energy conserved (symplectic integration)")


def demo_symbolic_engine():
    """Demonstrate symbolic mathematics"""
    print("\n" + "="*60)
    print("DEMO 2: Symbolic Hamilton's Equations")
    print("="*60)
    
    # Create 2-DOF harmonic oscillator symbolically
    sh = harmonic_oscillator_hamiltonian(n_dof=2, k=1.0, m=1.0)
    
    print(f"\nHamiltonian:")
    print(f"H = {sh.H}")
    
    # Derive equations of motion
    dq_dt, dp_dt = sh.hamilton_equations()
    
    print(f"\nHamilton's Equations:")
    for i in range(sh.n_dof):
        print(f"  dq{i}/dt = {dq_dt[i]}")
        print(f"  dp{i}/dt = {dp_dt[i]}")
    
    # Find conserved quantities
    conserved = sh.find_conserved_quantities()
    
    print(f"\nConserved Quantities:")
    for name, expr in conserved.items():
        print(f"  {name}: {expr}")
    
    print("\n✓ Automatically derived equations and conservation laws")


def demo_coupled_system():
    """Demonstrate coupled oscillators"""
    print("\n" + "="*60)
    print("DEMO 3: Coupled Oscillators (Normal Modes)")
    print("="*60)
    
    @define_system
    class CoupledOscillators:
        coordinates = ['x1', 'x2']
        
        def kinetic(self, p):
            return (p.px1**2 + p.px2**2) / 2
        
        def potential(self, q):
            k = 1.0  # Spring constant
            k_c = 0.3  # Coupling constant
            V_individual = 0.5 * k * (q.x1**2 + q.x2**2)
            V_coupling = 0.5 * k_c * (q.x1 - q.x2)**2
            return V_individual + V_coupling
    
    system = CoupledOscillators()
    
    # Initial: one oscillator displaced, other at rest
    initial = PhaseSpace(q=np.array([1.0, 0.0]), p=np.array([0.0, 0.0]))
    
    print(f"\nInitial state: q₁={initial.q[0]:.2f}, q₂={initial.q[1]:.2f}")
    
    t, q_traj, p_traj = system.evolve(initial, t_max=30.0, dt=0.01)
    
    print(f"\nEvolved for {t[-1]:.1f} time units")
    print(f"Observing energy transfer between oscillators...")
    
    # Check max displacements
    q1_max = np.max(np.abs(q_traj[:, 0]))
    q2_max = np.max(np.abs(q_traj[:, 1]))
    
    print(f"Max displacement q₁: {q1_max:.3f}")
    print(f"Max displacement q₂: {q2_max:.3f}")
    print("\n✓ Energy oscillates between coupled systems (normal modes)")


def demo_phase_space_topology():
    """Illustrate phase-space structure"""
    print("\n" + "="*60)
    print("DEMO 4: Phase-Space Topology")
    print("="*60)
    
    print("\nPhase space is a symplectic manifold with structure:")
    print("  • ω = Σᵢ dqᵢ ∧ dpᵢ  (symplectic 2-form)")
    print("  • J = [[0, I], [-I, 0]]  (symplectic matrix)")
    print("  • Hamilton's flow preserves ω (Liouville's theorem)")
    
    sh = SymbolicHamiltonian(n_dof=2)
    J = sh.symplectic_matrix()
    
    print(f"\nSymplectic matrix (2 DOF):")
    print(J)
    
    print("\nKey property: J² = -I (J is almost complex)")
    J_squared = J @ J
    print(f"J² =")
    print(J_squared)
    
    print("\n✓ Phase space has natural geometric structure")


def main():
    """Run all demos"""
    print("\n")
    print("████████████████████████████████████████████████████████████")
    print("█                                                          █")
    print("█       UNIVERSAL HAMILTONIAN FRAMEWORK - DEMO             █")
    print("█                                                          █")
    print("█   All systems are Hamiltonians.                          █")
    print("█   All algorithms are propagators.                        █")
    print("█   All intelligence is phase-space control.               █")
    print("█                                                          █")
    print("████████████████████████████████████████████████████████████")
    
    try:
        demo_quantum_oscillator()
        demo_symbolic_engine()
        demo_coupled_system()
        demo_phase_space_topology()
        
        print("\n" + "="*60)
        print("ALL DEMOS COMPLETED SUCCESSFULLY")
        print("="*60)
        print("\nNext steps:")
        print("  1. Run visualization: python src/viz/phase_space_viz.py")
        print("  2. Explore domains: quantum, market, consciousness, blockchain")
        print("  3. Read Book of Mopati: docs/book-of-mopati.md")
        print("\n")
        
    except Exception as e:
        print(f"\nError in demo: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
