"""
Phase-Space Visualization - Plotly Dash

Interactive phase-space exploration with real-time evolution display.
"""

import dash
from dash import dcc, html, Input, Output, State
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from typing import Optional

# Will import from core when available
# from ..core import PhaseSpace, HamiltonianSystem


class PhaseSpaceApp:
    """
    Interactive Dash application for phase-space visualization.
    
    Features:
    - Domain selector
    - Real-time phase portraits
    - Parameter controls
    - Multi-system comparison
    """
    
    def __init__(self, title: str = "Universal Hamiltonian Framework"):
        self.app = dash.Dash(__name__)
        self.title = title
        self.setup_layout()
        self.setup_callbacks()
    
    def setup_layout(self):
        """Create the UI layout"""
        self.app.layout = html.Div([
            html.H1(self.title, style={'textAlign': 'center', 'color': '#00d4ff'}),
            
            html.Div([
                # Domain selector
                html.Div([
                    html.Label("Select Domain:", style={'color': '#ffffff'}),
                    dcc.Dropdown(
                        id='domain-selector',
                        options=[
                            {'label': '⚛️ Quantum Systems', 'value': 'quantum'},
                            {'label': '🌌 Classical Mechanics', 'value': 'classical'},
                            {'label': '📈 Market Dynamics', 'value': 'market'},
                            {'label': '🧠 Consciousness Field', 'value': 'consciousness'},
                            {'label': '🔗 Blockchain Consensus', 'value': 'blockchain'},
                        ],
                        value='quantum',
                        style={'backgroundColor': '#1e1e1e', 'color': '#ffffff'}
                    ),
                ], style={'width': '30%', 'display': 'inline-block', 'padding': '20px'}),
                
                # Parameter controls
                html.Div([
                    html.Label("Mass (m):", style={'color': '#ffffff'}),
                    dcc.Slider(id='mass-slider', min=0.1, max=5.0, value=1.0, step=0.1,
                               marks={i: str(i) for i in range(1, 6)}),
                    
                    html.Label("Spring Constant (k):", style={'color': '#ffffff'}),
                    dcc.Slider(id='k-slider', min=0.1, max=5.0, value=1.0, step=0.1,
                               marks={i: str(i) for i in range(1, 6)}),
                    
                    html.Label("Initial Position (q₀):", style={'color': '#ffffff'}),
                    dcc.Slider(id='q0-slider', min=-5.0, max=5.0, value=1.0, step=0.5,
                               marks={i: str(i) for i in range(-5, 6)}),
                    
                    html.Label("Initial Momentum (p₀):", style={'color': '#ffffff'}),
                    dcc.Slider(id='p0-slider', min=-5.0, max=5.0, value=0.0, step=0.5,
                               marks={i: str(i) for i in range(-5, 6)}),
                ], style={'width': '30%', 'display': 'inline-block', 'padding': '20px'}),
                
                # Control buttons
                html.Div([
                    html.Button('▶️ Evolve', id='evolve-button', n_clicks=0,
                                style={'backgroundColor': '#00d4ff', 'color': '#000000', 
                                       'fontSize': '16px', 'padding': '10px 20px', 'margin': '10px'}),
                    html.Button('⏹️ Reset', id='reset-button', n_clicks=0,
                                style={'backgroundColor': '#ff6b6b', 'color': '#000000',
                                       'fontSize': '16px', 'padding': '10px 20px', 'margin': '10px'}),
                ], style={'width': '30%', 'display': 'inline-block', 'padding': '20px', 'textAlign': 'center'}),
            ]),
            
            # Phase portrait
            html.Div([
                dcc.Graph(id='phase-portrait', style={'height': '500px'}),
            ]),
            
            # Time evolution
            html.Div([
                dcc.Graph(id='time-evolution', style={'height': '400px'}),
            ]),
            
            # Energy conservation
            html.Div([
                dcc.Graph(id='energy-plot', style={'height': '300px'}),
            ]),
            
        ], style={'backgroundColor': '#0a0a0a', 'padding': '20px'})
    
    def setup_callbacks(self):
        """Setup interactive callbacks"""
        
        @self.app.callback(
            [Output('phase-portrait', 'figure'),
             Output('time-evolution', 'figure'),
             Output('energy-plot', 'figure')],
            [Input('evolve-button', 'n_clicks'),
             Input('reset-button', 'n_clicks')],
            [State('domain-selector', 'value'),
             State('mass-slider', 'value'),
             State('k-slider', 'value'),
             State('q0-slider', 'value'),
             State('p0-slider', 'value')]
        )
        def update_plots(n_evolve, n_reset, domain, mass, k, q0, p0):
            """Update all plots based on parameters"""
            # Simulate harmonic oscillator
            t_max = 20.0
            dt = 0.05
            n_steps = int(t_max / dt)
            
            t = np.linspace(0, t_max, n_steps)
            omega = np.sqrt(k / mass)
            
            # Analytical solution for harmonic oscillator
            q = q0 * np.cos(omega * t) + (p0 / (mass * omega)) * np.sin(omega * t)
            p = -mass * omega * q0 * np.sin(omega * t) + p0 * np.cos(omega * t)
            
            # Energy
            E = 0.5 * mass * (p / mass)**2 + 0.5 * k * q**2
            
            # Phase portrait
            phase_fig = go.Figure()
            phase_fig.add_trace(go.Scatter(
                x=q, y=p,
                mode='lines',
                line=dict(color='#00d4ff', width=2),
                name='Trajectory'
            ))
            phase_fig.add_trace(go.Scatter(
                x=[q[0]], y=[p[0]],
                mode='markers',
                marker=dict(color='#00ff00', size=12, symbol='circle'),
                name='Start'
            ))
            phase_fig.add_trace(go.Scatter(
                x=[q[-1]], y=[p[-1]],
                mode='markers',
                marker=dict(color='#ff0000', size=12, symbol='square'),
                name='End'
            ))
            phase_fig.update_layout(
                title=f"Phase Portrait - {domain.capitalize()} Domain",
                xaxis_title="Position (q)",
                yaxis_title="Momentum (p)",
                template='plotly_dark',
                paper_bgcolor='#0a0a0a',
                plot_bgcolor='#1e1e1e',
                font=dict(color='#ffffff')
            )
            
            # Time evolution
            time_fig = go.Figure()
            time_fig.add_trace(go.Scatter(
                x=t, y=q,
                mode='lines',
                line=dict(color='#ff6b6b', width=2),
                name='q(t)'
            ))
            time_fig.add_trace(go.Scatter(
                x=t, y=p,
                mode='lines',
                line=dict(color='#4ecdc4', width=2),
                name='p(t)'
            ))
            time_fig.update_layout(
                title="Time Evolution",
                xaxis_title="Time (t)",
                yaxis_title="q, p",
                template='plotly_dark',
                paper_bgcolor='#0a0a0a',
                plot_bgcolor='#1e1e1e',
                font=dict(color='#ffffff')
            )
            
            # Energy
            energy_fig = go.Figure()
            energy_fig.add_trace(go.Scatter(
                x=t, y=E,
                mode='lines',
                line=dict(color='#ffd93d', width=2),
                fill='tozeroy',
                fillcolor='rgba(255, 217, 61, 0.2)',
                name='E(t)'
            ))
            energy_fig.update_layout(
                title="Energy Conservation",
                xaxis_title="Time (t)",
                yaxis_title="Energy (H)",
                template='plotly_dark',
                paper_bgcolor='#0a0a0a',
                plot_bgcolor='#1e1e1e',
                font=dict(color='#ffffff')
            )
            
            return phase_fig, time_fig, energy_fig
    
    def run(self, port: int = 8050, debug: bool = True):
        """Start the Dash server"""
        self.app.run_server(port=port, debug=debug)


