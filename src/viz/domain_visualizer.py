"""
Domain Visualizer - Automatic visualization for ANY Hamiltonian system

This module creates the coupling between visualization layer and domain layer.
It automatically detects domain type and creates appropriate visualizations.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from typing import Any, Optional, List, Tuple

from .theme import apply_matplotlib_theme, DOMAIN_COLORS, QUANTUM_PALETTE


class DomainVisualizer:
    """
    Automatically visualize any domain Hamiltonian.
    
    Detects domain type and creates appropriate plots:
    - Quantum: Wavefunction, energy levels
    - Classical: Trajectories, phase portraits
    - Market: Price evolution, order book
    - Consciousness: Neural field, Φ visualization
    - Blockchain: Consensus convergence, retrocausality
    """
    
    def __init__(self, domain, domain_type: Optional[str] = None):
        """
        Args:
            domain: Domain Hamiltonian instance
            domain_type: Override auto-detection ('quantum', 'classical', etc.)
        """
        self.domain = domain
        self.domain_type = domain_type or self._detect_domain_type()
        self.colors = DOMAIN_COLORS.get(self.domain_type, DOMAIN_COLORS['quantum'])
        
        # Apply theme
        apply_matplotlib_theme()
    
    def _detect_domain_type(self) -> str:
        """Auto-detect domain type from class name"""
        class_name = self.domain.__class__.__name__.lower()
        
        if 'quantum' in class_name or 'wavefunction' in class_name:
            return 'quantum'
        elif 'market' in class_name or 'price' in class_name:
            return 'market'
        elif 'consciousness' in class_name or 'neural' in class_name:
            return 'consciousness'
        elif 'blockchain' in class_name or 'consensus' in class_name:
            return 'blockchain'
        else:
            return 'classical'
    
    def interactive_explore(self, initial_state=None, t_max=10.0, dt=0.01):
        """
        Create interactive exploration interface.
        
        Automatically chooses appropriate visualization based on domain.
        """
        if self.domain_type == 'quantum':
            self._quantum_visualizer(initial_state, t_max, dt)
        elif self.domain_type == 'market':
            self._market_visualizer(initial_state, t_max, dt)
        elif self.domain_type == 'consciousness':
            self._consciousness_visualizer(initial_state, t_max, dt)
        elif self.domain_type == 'blockchain':
            self._blockchain_visualizer(initial_state, t_max, dt)
        else:
            self._classical_visualizer(initial_state, t_max, dt)
    
    def _classical_visualizer(self, initial_state, t_max, dt):
        """Visualize classical Hamiltonian system"""
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle(f'{self.domain.__class__.__name__} - Phase Space Evolution',
                     color=self.colors['primary'], fontsize=16, fontweight='bold')
        
        # Evolve system
        if hasattr(self.domain, 'evolve'):
            t, q_traj, p_traj = self.domain.evolve(initial_state, t_max, dt)
        else:
            # Manual evolution
            from core import PhaseSpace
            states = [initial_state]
            times = [0]
            
            for step in range(int(t_max / dt)):
                if hasattr(self.domain, '_verlet_step'):
                    new_state = self.domain._verlet_step(states[-1], dt)
                    states.append(new_state)
                    times.append(times[-1] + dt)
            
            t = np.array(times)
            q_traj = np.array([s.q for s in states])
            p_traj = np.array([s.p for s in states])
        
        # Phase portrait
        ax_phase = axes[0, 0]
        for i in range(q_traj.shape[1]):
            ax_phase.plot(q_traj[:, i], p_traj[:, i], 
                         color=self.colors['primary'], alpha=0.7, linewidth=2)
        ax_phase.set_xlabel('Position q', fontsize=12)
        ax_phase.set_ylabel('Momentum p', fontsize=12)
        ax_phase.set_title('Phase Portrait', fontweight='bold')
        ax_phase.grid(alpha=0.3)
        
        # Position vs time
        ax_q = axes[0, 1]
        for i in range(q_traj.shape[1]):
            ax_q.plot(t, q_traj[:, i], color=self.colors['secondary'], linewidth=2)
        ax_q.set_xlabel('Time', fontsize=12)
        ax_q.set_ylabel('Position q(t)', fontsize=12)
        ax_q.set_title('Position Evolution', fontweight='bold')
        ax_q.grid(alpha=0.3)
        
        # Momentum vs time
        ax_p = axes[1, 0]
        for i in range(p_traj.shape[1]):
            ax_p.plot(t, p_traj[:, i], color=self.colors['accent'], linewidth=2)
        ax_p.set_xlabel('Time', fontsize=12)
        ax_p.set_ylabel('Momentum p(t)', fontsize=12)
        ax_p.set_title('Momentum Evolution', fontweight='bold')
        ax_p.grid(alpha=0.3)
        
        # Energy conservation
        ax_E = axes[1, 1]
        if hasattr(self.domain, 'hamiltonian'):
            energies = [self.domain.hamiltonian(q_traj[i], p_traj[i]) 
                       for i in range(len(t))]
            ax_E.plot(t, energies, color=QUANTUM_PALETTE['energy'], linewidth=2)
            ax_E.axhline(energies[0], linestyle='--', color='white', alpha=0.5)
            ax_E.set_ylabel('Energy H', fontsize=12)
        ax_E.set_xlabel('Time', fontsize=12)
        ax_E.set_title('Energy Conservation', fontweight='bold')
        ax_E.grid(alpha=0.3)
        
        plt.tight_layout()
        plt.show()
    
    def _market_visualizer(self, initial_state, t_max, dt):
        """Visualize market dynamics"""
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('Market Hamiltonian Dynamics',
                     color=DOMAIN_COLORS['market']['primary'], 
                     fontsize=16, fontweight='bold')
        
        # Evolve market
        states = [initial_state]
        for _ in range(int(t_max / dt)):
            if hasattr(self.domain, 'evolve_tick'):
                new_state = self.domain.evolve_tick(states[-1], dt)
                states.append(new_state)
        
        times = np.arange(len(states)) * dt
        prices = [s.price if hasattr(s, 'price') else s.q[0] for s in states]
        momenta = [s.momentum if hasattr(s, 'momentum') else s.p[0] for s in states]
        
        # Price evolution
        axes[0, 0].plot(times, prices, color=DOMAIN_COLORS['market']['primary'], linewidth=2)
        if hasattr(self.domain, 'p_eq'):
            axes[0, 0].axhline(self.domain.p_eq, linestyle='--', color='white', alpha=0.5)
        axes[0, 0].set_xlabel('Time (ticks)')
        axes[0, 0].set_ylabel('Price')
        axes[0, 0].set_title('Price Evolution')
        axes[0, 0].grid(alpha=0.3)
        
        # Momentum (order flow)
        axes[0, 1].plot(times, momenta, color=DOMAIN_COLORS['market']['secondary'], linewidth=2)
        axes[0, 1].set_xlabel('Time (ticks)')
        axes[0, 1].set_ylabel('Momentum')
        axes[0, 1].set_title('Order Flow')
        axes[0, 1].grid(alpha=0.3)
        
        # Phase space
        axes[1, 0].plot(prices, momenta, color=DOMAIN_COLORS['market']['accent'], linewidth=2)
        axes[1, 0].set_xlabel('Price')
        axes[1, 0].set_ylabel('Momentum')
        axes[1, 0].set_title('Market Phase Portrait')
        axes[1, 0].grid(alpha=0.3)
        
        # Returns distribution
        returns = np.diff(prices) / np.array(prices[:-1])
        axes[1, 1].hist(returns, bins=30, color=DOMAIN_COLORS['market']['primary'], alpha=0.7)
        axes[1, 1].set_xlabel('Returns')
        axes[1, 1].set_ylabel('Frequency')
        axes[1, 1].set_title('Returns Distribution')
        axes[1, 1].grid(alpha=0.3)
        
        plt.tight_layout()
        plt.show()
    
    def _quantum_visualizer(self, initial_state, t_max, dt):
        """Visualize quantum system"""
        print(f"Quantum visualization for {self.domain.__class__.__name__}")
        print("(Quantum wavefunction visualization - coming soon)")
        self._classical_visualizer(initial_state, t_max, dt)
    
    def _consciousness_visualizer(self, initial_state, t_max, dt):
        """Visualize consciousness field"""
        print(f"Consciousness visualization for {self.domain.__class__.__name__}")
        print("(Neural field + Φ computation - coming soon)")
        self._classical_visualizer(initial_state, t_max, dt)
    
    def _blockchain_visualizer(self, initial_state, t_max, dt):
        """Visualize blockchain consensus"""
        print(f"Blockchain visualization for {self.domain.__class__.__name__}")
        print("(Retrocausal consensus plots - coming soon)")
        self._classical_visualizer(initial_state, t_max, dt)


# Convenience function
def visualize_domain(domain, initial_state=None, **kwargs):
    """
    Quick visualization of any domain.
    
    Example:
        from domains import MarketHamiltonian
        from viz import visualize_domain
        
        market = MarketHamiltonian()
        visualize_domain(market, initial_state=...)
    """
    viz = DomainVisualizer(domain)
    viz.interactive_explore(initial_state, **kwargs)


__all__ = ['DomainVisualizer', 'visualize_domain']
