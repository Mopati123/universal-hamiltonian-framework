"""
ΔS Operator - Entropy-guided operator with invariant inversion

Implements the full objective:
J(θ) = E[Σ_t (α·PnL - β·ΔS - γ·Φ - η·||∇Φ||²)]

With shadow exploration and collapse enforcement.
"""

from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional, Callable, Any
import numpy as np
from .invariant_algebra import ViolationPotential, InversionOperator, RelaxedInvariant


@dataclass
class Weights:
    """Reward functional weights"""
    alpha: float = 1.0   # PnL
    beta: float = 0.5    # ΔS
    gamma: float = 2.0   # Φ (violation)
    eta: float = 0.1     # ∇Φ penalty


class EntropyFunction:
    """S(x) = S_market + S_agent + S_risk"""
    
    def __init__(self, 
                 market_fn: Optional[Callable] = None,
                 agent_fn: Optional[Callable] = None,
                 risk_fn: Optional[Callable] = None):
        self.market_fn = market_fn or self._default_market_entropy
        self.agent_fn = agent_fn or self._default_agent_entropy
        self.risk_fn = risk_fn or self._default_risk_entropy
    
    def __call__(self, x: Dict[str, np.ndarray]) -> float:
        return (self.market_fn(x) + 
                self.agent_fn(x) + 
                self.risk_fn(x))
    
    def _default_market_entropy(self, x: Dict[str, np.ndarray]) -> float:
        # Proxy: log volatility
        if 'volatility' in x:
            return np.log(np.clip(x['volatility'], 1e-6, None))
        return 0.0
    
    def _default_agent_entropy(self, x: Dict[str, np.ndarray]) -> float:
        # Policy entropy placeholder
        return 0.0
    
    def _default_risk_entropy(self, x: Dict[str, np.ndarray]) -> float:
        # Proxy: log variance
        if 'position' in x and 'drawdown' in x:
            pos = x['position']
            dd = x['drawdown']
            if isinstance(pos, np.ndarray):
                pos_var = pos.var() if pos.size > 0 else 0.0
            else:
                pos_var = 0.0
            if isinstance(dd, np.ndarray):
                dd_var = dd.var() if dd.size > 0 else 0.0
            else:
                dd_var = 0.0
            return np.log(pos_var + dd_var + 1e-6)
        return 0.0


class DeltaSOperator:
    """
    Entropy-guided operator with invariant inversion algebra.
    
    Shadow phase: Explore all candidates, compute ΔS, Φ, ∇Φ
    Collapse phase: Enforce Φ=0, select optimal action
    """
    
    def __init__(self,
                 entropy_fn: EntropyFunction,
                 violation_potential: ViolationPotential,
                 weights: Weights,
                 gamma_discount: float = 0.99):
        self.entropy = entropy_fn
        self.phi = violation_potential
        self.weights = weights
        self.gamma = gamma_discount
        self.inversion = InversionOperator(violation_potential.invariants)
    
    def compute_delta_s(self, 
                       x: Dict[str, np.ndarray], 
                       x_next: Dict[str, np.ndarray]) -> float:
        """ΔS = S(x_next) - S(x)"""
        return self.entropy(x_next) - self.entropy(x)
    
    def _extract_state_vector(self, x: Dict[str, np.ndarray]) -> np.ndarray:
        """Extract continuous state vector from state dict."""
        vectors = []
        for key, val in x.items():
            if isinstance(val, np.ndarray):
                vectors.append(val.flatten())
        if vectors:
            return np.concatenate(vectors)
        return np.zeros(1)
    
    def compute_reward(self,
                      x: Dict[str, np.ndarray],
                      x_next: Dict[str, np.ndarray],
                      pnl: float) -> Dict[str, Any]:
        """
        r = α·PnL - β·ΔS - γ·Φ - η·||∇Φ||²
        
        Returns full reward breakdown for auditing.
        """
        delta_s = self.compute_delta_s(x, x_next)
        
        # Get state vector for Φ computation
        x_vec = self._extract_state_vector(x_next)
        
        phi = self.phi(x_vec)
        grad_phi = self.phi.gradient(x_vec)
        grad_norm_sq = np.sum(grad_phi ** 2)
        
        reward = (self.weights.alpha * pnl -
                  self.weights.beta * delta_s -
                  self.weights.gamma * phi -
                  self.weights.eta * grad_norm_sq)
        
        return {
            'reward': reward,
            'pnl': pnl,
            'delta_s': delta_s,
            'phi': phi,
            'grad_phi_norm': np.sqrt(grad_norm_sq),
            'grad_phi': grad_phi
        }
    
    def propose(self,
               x: Dict[str, np.ndarray],
               action_sampler: Callable,
               env_simulator: Callable,
               K: int = 8) -> List[Dict[str, Any]]:
        """
        Shadow phase: Generate K candidate transitions.
        
        No restrictions - explore freely.
        """
        candidates = []
        
        for k in range(K):
            # Sample action from policy
            a_k = action_sampler(x)
            
            # Simulate (deterministic, no IO)
            result = env_simulator(x, a_k)
            
            # Handle different return types
            if isinstance(result, tuple):
                x_next, pnl = result
            else:
                x_next = result
                pnl = 0.0
            
            # Compute full metrics
            metrics = self.compute_reward(x, x_next, pnl)
            
            candidates.append({
                'action': a_k,
                'next_state': x_next,
                'pnl': pnl,
                'metrics': metrics
            })
        
        return candidates
    
    def collapse(self,
                x: Dict[str, np.ndarray],
                candidates: List[Dict[str, Any]],
                lambda_scheduler: float = 1.0) -> Optional[Dict[str, Any]]:
        """
        Collapse phase: Enforce Φ=0, select optimal.
        
        Lawful collapse only - no violations committed.
        """
        best = None
        best_score = float('-inf')
        
        for c in candidates:
            metrics = c['metrics']
            
            # STRICT ENFORCEMENT: Φ must be 0
            if metrics['phi'] > 1e-6:
                continue
            
            # Score with scheduler-adjusted weights
            score = (self.weights.alpha * c['pnl'] -
                     self.weights.beta * metrics['delta_s'] -
                     (self.weights.gamma * lambda_scheduler) * metrics['phi'])
            
            if score > best_score:
                best_score = score
                best = c
        
        return best  # None if no lawful candidate found
    
    def execute(self,
               x: Dict[str, np.ndarray],
               action_sampler: Callable,
               env_simulator: Callable,
               K: int = 8,
               lambda_scheduler: float = 1.0) -> Tuple[Optional[Dict[str, Any]], Dict[str, Any]]:
        """
        Full shadow → collapse pipeline.
        
        Returns:
            (selected_candidate, audit_info)
        """
        # Shadow phase: explore
        candidates = self.propose(x, action_sampler, env_simulator, K)
        
        # Collapse phase: enforce and select
        selected = self.collapse(x, candidates, lambda_scheduler)
        
        # Audit info
        audit = {
            'n_candidates': len(candidates),
            'n_lawful': sum(1 for c in candidates if c['metrics']['phi'] < 1e-6),
            'phi_values': [c['metrics']['phi'] for c in candidates],
            'rewards': [c['metrics']['reward'] for c in candidates],
            'delta_s_values': [c['metrics']['delta_s'] for c in candidates]
        }
        
        return selected, audit
