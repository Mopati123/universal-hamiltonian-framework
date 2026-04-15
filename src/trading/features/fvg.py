"""
Fair Value Gap (FVG) Detection

ICT definition:
- Bullish FVG: low[i] > high[i-2]
- Bearish FVG: high[i] < low[i-2]
"""

import numpy as np

def detect_fvg(ohlc):
    """
    Detect Fair Value Gaps in OHLC data.
    
    ohlc: [T, 4] or [B, T, 4] → (open, high, low, close)
    
    Returns:
        fvg_mask: Boolean array indicating FVG presence
        fvg_upper: Upper bound of FVG zone
        fvg_lower: Lower bound of FVG zone
    """
    high = ohlc[..., 1]
    low = ohlc[..., 2]
    
    prev2_high = np.roll(high, shift=2, axis=-1)
    prev2_low = np.roll(low, shift=2, axis=-1)
    
    # Bullish FVG: current low > high 2 bars ago
    bullish = low > prev2_high
    # Bearish FVG: current high < low 2 bars ago
    bearish = high < prev2_low
    
    fvg_mask = bullish | bearish
    
    # Upper and lower bounds
    fvg_upper = np.where(bullish, low, prev2_low)
    fvg_lower = np.where(bullish, prev2_high, high)
    
    return fvg_mask.astype(float), fvg_upper, fvg_lower


def fvg_distance(price, fvg_upper, fvg_lower):
    """
    Compute distance to nearest FVG zone.
    
    Returns 0 if price is inside an FVG zone.
    Returns positive distance to nearest edge if outside.
    """
    inside = (price >= fvg_lower) & (price <= fvg_upper)
    
    dist_lower = np.abs(price - fvg_lower)
    dist_upper = np.abs(price - fvg_upper)
    
    return np.where(inside, 0.0, np.minimum(dist_lower, dist_upper))


def extract_fvg_features(ohlc):
    """
    Extract comprehensive FVG features from OHLC data.
    
    Returns dict with:
    - fvg_mask: presence of FVG
    - fvg_upper/lower: zone bounds
    - fvg_mid: center of zone
    - fvg_width: size of imbalance
    - distance_to_fvg: from current close price
    """
    mask, upper, lower = detect_fvg(ohlc)
    
    close = ohlc[..., 3]
    
    mid = (upper + lower) / 2.0
    width = np.abs(upper - lower)
    dist = fvg_distance(close, upper, lower)
    
    return {
        'fvg_mask': mask,
        'fvg_upper': upper,
        'fvg_lower': lower,
        'fvg_mid': mid,
        'fvg_width': width,
        'distance_to_fvg': dist
    }