def create_3d_phase_space_plot(q_traj: np.ndarray, p_traj: np.ndarray, E_traj: np.ndarray):
    """
    Create 3D phase-space plot: (q, p, E)
    
    Args:
        q_traj: Position trajectory
        p_traj: Momentum trajectory
        E_traj: Energy trajectory
    """
    fig = go.Figure()
    
    # Trajectory
    fig.add_trace(go.Scatter3d(
        x=q_traj, y=p_traj, z=E_traj,
        mode='lines',
        line=dict(
            color=np.arange(len(q_traj)),
            colorscale='Plasma',
            width=4
        ),
        name='Trajectory'
    ))
    
    # Start point
    fig.add_trace(go.Scatter3d(
        x=[q_traj[0]], y=[p_traj[0]], z=[E_traj[0]],
        mode='markers',
        marker=dict(size=10, color='green'),
        name='Start'
    ))
    
    fig.update_layout(
        scene=dict(
            xaxis_title='Position (q)',
            yaxis_title='Momentum (p)',
            zaxis_title='Energy (H)',
            bgcolor='#0a0a0a',
        ),
        template='plotly_dark',
        title='3D Phase Space'
    )
    
    return fig


if __name__ == '__main__':
    app = PhaseSpaceApp()
    print("Starting Universal Hamiltonian Framework visualization...")
    print("Open http://localhost:8050 in your browser")
    app.run()
