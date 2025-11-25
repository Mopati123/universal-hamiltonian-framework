# Tutorial 1: Getting Started with Universal Hamiltonian Framework

This notebook introduces the core concepts of the Universal Hamiltonian Framework through hands-on examples.

## Philosophy

> "Everything that exists can be expressed as a Hamiltonian."

Any system with:
- **Degrees of freedom** (q): configurations
- **Conjugate momenta** (p): rates of change
- **Energy function** H(q, p)

...can be modeled and controlled using this framework.

---

## Setup

```python
import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, '../src')

from core import PhaseSpace, HamiltonianSystem
from compiler import define_system, harmonic_oscillator_hamiltonian

# Plotting style
plt.style.use('dark_background')
```

---

## Example 1: Simple Harmonic Oscillator

The harmonic oscillator is the "hydrogen atom" of Hamiltonian mechanics.

### Define the System

```python
@define_system
class SimpleOscillator:
    """
    Spring-mass system: F = -kx
    H = p²/(2m) + ½kx²
    """
    coordinates = ['x']
    
    def kinetic(self, p):
        return p.px**2 / 2  # m = 1
    
    def potential(self, q):
        return 0.5 * q.x**2  # k = 1

# Create system
system = SimpleOscillator()
```

### Evolve the System

```python
# Initial condition: displaced spring at rest
initial = PhaseSpace(q=np.array([1.0]), p=np.array([0.0]))

# Evolve through time
t, q_traj, p_traj = system.evolve(initial, t_max=20.0, dt=0.01)

# Visualize
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# Position vs Time
axes[0, 0].plot(t, q_traj[:, 0], color='#ff6b6b', linewidth=2)
axes[0, 0].set_xlabel('Time')
axes[0, 0].set_ylabel('Position q(t)')
axes[0, 0].set_title('Time Evolution')
axes[0, 0].grid(alpha=0.3)

# Momentum vs Time
axes[0, 1].plot(t, p_traj[:, 0], color='#4ecdc4', linewidth=2)
axes[0, 1].set_xlabel('Time')
axes[0, 1].set_ylabel('Momentum p(t)')
axes[0, 1].set_title('Momentum Evolution')
axes[0, 1].grid(alpha=0.3)

# Phase Portrait
axes[1, 0].plot(q_traj[:, 0], p_traj[:, 0], color='#00d4ff', linewidth=2)
axes[1, 0].scatter(q_traj[0, 0], p_traj[0, 0], color='#00ff00', s=100, label='Start', zorder=5)
axes[1, 0].scatter(q_traj[-1, 0], p_traj[-1, 0], color='#ff0000', s=100, label='End', zorder=5)
axes[1, 0].set_xlabel('Position q')
axes[1, 0].set_ylabel('Momentum p')
axes[1, 0].set_title('Phase Portrait')
axes[1, 0].legend()
axes[1, 0].grid(alpha=0.3)
axes[1, 0].set_aspect('equal')

# Energy Conservation
E = np.array([system.hamiltonian(q_traj[i], p_traj[i]) for i in range(len(t))])
axes[1, 1].plot(t, E, color='#ffd93d', linewidth=2)
axes[1, 1].axhline(E[0], color='white', linestyle='--', alpha=0.5, label='Initial Energy')
axes[1, 1].set_xlabel('Time')
axes[1, 1].set_ylabel('Energy H(q, p)')
axes[1, 1].set_title('Energy Conservation')
axes[1, 1].legend()
axes[1, 1].grid(alpha=0.3)

plt.tight_layout()
plt.savefig('oscillator_evolution.png', dpi=150, bbox_inches='tight')
plt.show()

# Check conservation
E_drift = (E[-1] - E[0]) / E[0]
print(f"Energy conservation: ΔE/E₀ = {E_drift:.2e}")
```

**Key Observation**: The phase portrait is a **perfect ellipse** - this is the signature of Hamiltonian dynamics!

---

## Example 2: Coupled Oscillators (Normal Modes)

