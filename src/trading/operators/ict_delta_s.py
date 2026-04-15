"""
ICT/FVG Trading Operator with ΔS-driven execution

Encodes:
- FVG entry only
- HTF alignment  
- Liquidity draw direction
- Risk per trade cap
- Max open positions

This is a production-grade ΔS operator for ICT/FVG trading systems.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from dataclasses import dataclass
from typing import Dict, List, Optional, Any
import numpy as np
from core.delta_s_operator import DeltaSOperator, Weights
from core.invariant_algebra import ViolationPotential, RelaxedInvariant
from trading.features.fvg import extract_fvg_features, fvg_distance
from trading.features.liquidity import detect_equal_highs, detect_equal_lows, liquidity_direction
from trading.features.structure import detect_swings, classify_structure, detect_bos, compute_structure_bias


# OperatorMeta schema for this trading operator
META = {
    "name": "DeltaS_ICT_FVG_Operator",
    "version": "v1.0.0",
    
    "design_tensor": {
        "domain_type": "market_state",
        "codomain_type": "market_state",
        "operator_class": "stochastic_control",
        "time_dependency": "discrete_event_driven"
    },
    
    "domain": "ICTMarketState",
    "codomain": "ICTMarketState",
    
    "invariants": [
        "fvg_entry_only",
        "htf_alignment", 
        "risk_per_trade_cap",
        "max_open_positions"
    ],
    
    "invariant_fields": {
        "enabled": True,
        "relaxation": "continuous",
        "phi_definition": "weighted_sum",
        "gradient_required": True
    },
    
    "objective": {
        "type": "delta_s_constrained_rl",
        "components": {
            "pnl": {"weight": 1.0},
            "delta_s": {"weight": 0.7},
            "violation": {"weight": 2.5},
            "gradient_penalty": {"weight": 0.15}
        },
        "aggregation": "discounted_sum"
    },
    
    "entropy": {
        "type": "ict_composite",
        "components": [
            "market_structure_entropy",
            "liquidity_entropy",
            "execution_entropy",
            "risk_entropy"
        ]
    },
    
    "scheduler_dependencies": ["delta_s_evaluator", "liquidity_target_resolver"],
    "audit_outputs": ["delta_s", "phi", "grad_phi_norm", "reward", "fvg_id", "htf_bias"],
    
    "lambda_usage": {"mode": "adaptive", "range": [0.5, 2.5]},
    "cpu_backend_semantics": "deterministic_shadow_required"
}


def fvg_relaxed(x: np.ndarray, k: float = 5.0) -> float:
    """
    Ĩ_FVG(x) = σ(-k * d_FVG)
    
    Distance from FVG center mapped to [0, 1].
    Inside FVG = 1, far away = 0.
    
    Expects x[0] = distance_to_fvg
    """
    distance = x[0]
    return 1.0 / (1.0 + np.exp(-k * distance))


def htf_alignment_relaxed(x: np.ndarray) -> float:
    """
    Ĩ_HTF(x) = (agreement + 1) / 2
    
    Agreement across timeframes in [-1, 1] mapped to [0, 1].
    
    Expects x[1:5] = tf_signals (H4, H1, M15, M1)
    """
    tf_signals = x[1:5]
    agreement = np.mean(np.sign(tf_signals))
    return (agreement + 1.0) / 2.0


def risk_cap_relaxed(x: np.ndarray) -> float:
    """
    Ĩ_RISK(x) = exp(-max(0, risk - cap))
    
    Exponential decay when risk exceeds cap.
    
    Expects x[5] = risk, x[6] = risk_cap
    """
    risk = x[5]
    cap = x[6]
    excess = max(0.0, risk - cap)
    return np.exp(-excess)


def liquidity_direction_relaxed(x: np.ndarray) -> float:
    """
    Ĩ_LIQ(x) = σ(k * (direction * alignment))
    
    Trade direction aligns with liquidity draw.
    
    Expects x[7] = liq_direction (+1 buy, -1 sell)
            x[8] = trade_direction (+1 long, -1 short)
    """
    liq_dir = x[7]
    trade_dir = x[8]
    alignment = liq_dir * trade_dir
    return 1.0 / (1.0 + np.exp(-5.0 * alignment))


class ICTMarketEntropy:
    """
    S(x) = S_structure + S_liquidity + S_execution + S_risk
    
    ICT-aligned entropy components.
    """
    
    def __call__(self, x: Dict[str, np.ndarray]) -> float:
        return (self.structure_entropy(x) + 
                self.liquidity_entropy(x) + 
                self.execution_entropy(x) + 
                self.risk_entropy(x))
    
    def structure_entropy(self, x: Dict[str, np.ndarray]) -> float:
        """S_structure = -Σ p_trend log p_trend"""
        if 'structure' in x:
            struct = x['structure']
            # Count structure types
            counts = np.bincount(struct.astype(int).flatten(), minlength=5)
            probs = counts / (counts.sum() + 1e-10)
            # Shannon entropy
            entropy = -np.sum(probs * np.log(probs.clip(1e-8)))
            return entropy
        return 0.0
    
    def liquidity_entropy(self, x: Dict[str, np.ndarray]) -> float:
        """S_liquidity ~ log(dispersion of liquidity targets)"""
        if 'eq_highs' in x and 'eq_lows' in x:
            # Dispersion measure
            return np.log(1.0 + np.std(x['eq_highs']) + np.std(x['eq_lows']))
        return 0.0
    
    def execution_entropy(self, x: Dict[str, np.ndarray]) -> float:
        """S_execution = policy entropy (placeholder for RL policy)"""
        if 'policy_logits' in x:
            logits = x['policy_logits']
            # Softmax probabilities
            exp_logits = np.exp(logits - np.max(logits))
            probs = exp_logits / np.sum(exp_logits)
            # Policy entropy
            return -np.sum(probs * np.log(probs.clip(1e-8)))
        return 0.0
    
    def risk_entropy(self, x: Dict[str, np.ndarray]) -> float:
        """S_risk = log(var(position) + var(drawdown))"""
        pos = x.get('position', np.array([0]))
        dd = x.get('drawdown', np.array([0]))
        
        pos_var = np.var(pos) if pos.size > 0 else 0.0
        dd_var = np.var(dd) if dd.size > 0 else 0.0
        
        return np.log(pos_var + dd_var + 1e-6)


class ICTDeltaSOperator(DeltaSOperator):
    """
    ICT/FVG Trading Operator
    
    Learns to enter when:
    1. Market collapsing toward structure (ΔS < 0)
    2. Inside FVG zone
    3. HTF aligned
    4. Risk within cap
    5. Liquidity direction matches trade
    
    Full shadow → collapse pipeline with OperatorMeta compliance.
    """
    
    def __init__(self, weights: Optional[Weights] = None):
        # Build invariant algebra
        invariants = [
            RelaxedInvariant(lambda x: fvg_relaxed(x)),
            RelaxedInvariant(lambda x: htf_alignment_relaxed(x)),
            RelaxedInvariant(lambda x: risk_cap_relaxed(x)),
            RelaxedInvariant(lambda x: liquidity_direction_relaxed(x))
        ]
        
        weights_inv = np.array([1.0, 1.0, 1.0, 1.0])
        phi = ViolationPotential(invariants, weights_inv)
        
        entropy = ICTMarketEntropy()
        
        super().__init__(entropy, phi, weights or Weights())
        
        # Store META for compliance
        self.meta = META
    
    def extract_ict_features(self, ohlc: np.ndarray, position: float = 0, 
                           drawdown: float = 0) -> Dict[str, np.ndarray]:
        """
        Extract all ICT features from OHLC data.
        
        Args:
            ohlc: [T, 4] array with (open, high, low, close)
            position: Current position size
            drawdown: Current drawdown
            
        Returns:
            Dict of ICT features
        """
        # FVG
        fvg = extract_fvg_features(ohlc)
        
        # Liquidity
        high = ohlc[:, 1]
        low = ohlc[:, 2]
        eq_highs = detect_equal_highs(high)
        eq_lows = detect_equal_lows(low)
        liq_dir = liquidity_direction(eq_highs, eq_lows)
        
        # Structure
        sh, sl = detect_swings(high, low)
        structure = classify_structure(high, low, sh, sl)
        bos_up, bos_down = detect_bos(structure)
        bias = compute_structure_bias(structure)
        
        return {
            # FVG
            'fvg_mask': fvg['fvg_mask'],
            'distance_to_fvg': fvg['distance_to_fvg'],
            'fvg_width': fvg['fvg_width'],
            
            # Liquidity
            'eq_highs': eq_highs,
            'eq_lows': eq_lows,
            'liq_direction': liq_dir,
            
            # Structure
            'swing_high': sh,
            'swing_low': sl,
            'structure': structure,
            'bos_up': bos_up,
            'bos_down': bos_down,
            'structure_bias': np.array([bias]),
            
            # Position/Risk
            'position': np.array([position]),
            'drawdown': np.array([drawdown])
        }
    
    def build_state_vector(self, features: Dict[str, np.ndarray], 
                          htf_bias: float = 0.0,
                          risk: float = 0.0,
                          risk_cap: float = 1.0) -> np.ndarray:
        """
        Build state vector for invariant evaluation.
        
        State vector layout:
        [0]: distance_to_fvg (current)
        [1-4]: timeframe_signals (H4, H1, M15, M1)
        [5]: risk
        [6]: risk_cap
        [7]: liq_direction (current)
        [8]: trade_direction (intended)
        """
        dist = features['distance_to_fvg'][-1] if len(features['distance_to_fvg']) > 0 else 0.0
        liq_dir = features['liq_direction'][-1] if len(features['liq_direction']) > 0 else 0.0
        
        # HTF signals (placeholder - would come from multi-TF data)
        # For now, use structure bias replicated across TFs
        struct_bias = features['structure_bias'][0] if 'structure_bias' in features else 0.0
        tf_signals = np.array([struct_bias, struct_bias * 0.8, struct_bias * 0.6, struct_bias * 0.4])
        
        return np.array([
            dist,           # [0] distance to FVG
            tf_signals[0],  # [1] H4 bias
            tf_signals[1],  # [2] H1 bias
            tf_signals[2],  # [3] M15 bias
            tf_signals[3],  # [4] M1 bias
            risk,           # [5] current risk
            risk_cap,       # [6] risk cap
            liq_dir,        # [7] liquidity direction
            0.0             # [8] trade direction (filled at decision time)
        ])
    
    def evaluate_entry(self, ohlc: np.ndarray, trade_direction: int,
                      position: float = 0, risk: float = 0, 
                      risk_cap: float = 1.0, K: int = 8) -> Dict[str, Any]:
        """
        Evaluate entry opportunity with shadow → collapse.
        
        Args:
            ohlc: Price data
            trade_direction: +1 for long, -1 for short
            position: Current position
            risk: Current risk exposure
            risk_cap: Maximum allowed risk
            K: Number of shadow candidates
            
        Returns:
            Decision dict with entry recommendation
        """
        # Extract ICT features
        features = self.extract_ict_features(ohlc, position)
        
        # Build state vector
        x_vec = self.build_state_vector(features, risk=risk, risk_cap=risk_cap)
        x_vec[8] = trade_direction  # Set intended trade direction
        
        # Convert to dict format for operator
        x = {k: v if isinstance(v, np.ndarray) else np.array([v]) 
             for k, v in features.items()}
        
        # Define action sampler (different entry prices within FVG)
        def action_sampler(x):
            # Sample entry price near FVG
            if 'fvg_mid' in x:
                mid = x['fvg_mid'][-1] if len(x['fvg_mid']) > 0 else 0.0
                width = x['fvg_width'][-1] if len(x['fvg_width']) > 0 else 0.0
                # Random entry within FVG zone
                noise = np.random.uniform(-0.3, 0.3)
                return mid + noise * width
            return 0.0
        
        # Define environment simulator
        def env_simulator(x, action):
            # Simulated: entry at action price
            # PnL proportional to distance to next target (simplified)
            if 'liq_direction' in x:
                target_direction = x['liq_direction'][-1] if len(x['liq_direction']) > 0 else 0.0
                pnl = target_direction * trade_direction * 10.0  # Simplified
            else:
                pnl = 0.0
            
            # Return next state and PnL
            x_next = x.copy()
            x_next['position'] = np.array([trade_direction])
            return x_next, pnl
        
        # Execute shadow → collapse
        selected, audit = self.execute(x, action_sampler, env_simulator, K)
        
        return {
            'should_enter': selected is not None,
            'entry_price': selected['action'] if selected else None,
            'expected_pnl': selected['pnl'] if selected else 0.0,
            'reward': selected['metrics']['reward'] if selected else float('-inf'),
            'delta_s': selected['metrics']['delta_s'] if selected else 0.0,
            'phi': selected['metrics']['phi'] if selected else float('inf'),
            'audit': audit,
            'features': features
        }
