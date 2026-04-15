"""
Blockchain Consensus - Tachyonic Hamiltonian

Blockchain state evolution with retrocausal dynamics.
Uses Polars for efficient chain history queries.
"""

import numpy as np
import polars as pl
from typing import List, Optional, Callable
from dataclasses import dataclass
from datetime import datetime

@dataclass
class BlockState:
    """
    Phase-space point for blockchain: (state_vector, validation_rate)
    
    NOTE: state_hash is kept for reference but state_vector is used for
    Hamiltonian mechanics (requires continuous, differentiable variables).
    """
    state_vector: np.ndarray  # q - Continuous state representation (e.g., hash embedding)
    validation_rate: float  # p - Rate of block production
    timestamp: float
    block_height: int
    state_hash: str = ""  # Reference only - not used in H computation
    
    def to_dict(self) -> dict:
        return {
            'state_hash': self.state_hash,
            'state_vector': self.state_vector.tolist(),
            'validation_rate': self.validation_rate,
            'timestamp': self.timestamp,
            'block_height': self.block_height,
        }


def hash_to_vector(state_hash: str, dim: int = 32) -> np.ndarray:
    """
    Deterministic hash embedding for continuous Hamiltonian formalism.
    
    Converts a hex string hash to a normalized float vector that can be
    used in Hamiltonian mechanics (requires continuous, differentiable variables).
    
    Args:
        state_hash: Hex string hash (e.g., from SHA-256)
        dim: Target dimension for state vector
        
    Returns:
        Normalized float vector in [0, 1]
    """
    # Remove '0x' prefix if present
    clean_hash = state_hash.replace('0x', '').replace('-', '')
    
    # Convert hex to bytes
    try:
        hash_bytes = bytes.fromhex(clean_hash)
    except ValueError:
        # If not valid hex, use UTF-8 encoding
        hash_bytes = clean_hash.encode('utf-8')
    
    # Pad or truncate to target dimension
    if len(hash_bytes) >= dim:
        padded = hash_bytes[:dim]
    else:
        # Pad with repetition
        padded = hash_bytes * (dim // len(hash_bytes) + 1)
        padded = padded[:dim]
    
    # Normalize to [0, 1]
    return np.array(list(padded), dtype=float) / 255.0


class TachyonicBlockchainHamiltonian:
    """
    Blockchain consensus as Hamiltonian with retrocausal terms.
    
    H = T(validation_rate) + V(state_divergence) + H_retro(future_state)
    
    Retrocausal term: future consensus state influences present validation.
    """
    
    def __init__(
        self,
        network_mass: float = 1.0,
        consensus_strength: float = 1.0,
        retrocausal_coupling: float = 0.1,
        target_block_time: float = 10.0
    ):
        self.M_network = network_mass
        self.kappa = consensus_strength
        self.lambda_retro = retrocausal_coupling
        self.t_target = target_block_time
    
    def kinetic_energy(self, validation_rate: float) -> float:
        """T = ½M·v² where v is validation rate"""
        return 0.5 * self.M_network * validation_rate**2
    
    def potential_energy(self, state_divergence: float) -> float:
        """
        V(Δ) = ½κ·Δ²
        
        where Δ = divergence from consensus
        """
        return 0.5 * self.kappa * state_divergence**2
    
    def retrocausal_potential(
        self,
        current_vector: np.ndarray,
        future_vector: Optional[np.ndarray],
        time_separation: float
    ) -> float:
        """
        Tachyonic term: V_retro = λ·||s_future - s_current||·exp(-t/τ)
        
        Future state creates backward-in-time potential.
        Uses continuous vector distance (differentiable) instead of Hamming distance.
        Decays exponentially with time separation.
        """
        if future_vector is None:
            return 0.0
        
        # Continuous L2 distance (differentiable)
        divergence = np.linalg.norm(current_vector - future_vector)
        
        # Exponential decay with time
        decay = np.exp(-time_separation / self.t_target)
        
        return self.lambda_retro * divergence * decay
    
    def total_hamiltonian(
        self,
        state: BlockState,
        consensus_vector: np.ndarray,
        future_state: Optional[BlockState] = None
    ) -> float:
        """
        H_total = T + V + V_retro
        
        Uses continuous state_vector for differentiable Hamiltonian formalism.
        """
        # Continuous state divergence from consensus (L2 norm)
        divergence = np.linalg.norm(state.state_vector - consensus_vector)
        
        H = self.kinetic_energy(state.validation_rate)
        H += self.potential_energy(divergence)
        
        if future_state:
            time_sep = future_state.timestamp - state.timestamp
            H += self.retrocausal_potential(
                state.state_vector,
                future_state.state_vector,
                time_sep
            )
        
        return H
    
    def validation_force(
        self,
        current_state: BlockState,
        consensus_vector: np.ndarray,
        future_state: Optional[BlockState] = None
    ) -> float:
        """
        F = -∂H/∂(state) = pull toward consensus + retrocausal pull
        
        Uses continuous gradient (differentiable) for Hamiltonian force.
        Returns: adjustment to validation rate
        """
        # Forward consensus force (gradient of potential)
        # V = ½κ·||q - q_consensus||²
        # F = -∂V/∂q = -κ·(q - q_consensus)
        delta = current_state.state_vector - consensus_vector
        F_consensus = -self.kappa * np.mean(delta)  # Average over dimensions
        
        # Retrocausal force from future
        F_retro = 0.0
        if future_state:
            future_delta = current_state.state_vector - future_state.state_vector
            future_div = np.linalg.norm(future_delta)
            
            time_sep = future_state.timestamp - current_state.timestamp
            decay = np.exp(-time_sep / self.t_target)
            
            F_retro = -self.lambda_retro * future_div * decay
        
        return F_consensus + F_retro


class PolarsBlockchainHistory:
    """
    Blockchain history with Polars lazy evaluation.
    
    Efficient queries over chain state evolution.
    """
    
    def __init__(self):
        self.chain_data: List[dict] = []
    
    def add_block(self, state: BlockState):
        """Append block to history"""
        self.chain_data.append(state.to_dict())
    
    def to_lazy_frame(self) -> pl.LazyFrame:
        """Convert to Polars LazyFrame for efficient queries"""
        if not self.chain_data:
            return pl.DataFrame().lazy()
        
        return pl.DataFrame(self.chain_data).lazy()
    
    def query_consensus_at_height(self, height: int) -> pl.LazyFrame:
        """Find consensus state at given block height"""
        return (
            self.to_lazy_frame()
            .filter(pl.col('block_height') == height)
        )
    
    def compute_chain_energy(self, hamiltonian: TachyonicBlockchainHamiltonian) -> pl.LazyFrame:
        """
        Compute Hamiltonian energy for entire chain history.
        
        Uses lazy evaluation - only computed when .collect() called.
        """
        lf = self.to_lazy_frame()
        
        # This would need custom logic - simplified here
        return lf.with_columns([
            pl.col('validation_rate').alias('kinetic_energy'),
            pl.lit(0.0).alias('potential_energy'),  # Placeholder
        ])
    
    def detect_forks(self) -> pl.LazyFrame:
        """
        Identify blockchain forks (state divergences).
        
        Lazy query - optimized by Polars.
        """
        return (
            self.to_lazy_frame()
            .with_columns([
                pl.col('state_hash').shift(1).alias('prev_hash'),
            ])
            .with_columns([
                (pl.col('state_hash') != pl.col('prev_hash')).alias('is_fork')
            ])
            .filter(pl.col('is_fork'))
        )
    
    def retrocausal_correlation(self, lookahead: int = 10) -> pl.LazyFrame:
        """
        Measure correlation between past and future states.
        
        Tests retrocausal hypothesis: does future influence past?
        """
        lf = self.to_lazy_frame()
        
        return lf.with_columns([
            # Future state (shifted)
            pl.col('state_hash').shift(-lookahead).alias('future_state'),
            pl.col('validation_rate').shift(-lookahead).alias('future_rate'),
        ]).with_columns([
            # Correlation (simplified - would need proper hash comparison)
            (
                pl.col('validation_rate') * pl.col('future_rate')
            ).alias('retrocausal_correlation')
        ])


def simulate_tachyonic_blockchain(
    hamiltonian: TachyonicBlockchainHamiltonian,
    n_blocks: int,
    consensus_target: str,
    initial_state: BlockState
) -> PolarsBlockchainHistory:
    """
    Simulate blockchain evolution with retrocausal dynamics.
    
    Args:
        hamiltonian: Tachyonic blockchain Hamiltonian
        n_blocks: Number of blocks to generate
        consensus_target: Target consensus state (string)
        initial_state: Genesis block (with state_vector)
    
    Returns:
        Complete blockchain history
    """
    history = PolarsBlockchainHistory()
    current_state = initial_state
    history.add_block(current_state)
    
    # Convert target hash to continuous vector
    consensus_vector = hash_to_vector(consensus_target)
    
    for i in range(1, n_blocks):
        # Future state (simulated oracle for demo)
        # In reality, this would be unknown
        future_state = None
        
        # Compute force using continuous vector
        F = hamiltonian.validation_force(current_state, consensus_vector, future_state)
        
        # Update validation rate (momentum)
        new_rate = current_state.validation_rate + 0.1 * F
        
        # Generate new state vector (moving toward consensus)
        # Linear interpolation toward target with some noise
        new_vector = current_state.state_vector + 0.1 * (consensus_vector - current_state.state_vector)
        new_vector += np.random.randn(len(new_vector)) * 0.01  # Small noise
        new_vector = np.clip(new_vector, 0, 1)  # Keep normalized
        
        # Generate corresponding hash (for reference)
        hash_bytes = (new_vector * 255).astype(np.uint8)
        new_hash = hash_bytes.tobytes().hex()[:32]  # Truncate to reasonable length
        
        # Create new block
        new_state = BlockState(
            state_vector=new_vector,
            validation_rate=new_rate,
            timestamp=current_state.timestamp + hamiltonian.t_target,
            block_height=i,
            state_hash=new_hash
        )
        
        history.add_block(new_state)
        current_state = new_state
    
    return history
