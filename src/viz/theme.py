"""
Quantum Color Palette & Visualization Theme

Unified theme system for all visualizations in the framework.
Based on quantum field theory color symbolism.
"""

# ============================================================================
# Quantum Color Palette
# ============================================================================

QUANTUM_PALETTE = {
    # Primary quantum colors
    'quantum_cyan': '#00d4ff',      # Superposition, phase space
    'quantum_magenta': '#ff00ff',   # Entanglement
    'wavefunction_blue': '#4ecdc4', # Probability amplitude
    
    # Energy levels
    'ground_state': '#0066ff',      # Lowest energy
    'excited_state': '#ff6b6b',     # Higher energy
    'ionization': '#ffd93d',        # Critical energy
    
    # Phase transitions
    'classical': '#888888',         # Classical limit
    'decoherence': '#ff9900',       # Quantum → Classical
    'measurement': '#00ff00',       # Wavefunction collapse
    
    # Semantic colors
    'momentum': '#4ecdc4',          # Cyan (p-space)
    'position': '#ff6b6b',          # Red (q-space)
    'energy': '#ffd93d',            # Gold (conserved)
    'time': '#ffffff',              # White (parameter)
    
    # Backgrounds
    'dark_bg': '#0a0a0a',
    'medium_bg': '#1e1e1e',
    'light_bg': '#333333',
}

# Matplotlib style
MATPLOTLIB_STYLE = {
    'axes.facecolor': QUANTUM_PALETTE['dark_bg'],
    'figure.facecolor': QUANTUM_PALETTE['dark_bg'],
    'axes.edgecolor': QUANTUM_PALETTE['quantum_cyan'],
    'axes.labelcolor': QUANTUM_PALETTE['quantum_cyan'],
    'xtick.color': QUANTUM_PALETTE['classical'],
    'ytick.color': QUANTUM_PALETTE['classical'],
    'grid.color': QUANTUM_PALETTE['light_bg'],
    'grid.alpha': 0.3,
    'text.color': 'white',
}

# Plotly theme
PLOTLY_TEMPLATE = {
    'layout': {
        'paper_bgcolor': QUANTUM_PALETTE['dark_bg'],
        'plot_bgcolor': QUANTUM_PALETTE['medium_bg'],
        'font': {'color': 'white'},
        'xaxis': {
            'gridcolor': QUANTUM_PALETTE['light_bg'],
            'zerolinecolor': QUANTUM_PALETTE['classical'],
        },
        'yaxis': {
            'gridcolor': QUANTUM_PALETTE['light_bg'],
            'zerolinecolor': QUANTUM_PALETTE['classical'],
        },
    }
}

# HTML/CSS theme
CSS_THEME = f"""
:root {{
    --quantum-cyan: {QUANTUM_PALETTE['quantum_cyan']};
    --quantum-magenta: {QUANTUM_PALETTE['quantum_magenta']};
    --wavefunction-blue: {QUANTUM_PALETTE['wavefunction_blue']};
    --energy-gold: {QUANTUM_PALETTE['energy']};
    --dark-bg: {QUANTUM_PALETTE['dark_bg']};
    --medium-bg: {QUANTUM_PALETTE['medium_bg']};
}}

body {{
    background: var(--dark-bg);
    color: white;
    font-family: 'Segoe UI', sans-serif;
}}

.phase-space {{
    border: 2px solid var(--quantum-cyan);
    box-shadow: 0 0 20px rgba(0, 212, 255, 0.3);
}}

.energy-conserved {{
    color: var(--energy-gold);
    text-shadow: 0 0 10px var(--energy-gold);
}}
"""

# ============================================================================
# Domain-Specific Color Mappings
# ============================================================================

DOMAIN_COLORS = {
    'quantum': {
        'primary': QUANTUM_PALETTE['quantum_cyan'],
        'secondary': QUANTUM_PALETTE['wavefunction_blue'],
        'accent': QUANTUM_PALETTE['quantum_magenta'],
    },
    'classical': {
        'primary': QUANTUM_PALETTE['classical'],
        'secondary': QUANTUM_PALETTE['light_bg'],
        'accent': QUANTUM_PALETTE['excited_state'],
    },
    'market': {
        'primary': QUANTUM_PALETTE['excited_state'],  # Price (volatile)
        'secondary': QUANTUM_PALETTE['momentum'],      # Momentum
        'accent': QUANTUM_PALETTE['energy'],           # Capital
    },
    'consciousness': {
        'primary': QUANTUM_PALETTE['quantum_magenta'],  # Neural activity
        'secondary': QUANTUM_PALETTE['wavefunction_blue'], # Attention
        'accent': QUANTUM_PALETTE['measurement'],         # Awareness
    },
    'blockchain': {
        'primary': QUANTUM_PALETTE['quantum_cyan'],     # Consensus
        'secondary': QUANTUM_PALETTE['decoherence'],    # Hash power
        'accent': QUANTUM_PALETTE['ionization'],        # Transaction
    },
}

# ============================================================================
# Helper Functions
# ============================================================================

def apply_matplotlib_theme():
    """Apply quantum theme to matplotlib"""
    import matplotlib.pyplot as plt
    plt.style.use('dark_background')
    for key, value in MATPLOTLIB_STYLE.items():
        plt.rcParams[key] = value

def get_domain_colormap(domain: str):
    """Get colormap for specific domain"""
    import matplotlib.colors as mcolors
    
    if domain not in DOMAIN_COLORS:
        domain = 'quantum'  # Default
    
    colors = DOMAIN_COLORS[domain]
    cmap = mcolors.LinearSegmentedColormap.from_list(
        f'{domain}_cmap',
        [colors['primary'], colors['secondary'], colors['accent']]
    )
    return cmap

def phase_space_gradient():
    """Return gradient for phase-space backgrounds"""
    return f"linear-gradient(135deg, {QUANTUM_PALETTE['dark_bg']}, {QUANTUM_PALETTE['medium_bg']})"

# ============================================================================
# Exports
# ============================================================================

__all__ = [
    'QUANTUM_PALETTE',
    'DOMAIN_COLORS',
    'apply_matplotlib_theme',
    'get_domain_colormap',
    'phase_space_gradient',
    'CSS_THEME',
]