Two springs connected together demonstrate **emergent behavior**.

```python
@define_system
class CoupledOscillators:
    """
    Two masses connected by springs
    Energy transfers between them
    """
    coordinates = ['x1', 'x2']
    
    def kinetic(self, p):
        return (p.px1**2 + p.px2**2) / 2
    
    def potential(self, q):
        k = 1.0  # Individual spring
        k_c = 0.3  # Coupling spring
        
        V_individual = 0.5 * k * (q.x1**2 + q.x2**2)
        V_coupling = 0.5 * k_c * (q.x1 - q.x2)**2
        
        return V_individual + V_coupling

# Create and evolve
coupled_system = CoupledOscillators()
initial_coupled = PhaseSpace(q=np.array([1.0, 0.0]), p=np.array([0.0, 0.0]))

t_c, q_c, p_c = coupled_system.evolve(initial_coupled, t_max=50.0, dt=0.01)

# Plot energy transfer
fig, ax = plt.subplots(figsize=(12, 6))

E1 = 0.5 * p_c[:, 0]**2 + 0.5 * q_c[:, 0]**2
E2 = 0.5 * p_c[:, 1]**2 + 0.5 * q_c[:, 1]**2

ax.plot(t_c, E1, label='Oscillator 1 Energy', linewidth=2)
ax.plot(t_c, E2, label='Oscillator 2 Energy', linewidth=2)
ax.plot(t_c, E1 + E2, label='Total Energy', linestyle='--', linewidth=2, color='white')
ax.set_xlabel('Time')
ax.set_ylabel('Energy')
ax.set_title('Energy Transfer Between Coupled Oscillators')
ax.legend()
ax.grid(alpha=0.3)
plt.savefig('coupled_oscillators.png', dpi=150, bbox_inches='tight')
plt.show()

print("Energy oscillates between the two systems - this is a NORMAL MODE!")
```

---

## Example 3: Using the Symbolic Engine

The symbolic engine automatically derives equations.

```python
from compiler import SymbolicHamiltonian

# Create symbolic 2-DOF system
sh = harmonic_oscillator_hamiltonian(n_dof=2, k=1.0, m=1.0)

print("Hamiltonian:")
print(sh.H)
print()

# Derive equations automatically
dq_dt, dp_dt = sh.hamilton_equations()

print("Hamilton's Equations:")
for i in range(sh.n_dof):
    print(f"  dq{i}/dt = {dq_dt[i]}")
    print(f"  dp{i}/dt = {dp_dt[i]}")
print()

# Find conserved quantities
conserved = sh.find_conserved_quantities()

print("Conserved Quantities:")
for name, expr in conserved.items():
    print(f"  {name}: {expr}")
```

Output:
```
Hamiltonian:
p0**2/2 + p1**2/2 + q0**2/2 + q1**2/2

Hamilton's Equations:
  dq0/dt = p0
  dp0/dt = -q0
  dq1/dt = p1
  dp1/dt = -q1

Conserved Quantities:
  energy: p0**2/2 + p1**2/2 + q0**2/2 + q1**2/2
  momentum: p0 + p1
```

All of this was **automatically derived** from the Hamiltonian!

---

## Exercise for You

Try modifying the potential to create a **double-well potential**:

```python
@define_system
class DoubleWell:
    coordinates = ['x']
    
    def kinetic(self, p):
        return p.px**2 / 2
    
    def potential(self, q):
        # Double-well: V(x) = -x² + x⁴
        return -q.x**2 + 0.25 * q.x**4

# Try evolving this and see what happens!
```

---

## Next Steps

- **Tutorial 2**: Market Dynamics - Modeling financial prices as Hamiltonians
- **Tutorial 3**: Quantum Systems - Entanglement and measurement
- **Tutorial 4**: Consciousness - Computing Integrated Information Φ

---

**Philosophy**: You just saw how the same framework handles simple oscillators, coupled systems, and emergent behavior. This is why Hamiltonian mechanics is universal!
