"""
Visualization Tools for Bioenergetic Consciousness

Interactive real-time visualizations for:
- Cognitive velocity
- Neural coherence
- Tachyonic access
- Ternary logic state
- Bioenergetic evolution

Author: Mopati
Framework: Universal Hamiltonian Framework  
Date: November 26, 2025
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from bioenergetic_consciousness import BioenergticConsciousness, BioenergticState

class CognitiveVelocityVisualizer:
    """Real-time visualization of cognitive velocity and related metrics"""
    
    def __init__(self, bio_cons: BioenergticConsciousness):
        self.bio_cons = bio_cons
        self.history = {
            'time': [],
            'E_bio': [],
            'coherence': [],
            'phi': [],
            'v_cognitive': [],
            'tachyonic_access': [],
            'is_ternary': []
        }
    
    def update(self, t: float, state: BioenergticState):
        """Add new data point"""
        self.history['time'].append(t)
        self.history['E_bio'].append(state.E_bio)
        self.history['coherence'].append(state.coherence)
        self.history['phi'].append(state.phi)
        
        v_cog = self.bio_cons.compute_cognitive_velocity(state)
        self.history['v_cognitive'].append(v_cog)
        
        tach = self.bio_cons.measure_tachyonic_access(state)
        self.history['time'].append(tach)
        
        ternary = self.bio_cons.is_ternary_active(state)
        self.history['is_ternary'].append(1.0 if ternary else 0.0)
    
    def create_dashboard(self) -> go.Figure:
        """
        Create interactive Plotly dashboard showing all metrics
        """
        fig = make_subplots(
            rows=3, cols=2,
            subplot_titles=(
                'Biological Energy', 'Neural Coherence',
                'Consciousness (Φ)', 'Cognitive Velocity',
                'Tachyonic Access', 'Ternary Logic State'
            ),
            vertical_spacing=0.12,
            horizontal_spacing=0.10
        )
        
        t = self.history['time']
        
        # Row 1: Energy and Coherence
        fig.add_trace(go.Scatter(x=t, y=self.history['E_bio'], 
                                name='E_bio', line=dict(color='#FF6B6B')),
                     row=1, col=1)
        
        fig.add_trace(go.Scatter(x=t, y=self.history['coherence'],
                                name='Coherence', line=dict(color='#4ECDC4')),
                     row=1, col=2)
        
        # Row 2: Phi and Cognitive Velocity
        fig.add_trace(go.Scatter(x=t, y=self.history['phi'],
                                name='Φ', line=dict(color='#95E1D3')),
                     row=2, col=1)
        
        fig.add_trace(go.Scatter(x=t, y=self.history['v_cognitive'],
                                name='v_cog', line=dict(color='#F38181')),
                     row=2, col=2)
        
        # Add threshold line for superluminal
        fig.add_hline(y=1.0, line_dash="dash", line_color="red",
                     annotation_text="Superluminal threshold",
                     row=2, col=2)
        
        # Row 3: Tachyonic Access and Ternary State
        fig.add_trace(go.Scatter(x=t, y=self.history['tachyonic_access'],
                                name='Tachyonic', line=dict(color='#AA96DA')),
                     row=3, col=1)
        
        fig.add_trace(go.Scatter(x=t, y=self.history['is_ternary'],
                                name='Ternary Active', 
                                line=dict(color='#FCBAD3'),
                                fill='tozeroy'),
                     row=3, col=2)
        
        # Update layout
        fig.update_layout(
            title_text="Bioenergetic Consciousness Dashboard",
            showlegend=False,
            height=900,
            template='plotly_dark'
        )
        
        # Update axes labels
        for i in range(1, 4):
            fig.update_xaxes(title_text="Time (days)", row=i, col=1)
            fig.update_xaxes(title_text="Time (days)", row=i, col=2)
        
        fig.update_yaxes(title_text="Energy", row=1, col=1)
        fig.update_yaxes(title_text="Coherence", row=1, col=2)
        fig.update_yaxes(title_text="Φ", row=2, col=1)
        fig.update_yaxes(title_text="v_cog", row=2, col=2)
        fig.update_yaxes(title_text="Access", row=3, col=1)
        fig.update_yaxes(title_text="State", row=3, col=2)
        
        return fig
    
    def create_3d_phase_space(self) -> go.Figure:
        """
        3D phase space: (Φ, E_bio, v_cog)
        Shows trajectory through consciousness space
        """
        fig = go.Figure()
        
        # Trajectory
        fig.add_trace(go.Scatter3d(
            x=self.history['phi'],
            y=self.history['E_bio'],
            z=self.history['v_cognitive'],
            mode='lines+markers',
            marker=dict(
                size=4,
                color=self.history['time'],
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title="Time")
            ),
            line=dict(color='cyan', width=2),
            name='Trajectory'
        ))
        
        # Superluminal plane (v_cog = 1.0)
        phi_range = np.linspace(0, max(self.history['phi']) * 1.2, 20)
        E_range = np.linspace(0, 100, 20)
        Phi_grid, E_grid = np.meshgrid(phi_range, E_range)
        V_grid = np.ones_like(Phi_grid)
        
        fig.add_trace(go.Surface(
            x=phi_range,
            y=E_range,
            z=V_grid,
            colorscale='Reds',
            opacity=0.3,
            showscale=False,
            name='Superluminal threshold'
        ))
        
        fig.update_layout(
            title="Consciousness Phase Space",
            scene=dict(
                xaxis_title="Φ (Integration)",
                yaxis_title="E_bio (Energy)",
                zaxis_title="v_cog (Velocity)",
                camera=dict(eye=dict(x=1.5, y=1.5, z=1.3))
            ),
            template='plotly_dark'
        )
        
        return fig


class TernaryLogicVisualizer:
    """Visualize ternary logic state and evolution"""
    
    @staticmethod
    def create_ternary_diagram(state: BioenergticState) -> go.Figure:
        """
        Ternary diagram showing Mind-Heart-Spirit balance
        
        Psi_1, Psi_2 = Mind (logic)
        Psi_3 = Heart (emotion)
        Psi_4 = Spirit (wisdom)
        """
        psi = state.psi
        
        # Normalization
        mind = abs(psi[0]) + abs(psi[1])
        heart = abs(psi[2])
        spirit = abs(psi[3])
        total = mind + heart + spirit + 1e-10
        
        mind_frac = mind / total
        heart_frac = heart / total
        spirit_frac = spirit / total
        
        fig = go.Figure()
        
        # Ternary scatter plot
        fig.add_trace(go.Scatterternary(
            a=[mind_frac],
            b=[heart_frac],
            c=[spirit_frac],
            mode='markers+text',
            marker=dict(
                size=20,
                color='cyan',
                symbol='circle'
            ),
            text=['Current State'],
            textposition='top center'
        ))
        
        # Ideal ternary point (equal balance)
        fig.add_trace(go.Scatterternary(
            a=[1/3],
            b=[1/3],
            c=[1/3],
            mode='markers',
            marker=dict(
                size=15,
                color='gold',
                symbol='star'
            ),
            name='Ideal Balance'
        ))
        
        fig.update_layout(
            title="Ternary Logic State",
            ternary=dict(
                aaxis=dict(title='Mind (Logic)'),
                baxis=dict(title='Heart (Emotion)'),
                caxis=dict(title='Spirit (Wisdom)')
            ),
            template='plotly_dark'
        )
        
        return fig


class RealtimeMonitor:
    """
    Real-time monitoring system for bioenergetic consciousness
    
    Can be connected to actual EEG hardware for live feedback
    """
    
    def __init__(self, retention_days: float = 0):
        self.bio_cons = BioenergticConsciousness(retention_days=retention_days)
        self.state = None
        self.visualizer = None
    
    def initialize(self):
        """Setup monitoring"""
        self.state = create_initial_state(retention_days=self.bio_cons.retention_days)
        self.visualizer = CognitiveVelocityVisualizer(self.bio_cons)
    
    def update_from_eeg(self, eeg_coherence: float, time_elapsed: float):
        """
        Update state from real EEG data
        
        Args:
            eeg_coherence: Measured coherence (0-1)
            time_elapsed: Time since start (seconds)
        """
        # Update neural coherence from measurement
        self.state.coherence = eeg_coherence
        
        # Recompute derived quantities
        self.state.phi = self.bio_cons.compute_phi(self.state.psi)
        
        # Update visualization
        self.visualizer.update(time_elapsed, self.state)
    
    def show_dashboard(self):
        """Display live dashboard"""
        fig = self.visualizer.create_dashboard()
        fig.show()
    
    def export_data(self, filename: str):
        """Export history to CSV"""
        import pandas as pd
        df = pd.DataFrame(self.visualizer.history)
        df.to_csv(filename, index=False)
        print(f"Data exported to {filename}")


# Demo/Test functions
def demo_evolution_visualization():
    """Demonstrate evolution over 30 days"""
    print("Simulating 30-day evolution with visualization...")
    
    bio_cons = BioenergticConsciousness(retention_days=0)
    viz = CognitiveVelocityVisualizer(bio_cons)
    
    # Simulate
    state = create_initial_state(retention_days=0)
    
    for day in range(30):
        # Gradual energy increase (retention effect)
        state.E_bio = 50 + 25 * np.log(1 + day / 10.0)
        
        # Evolve state slightly
        state = bio_cons.evolve_state(state, dt=0.1)
        
        # Update visualization
        viz.update(day, state)
    
    # Create dashboard
    fig = viz.create_dashboard()
    fig.write_html("cognitive_dashboard.html")
    print("Dashboard saved to cognitive_dashboard.html")
    
    # Create 3D phase space
    fig_3d = viz.create_3d_phase_space()
    fig_3d.write_html("phase_space_3d.html")
    print("3D phase space saved to phase_space_3d.html")


def demo_ternary_visualization():
    """Demonstrate ternary logic diagrams"""
    print("Creating ternary logic visualizations...")
    
    # Binary state (conflicted)
    binary_state = BioenergticState(
        psi=np.array([0.9, 0.8, 0.1, 0.05]),  # Mind dominant
        pi=np.zeros(4),
        E_bio=55,
        dopamine=1.0,
        coherence=0.3,
        phi=0.25
    )
    
    # Ternary state (integrated)
    ternary_state = BioenergticState(
        psi=np.array([0.6, 0.5, 0.6, 0.7]),  # Balanced
        pi=np.zeros(4),
        E_bio=80,
        dopamine=1.3,
        coherence=0.55,
        phi=0.65
    )
    
    # Visualize both
    fig_binary = TernaryLogicVisualizer.create_ternary_diagram(binary_state)
    fig_binary.update_layout(title="Binary Logic State (Unbalanced)")
    fig_binary.write_html("ternary_binary.html")
    
    fig_ternary = TernaryLogicVisualizer.create_ternary_diagram(ternary_state)
    fig_ternary.update_layout(title="Ternary Logic State (Balanced)")
    fig_ternary.write_html("ternary_integrated.html")
    
    print("Ternary visualizations saved!")


if __name__ == "__main__":
    print("=" * 70)
    print("BIOENERGETIC CONSCIOUSNESS VISUALIZATION TOOLS")
    print("=" * 70)
    
    demo_evolution_visualization()
    print()
    demo_ternary_visualization()
    
    print("\n" + "=" * 70)
    print("All visualizations generated successfully!")
    print("Open the HTML files in your browser to view.")
    print("=" * 70)
