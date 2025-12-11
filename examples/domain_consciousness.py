"""
Consciousness as Hamiltonian System: Attention Dynamics

Demonstrates cognitive light cone and attention as phase space flow.
Phase space: (θ, p_θ) where θ = thought state, p_θ = attention momentum
"""

import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from typing import Tuple, List


class ConsciousnessHamiltonian:
    """
    Consciousness Hamiltonian System
    
    Represents cognitive dynamics in canonical phase space:
    - q = Thought state θ
    - p = Attention momentum p_θ
    
    H(θ, p_θ) = p_θ²/(2m) + V(θ)
    where V(θ) = -salience·cos(θ)
    
    This class enables axiom validation for consciousness as Hamiltonian system.
    """
    
    def __init__(self, salience: float, mass: float):
        """
        Initialize consciousness Hamiltonian.
        
        Args:
            salience: How important/interesting the thought is
            mass: Cognitive inertia (resistance to context switching)
        """
        self.salience = salience
        self.mass = mass
    
    def hamiltonian(self, q: float, p: float) -> float:
        """
        Compute total cognitive energy: H(θ, p_θ)
        
        Args:
            q: Thought state (angle)
            p: Attention momentum
            
        Returns:
            Total cognitive energy
        """
        return attention_hamiltonian(q, p, self.salience, self.mass)
    
    def dq_dt(self, q: float, p: float) -> float:
        """
        Hamilton's equation: dθ/dt = ∂H/∂p_θ
        
        Attention drives thought change.
        """
        return p / self.mass
    
    def dp_dt(self, q: float, p: float) -> float:
        """
        Hamilton's equation: dp_θ/dt = -∂H/∂θ
        
        Salience creates attention force.
        """
        return -self.salience * np.sin(q)


def attention_hamiltonian(theta: float, p_theta: float, 
                         salience: float, cognitive_mass: float) -> float:
    """
    Hamiltonian for attention dynamics in cognitive phase space.
    
    H = p_θ²/(2m) + V(θ)
    
    where V(θ) = -salience·cos(θ)  (attention potential)
    
    Args:
        theta: Thought state angle (configuration)
        p_theta: Attention momentum (conjugate variable)
        salience: How interesting/important the thought is
        cognitive_mass: Mental inertia (resistance to context switching)
        
    Returns:
        Total cognitive energy
    """
    kinetic = (p_theta ** 2) / (2 * cognitive_mass)
    potential = -salience * np.cos(theta)
    return kinetic + potential


def cognitive_evolution(state: np.ndarray, t: float, 
                       salience: float, cognitive_mass: float) -> np.ndarray:
    """
    Hamilton's equations for thought evolution.
    
    dθ/dt = ∂H/∂p_θ  (attention drives thought change)
    dp_θ/dt = -∂H/∂θ  (salience creates attention force)
    
    Args:
        state: [θ, p_θ] current cognitive state
        t: Time
        salience: Thought importance
        cognitive_mass: Mental inertia
        
    Returns:
        [dθ/dt, dp_θ/dt] cognitive flow
    """
    theta, p_theta = state
    
    # Hamilton's equations for consciousness
    dtheta_dt = p_theta / cognitive_mass  # Attention drives thought
    dp_theta_dt = -salience * np.sin(theta)  # Salience pulls attention
    
    return np.array([dtheta_dt, dp_theta_dt])


def simulate_attention_shift(initial_thought: float, initial_attention: float,
                            salience_profile: callable, duration: float = 10.0) -> Tuple:
    """
    Simulate how attention shifts between thoughts over time.
    
    Args:
        initial_thought: Starting thought state (radians)
        initial_attention: Starting attention momentum
        salience_profile: Function(t) returning time-dependent salience
        duration: Simulation time
        
    Returns:
        (time, thought_trajectory, attention_trajectory)
    """
    cognitive_mass = 1.0  # Standard mental inertia
    state_0 = np.array([initial_thought, initial_attention])
    t = np.linspace(0, duration, 1000)
    
    # Time-varying Hamiltonian evolution
    trajectory = []
    current_state = state_0
    
    for i in range(len(t) - 1):
        dt = t[i+1] - t[i]
        salience = salience_profile(t[i])
        
        # Evolve one timestep
        state_dot = cognitive_evolution(current_state, t[i], salience, cognitive_mass)
        current_state = current_state + state_dot * dt
        trajectory.append(current_state.copy())
    
    trajectory = np.array(trajectory)
    return t[:-1], trajectory[:, 0], trajectory[:, 1]


