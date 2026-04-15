"""
Liquidity Pool Detection (Equal Highs/Lows)

ICT concept: Liquidity pools are areas where equal highs (buy-side liquidity)
or equal lows (sell-side liquidity) exist. These act as price attractors.
"""

import numpy as np

def detect_equal_highs(high, tolerance=1e-4, window=5):
    """
    Detect clusters of equal highs (buy-side liquidity targets).
    
    Args:
        high: High price series [T] or [B, T]
        tolerance: Price difference tolerance for "equality"
        window: Lookback window for detecting clusters
    
    Returns:
        eq_highs: Boolean mask of equal high locations
    """
    eq_highs = np.zeros_like(high)
    
    for i in range(window, high.shape[-1]):
        window_slice = high[..., i-window:i]
        ref = high[..., i:i+1] if high.ndim > 1 else high[i]
        
        if high.ndim > 1:
            # Batch mode
            diff = np.abs(window_slice - ref)
            match = np.any(diff < tolerance, axis=-1)
            eq_highs[..., i] = match.astype(float)
        else:
            # Single series mode
            diff = np.abs(window_slice - ref)
            match = np.any(diff < tolerance)
            eq_highs[i] = float(match)
    
    return eq_highs


def detect_equal_lows(low, tolerance=1e-4, window=5):
    """
    Detect clusters of equal lows (sell-side liquidity targets).
    
    Args:
        low: Low price series [T] or [B, T]
        tolerance: Price difference tolerance for "equality"
        window: Lookback window for detecting clusters
    
    Returns:
        eq_lows: Boolean mask of equal low locations
    """
    eq_lows = np.zeros_like(low)
    
    for i in range(window, low.shape[-1]):
        window_slice = low[..., i-window:i]
        ref = low[..., i:i+1] if low.ndim > 1 else low[i]
        
        if low.ndim > 1:
            diff = np.abs(window_slice - ref)
            match = np.any(diff < tolerance, axis=-1)
            eq_lows[..., i] = match.astype(float)
        else:
            diff = np.abs(window_slice - ref)
            match = np.any(diff < tolerance)
            eq_lows[i] = float(match)
    
    return eq_lows


def detect_liquidity_sweep(high, low, eq_highs, eq_lows):
    """
    Detect when liquidity is taken (swept).
    
    A sweep occurs when:
    - Price exceeds previous high where equal highs exist (bullish sweep)
    - Price falls below previous low where equal lows exist (bearish sweep)
    
    Returns:
        sweep_high: Boolean of buy-side liquidity sweeps
        sweep_low: Boolean of sell-side liquidity sweeps
    """
    prev_high = np.roll(high, 1, axis=-1)
    prev_low = np.roll(low, 1, axis=-1)
    
    # Buy-side sweep: current high > prev high AND equal highs exist
    sweep_high = (high > prev_high) & (eq_highs > 0)
    
    # Sell-side sweep: current low < prev low AND equal lows exist
    sweep_low = (low < prev_low) & (eq_lows > 0)
    
    return sweep_high.astype(float), sweep_low.astype(float)


def liquidity_direction(eq_highs, eq_lows):
    """
    Determine liquidity direction bias.
    
    Returns:
        +1: Buy-side liquidity dominant (equal highs present)
        -1: Sell-side liquidity dominant (equal lows present)
        0: Balanced or no clear liquidity
    """
    return np.sign(eq_highs - eq_lows)


def compute_liquidity_score(eq_highs, eq_lows, window=20):
    """
    Compute liquidity concentration score.
    
    High score = concentrated liquidity (clear target)
    Low score = dispersed liquidity (no clear target)
    """
    recent_highs = eq_highs[..., -window:] if eq_highs.ndim > 1 else eq_highs[-window:]
    recent_lows = eq_lows[..., -window:] if eq_lows.ndim > 1 else eq_lows[-window:]
    
    # Concentration = clustered detections
    high_concentration = np.sum(recent_highs, axis=-1) / window
    low_concentration = np.sum(recent_lows, axis=-1) / window
    
    return np.maximum(high_concentration, low_concentration)
