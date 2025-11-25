"""
Visualization Package - Phase-Space and Domain Rendering
"""

from .theme import (
    QUANTUM_PALETTE,
    DOMAIN_COLORS,
    apply_matplotlib_theme,
    get_domain_colormap,
    phase_space_gradient
)

from .domain_visualizer import (
    DomainVisualizer,
    visualize_domain
)

__all__ = [
    # Theme
    'QUANTUM_PALETTE',
    'DOMAIN_COLORS',
    'apply_matplotlib_theme',
    'get_domain_colormap',
    'phase_space_gradient',
    
    # Visualizers
    'DomainVisualizer',
    'visualize_domain',
]
