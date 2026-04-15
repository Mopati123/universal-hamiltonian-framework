"""
Market Structure (HH/HL/LH/LL + BOS/CHOCH)

ICT market structure encodes trend direction and strength.
- HH/HL = Bullish structure
- LH/LL = Bearish structure
- BOS = Break of Structure (trend continuation)
- CHOCH = Change of Character (trend reversal)
"""

import numpy as np

def detect_swings(high, low, window=3):
    """
    Detect swing highs and lows using local extrema.
    
    Swing high: Higher than window bars left and right
    Swing low: Lower than window bars left and right
    
    Returns:
        swing_high: Boolean mask of swing high points
        swing_low: Boolean mask of swing low points
    """
    swing_high = np.zeros_like(high)
    swing_low = np.zeros_like(low)
    
    for i in range(window, high.shape[-1] - window):
        h, l = high[..., i], low[..., i]
        
        left_h = high[..., i-window:i]
        right_h = high[..., i+1:i+1+window]
        
        left_l = low[..., i-window:i]
        right_l = low[..., i+1:i+1+window]
        
        if high.ndim > 1:
            # Batch mode
            is_swing_high = (h > np.max(left_h, axis=-1)) & (h > np.max(right_h, axis=-1))
            is_swing_low = (l < np.min(left_l, axis=-1)) & (l < np.min(right_l, axis=-1))
            swing_high[..., i] = is_swing_high.astype(float)
            swing_low[..., i] = is_swing_low.astype(float)
        else:
            # Single series mode
            is_swing_high = (h > np.max(left_h)) & (h > np.max(right_h))
            is_swing_low = (l < np.min(left_l)) & (l < np.min(right_l))
            swing_high[i] = float(is_swing_high)
            swing_low[i] = float(is_swing_low)
    
    return swing_high, swing_low


def classify_structure(high, low, swing_high, swing_low):
    """
    Classify market structure based on swing points.
    
    Structure codes:
    0 = None
    1 = HH (Higher High) - bullish
    2 = HL (Higher Low) - bullish  
    3 = LH (Lower High) - bearish
    4 = LL (Lower Low) - bearish
    
    Returns:
        structure: Integer array of structure types
    """
    structure = np.zeros_like(high)
    
    # Track last swing points
    last_high = high[..., 0] if high.ndim > 1 else high[0]
    last_low = low[..., 0] if low.ndim > 1 else low[0]
    
    for i in range(1, high.shape[-1]):
        is_sh = swing_high[..., i] > 0 if high.ndim > 1 else swing_high[i] > 0
        is_sl = swing_low[..., i] > 0 if low.ndim > 1 else swing_low[i] > 0
        
        current_high = high[..., i]
        current_low = low[..., i]
        
        if high.ndim > 1:
            # Batch mode
            hh = is_sh & (current_high > last_high)
            lh = is_sh & (current_high <= last_high)
            hl = is_sl & (current_low > last_low)
            ll = is_sl & (current_low <= last_low)
            
            structure[..., i] = (hh.astype(int) * 1 + 
                                hl.astype(int) * 2 + 
                                lh.astype(int) * 3 + 
                                ll.astype(int) * 4)
            
            # Update last swing points
            last_high = np.where(is_sh, current_high, last_high)
            last_low = np.where(is_sl, current_low, last_low)
        else:
            # Single series mode
            if is_sh:
                if current_high > last_high:
                    structure[i] = 1  # HH
                else:
                    structure[i] = 3  # LH
                last_high = current_high
            elif is_sl:
                if current_low > last_low:
                    structure[i] = 2  # HL
                else:
                    structure[i] = 4  # LL
                last_low = current_low
    
    return structure


def detect_bos(structure):
    """
    Detect Break of Structure (BOS) signals.
    
    Bullish BOS: HH after LH (trend continuation up)
    Bearish BOS: LL after HL (trend continuation down)
    
    Returns:
        bos_up: Boolean of bullish BOS
        bos_down: Boolean of bearish BOS
    """
    prev = np.roll(structure, 1, axis=-1)
    
    # Bullish BOS: current=HH(1), prev=LH(3)
    bos_up = (structure == 1) & (prev == 3)
    
    # Bearish BOS: current=LL(4), prev=HL(2)
    bos_down = (structure == 4) & (prev == 2)
    
    return bos_up.astype(float), bos_down.astype(float)


def detect_choch(structure):
    """
    Detect Change of Character (CHOCH) signals.
    
    Bullish CHOCH: HL after LL (trend reversal up)
    Bearish CHOCH: LH after HH (trend reversal down)
    
    Returns:
        choch_up: Boolean of bullish CHOCH
        choch_down: Boolean of bearish CHOCH
    """
    prev = np.roll(structure, 1, axis=-1)
    
    # Bullish CHOCH: current=HL(2), prev=LL(4)
    choch_up = (structure == 2) & (prev == 4)
    
    # Bearish CHOCH: current=LH(3), prev=HH(1)
    choch_down = (structure == 3) & (prev == 1)
    
    return choch_up.astype(float), choch_down.astype(float)


def compute_structure_bias(structure, window=20):
    """
    Compute bullish/bearish bias from recent structure.
    
    Returns score in [-1, 1]:
    - Positive = bullish bias (more HH/HL)
    - Negative = bearish bias (more LH/LL)
    """
    recent = structure[..., -window:] if structure.ndim > 1 else structure[-window:]
    
    # Bullish structures: HH(1), HL(2)
    # Bearish structures: LH(3), LL(4)
    bullish_count = np.sum((recent == 1) | (recent == 2), axis=-1)
    bearish_count = np.sum((recent == 3) | (recent == 4), axis=-1)
    
    total = bullish_count + bearish_count
    return np.where(total > 0, 
                    (bullish_count - bearish_count) / total,
                    0.0)