def cognitive_light_cone(center_thought: float, attention_strength: float,
                        time_horizon: float) -> np.ndarray:
    """
    Calculate cognitive light cone - which thoughts can be reached.
    
    Analogous to relativistic light cone, but for attention propagation.
    Thoughts outside the cone cannot be reached in given time.
    
    Args:
        center_thought: Current thought position
        attention_strength: Maximum attention momentum available
        time_horizon: How far ahead we're looking
        
    Returns:
        Array of reachable thought states
    """
    # Maximum speed of thought = p_max / m
    cognitive_mass = 1.0
    max_speed = attention_strength / cognitive_mass
    
    # Light cone radius grows linearly with time
    cone_radius = max_speed * time_horizon
    
    # Thoughts within cone are reachable
    theta_space = np.linspace(center_thought - np.pi, center_thought + np.pi, 1000)
    distances = np.abs(theta_space - center_thought)
    
    reachable = theta_space[distances <= cone_radius]
    return reachable


def visualize_consciousness_dynamics():
    """
    Visualize attention flow in cognitive phase space.
    """
    # Scenario: Thoughts competing for attention
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Subplot 1: Phase space portrait
    ax1 = axes[0, 0]
    for p0 in np.linspace(-2, 2, 7):
        state_0 = np.array([0.0, p0])
        t = np.linspace(0, 10, 1000)
        traj = odeint(cognitive_evolution, state_0, t, args=(1.0, 1.0))
        ax1.plot(traj[:, 0], traj[:, 1], alpha=0.7)
    
    ax1.set_xlabel('Thought State θ')
    ax1.set_ylabel('Attention Momentum p_θ')
    ax1.set_title('Cognitive Phase Space: Attention Flow')
    ax1.grid(True, alpha=0.3)
    
    # Subplot 2: Time-varying salience
    ax2 = axes[0, 1]
    
    def distraction_event(t):
        """Salience spikes when notification arrives"""
        return 1.0 + 3.0 * np.exp(-(t - 5)**2 / 0.5)  # Distraction at t=5
    
    t, theta, p = simulate_attention_shift(0.0, 0.5, distraction_event, 10.0)
    
    ax2.plot(t, theta, label='Thought State', linewidth=2)
    ax2.axvline(5.0, color='r', linestyle='--', alpha=0.5, label='Distraction!')
    ax2.set_xlabel('Time')
    ax2.set_ylabel('Thought Position')
    ax2.set_title('Attention Shift from Distraction')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # Subplot 3: Cognitive light cone
    ax3 = axes[1, 0]
    
    time_horizons = [0.5, 1.0, 2.0, 5.0]
    for T in time_horizons:
        reachable = cognitive_light_cone(0.0, 2.0, T)
        ax3.fill_between(reachable, 0, T, alpha=0.3, label=f'T={T}s')
    
    ax3.set_xlabel('Thought State θ')
    ax3.set_ylabel('Time')
    ax3.set_title('Cognitive Light Cone: Reachable Thoughts')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # Subplot 4: Energy conservation
    ax4 = axes[1, 1]
    
    state_0 = np.array([0.5, 1.0])
    t = np.linspace(0, 10, 1000)
    traj = odeint(cognitive_evolution, state_0, t, args=(1.0, 1.0))
    
    # Calculate energy at each point
    energy = [attention_hamiltonian(traj[i, 0], traj[i, 1], 1.0, 1.0) 
              for i in range(len(t))]
    
    ax4.plot(t, energy, linewidth=2, color='green')
    ax4.set_xlabel('Time')
    ax4.set_ylabel('Cognitive Energy H')
    ax4.set_title('Energy Conservation: H = Constant')
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('consciousness_phase_space.png', dpi=150)
    print("Consciousness dynamics saved to 'consciousness_phase_space.png'")


