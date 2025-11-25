"""
Interactive Phase-Space Visualizer

Real-time interactive Hamiltonian system visualization using matplotlib.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
from matplotlib.animation import FuncAnimation
import sys
import os

# Setup
plt.style.use('dark_background')
fig = plt.figure(figsize=(14, 10))
fig.suptitle('Universal Hamiltonian Framework - Interactive Phase-Space Explorer', 
             fontsize=16, fontweight='bold', color='#00d4ff')

# Create subplots
ax_phase = plt.subplot(2, 2, 1)
ax_time_q = plt.subplot(2, 2, 2)
ax_time_p = plt.subplot(2, 2, 3)
ax_energy = plt.subplot(2, 2, 4)

# Adjust for controls
plt.subplots_adjust(left=0.1, bottom=0.35, right=0.95, top=0.93, hspace=0.3, wspace=0.3)

# =============================================================================
# System Parameters (adjustable via sliders)
# =============================================================================

class HamiltonianSystem:
    def __init__(self):
        self.mass = 1.0
        self.k = 1.0  # Spring constant
        self.q0 = 1.0  # Initial position
        self.p0 = 0.0  # Initial momentum
        self.dt = 0.01
        self.max_points = 500
        
        # Current state
        self.reset()
    
    def reset(self):
        self.q = self.q0
        self.p = self.p0
        self.t = 0.0
        self.trajectory_q = [self.q]
        self.trajectory_p = [self.p]
        self.trajectory_t = [self.t]
        self.trajectory_E = [self.hamiltonian(self.q, self.p)]
    
    def hamiltonian(self, q, p):
        """H = p²/(2m) + ½kq²"""
        return p**2 / (2 * self.mass) + 0.5 * self.k * q**2
    
    def force(self, q):
        """F = -∂V/∂q = -kq"""
        return -self.k * q
    
    def step(self):
        """Symplectic Verlet integration step"""
        # Half-step momentum
        p_half = self.p + 0.5 * self.dt * self.force(self.q)
        
        # Full-step position
        self.q = self.q + self.dt * p_half / self.mass
        
        # Half-step momentum
        self.p = p_half + 0.5 * self.dt * self.force(self.q)
        
        # Update time
        self.t += self.dt
        
        # Store trajectory
        self.trajectory_q.append(self.q)
        self.trajectory_p.append(self.p)
        self.trajectory_t.append(self.t)
        self.trajectory_E.append(self.hamiltonian(self.q, self.p))
        
        # Keep only recent history
        if len(self.trajectory_q) > self.max_points:
            self.trajectory_q.pop(0)
            self.trajectory_p.pop(0)
            self.trajectory_t.pop(0)
            self.trajectory_E.pop(0)

# Create system
system = HamiltonianSystem()

# =============================================================================
# Create Sliders
# =============================================================================

# Mass slider
ax_mass = plt.axes([0.15, 0.25, 0.65, 0.03])
slider_mass = Slider(ax_mass, 'Mass (m)', 0.1, 5.0, valinit=system.mass, color='#00d4ff')

# Spring constant slider
ax_k = plt.axes([0.15, 0.20, 0.65, 0.03])
slider_k = Slider(ax_k, 'Spring (k)', 0.1, 5.0, valinit=system.k, color='#00d4ff')

# Initial position slider
ax_q0 = plt.axes([0.15, 0.15, 0.65, 0.03])
slider_q0 = Slider(ax_q0, 'Initial q₀', -5.0, 5.0, valinit=system.q0, color='#ff6b6b')

# Initial momentum slider
ax_p0 = plt.axes([0.15, 0.10, 0.65, 0.03])
slider_p0 = Slider(ax_p0, 'Initial p₀', -5.0, 5.0, valinit=system.p0, color='#4ecdc4')

# =============================================================================
# Create Buttons
# =============================================================================

# Reset button
ax_reset = plt.axes([0.15, 0.04, 0.1, 0.04])
btn_reset = Button(ax_reset, 'Reset', color='#ff6b6b', hovercolor='#ff8888')

# Play/Pause button
ax_play = plt.axes([0.27, 0.04, 0.1, 0.04])
btn_play = Button(ax_play, 'Pause', color='#4ecdc4', hovercolor='#6eddcc')

# =============================================================================
# Animation State
# =============================================================================

is_playing = True

def update_params(val):
    """Update system parameters from sliders"""
    system.mass = slider_mass.val
    system.k = slider_k.val
    system.q0 = slider_q0.val
    system.p0 = slider_p0.val

# Connect sliders
slider_mass.on_changed(update_params)
slider_k.on_changed(update_params)
slider_q0.on_changed(update_params)
slider_p0.on_changed(update_params)

def reset(event):
    """Reset simulation"""
    system.reset()
    update_plots()

def toggle_play(event):
    """Toggle play/pause"""
    global is_playing
    is_playing = not is_playing
    btn_play.label.set_text('Play' if not is_playing else 'Pause')

btn_reset.on_clicked(reset)
btn_play.on_clicked(toggle_play)

# =============================================================================
# Plotting Functions
# =============================================================================

# Initialize plot elements
line_phase, = ax_phase.plot([], [], 'o-', color='#00d4ff', linewidth=2, markersize=6, alpha=0.7)
point_current, = ax_phase.plot([], [], 'o', color='#ff0000', markersize=12, zorder=10)

line_q, = ax_time_q.plot([], [], color='#ff6b6b', linewidth=2)
line_p, = ax_time_p.plot([], [], color='#4ecdc4', linewidth=2)
line_E, = ax_energy.plot([], [], color='#ffd93d', linewidth=2)

# Configure axes
ax_phase.set_xlabel('Position q', fontsize=12)
ax_phase.set_ylabel('Momentum p', fontsize=12)
ax_phase.set_title('Phase Portrait', fontsize=14, fontweight='bold')
ax_phase.grid(True, alpha=0.3)
ax_phase.set_xlim(-5, 5)
ax_phase.set_ylim(-5, 5)
ax_phase.set_aspect('equal')

ax_time_q.set_xlabel('Time', fontsize=12)
ax_time_q.set_ylabel('Position q(t)', fontsize=12)
ax_time_q.set_title('Position Evolution', fontsize=14, fontweight='bold')
ax_time_q.grid(True, alpha=0.3)

ax_time_p.set_xlabel('Time', fontsize=12)
ax_time_p.set_ylabel('Momentum p(t)', fontsize=12)
ax_time_p.set_title('Momentum Evolution', fontsize=14, fontweight='bold')
ax_time_p.grid(True, alpha=0.3)

ax_energy.set_xlabel('Time', fontsize=12)
ax_energy.set_ylabel('Energy H(q,p)', fontsize=12)
ax_energy.set_title('Energy Conservation', fontsize=14, fontweight='bold')
ax_energy.grid(True, alpha=0.3)

def update_plots():
    """Update all plots with current trajectory"""
    if len(system.trajectory_q) < 2:
        return
    
    # Phase portrait
    line_phase.set_data(system.trajectory_q, system.trajectory_p)
    point_current.set_data([system.q], [system.p])
    
    # Time evolution
    line_q.set_data(system.trajectory_t, system.trajectory_q)
    line_p.set_data(system.trajectory_t, system.trajectory_p)
    line_E.set_data(system.trajectory_t, system.trajectory_E)
    
    # Auto-scale time plots
    if len(system.trajectory_t) > 1:
        t_min, t_max = min(system.trajectory_t), max(system.trajectory_t)
        dt_range = max(0.1, t_max - t_min)
        
        ax_time_q.set_xlim(t_min - 0.1*dt_range, t_max + 0.1*dt_range)
        ax_time_p.set_xlim(t_min - 0.1*dt_range, t_max + 0.1*dt_range)
        ax_energy.set_xlim(t_min - 0.1*dt_range, t_max + 0.1*dt_range)
        
        q_arr = np.array(system.trajectory_q)
        p_arr = np.array(system.trajectory_p)
        E_arr = np.array(system.trajectory_E)
        
        ax_time_q.set_ylim(q_arr.min() - 0.5, q_arr.max() + 0.5)
        ax_time_p.set_ylim(p_arr.min() - 0.5, p_arr.max() + 0.5)
        
        E_mean = E_arr.mean()
        E_range = max(0.01, E_arr.max() - E_arr.min())
        ax_energy.set_ylim(E_mean - 2*E_range, E_mean + 2*E_range)

def animate(frame):
    """Animation function"""
    if is_playing:
        # Evolve system
        for _ in range(5):  # 5 steps per frame for speed
            system.step()
        
        # Update plots
        update_plots()
    
    return line_phase, point_current, line_q, line_p, line_E

# =============================================================================
# Start Animation
# =============================================================================

# Add info text
info_text = fig.text(0.5, 0.01, 
                     'Use sliders to adjust parameters • Click Reset to restart • Pause/Play to control',
                     ha='center', fontsize=10, color='#888888')

print("\n" + "="*70)
print("UNIVERSAL HAMILTONIAN FRAMEWORK - INTERACTIVE VISUALIZER")
print("="*70)
print("\nControls:")
print("  • Adjust sliders to change mass, spring constant, and initial conditions")
print("  • Click 'Reset' to restart with new parameters")
print("  • Click 'Pause/Play' to control evolution")
print("\nPhase Portrait: Real-time (q, p) trajectory")
print("Position/Momentum: Time evolution")
print("Energy: Conservation verification")
print("\nClose the window to exit.")
print("="*70)
print()

# Create animation
ani = FuncAnimation(fig, animate, interval=50, blit=True, cache_frame_data=False)

plt.show()

print("\nVisualization closed.")