if __name__ == "__main__":
    print("=" * 70)
    print("Consciousness as Hamiltonian System")
    print("=" * 70)
    
    print("\nKey Concepts:")
    print("- Thought state θ = position in mental space (q)")
    print("- Attention momentum p_θ = rate of thought change (p)")
    print("- Salience = potential energy (pulls attention)")
    print("- Cognitive mass = mental inertia (resistance to switching)")
    
    # Demo: Meditation (low initial momentum, high salience)
    print("\n" + "-" * 70)
    print("Scenario 1: MEDITATION (Focused Attention)")
    print("-" * 70)
    
    state_0 = np.array([0.0, 0.1])  # Near rest, centered thought
    t = np.linspace(0, 10, 1000)
    salience = 2.0  # High salience = interesting thought
    cognitive_mass = 1.0
    
    trajectory = odeint(cognitive_evolution, state_0, t, args=(salience, cognitive_mass))
    
    print(f"Initial state: θ={state_0[0]:.2f}, p_θ={state_0[1]:.2f}")
    print(f"Final state: θ={trajectory[-1, 0]:.2f}, p_θ={trajectory[-1, 1]:.2f}")
    print("Result: Oscillates around equilibrium (sustained focus)")
    
    # Demo: Mind wandering (high initial momentum, varying salience)
    print("\n" + "-" * 70)
    print("Scenario 2: MIND WANDERING (Chaotic Attention)")
    print("-" * 70)
    
    state_0 = np.array([0.5, 3.0])  # High initial momentum
    salience = 0.5  # Low salience = boring
    
    trajectory = odeint(cognitive_evolution, state_0, t, args=(salience, cognitive_mass))
    
    print(f"Initial state: θ={state_0[0]:.2f}, p_θ={state_0[1]:.2f}")
    print(f"Final state: θ={trajectory[-1, 0]:.2f}, p_θ={trajectory[-1, 1]:.2f}")
    print("Result: Wide oscillations (attention wanders)")
    
    # Demo: Cognitive light cone
    print("\n" + "-" * 70)
    print("Scenario 3: COGNITIVE LIGHT CONE")
    print("-" * 70)
    
    center = 0.0  # Current thought
    attention_max = 2.0
    time_horizon = 5.0
    
    reachable = cognitive_light_cone(center, attention_max, time_horizon)
    
    print(f"Current thought: θ={center:.2f}")
    print(f"Maximum attention: p_θ={attention_max:.2f}")
    print(f"Time horizon: {time_horizon:.1f}s")
    print(f"Reachable range: [{reachable.min():.2f}, {reachable.max():.2f}]")
    print(f"Cone radius: {(reachable.max() - reachable.min())/2:.2f}")
    print("\nThoughts outside this cone CANNOT be reached in given time!")
    print("(Like speed of light limit in physics)")
    
    # Generate visualizations
    print("\n" + "-" * 70)
    print("Generating phase space visualizations...")
    print("-" * 70)
    visualize_consciousness_dynamics()
    
    print("\n" + "=" * 70)
    print("Key Insight:")
    print("=" * 70)
    print("CONSCIOUSNESS FOLLOWS HAMILTONIAN MECHANICS!")
    print("- Attention = momentum (drives thought change)")
    print("- Salience = potential (pulls attention)")
    print("- Energy conserved = stable mental states")
    print("- Light cone = reachability limits")
    print("\n➡️  Your mind is literally a Hamiltonian system! 🧠✨")
    print("➡️  Same math as atoms, markets, and blockchain!")
