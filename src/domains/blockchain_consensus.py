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
    """Phase-space point for blockchain: (state, validation_rate)"""
    state_hash: str  # q - Network consensus state
    validation_rate: float  # p - Rate of block production
    timestamp: float
    block_height: int
    
    def to_dict(self) -> dict:
        return {
            'state_hash': self.state_hash,
            'validation_rate': self.validation_rate,
            'timestamp': self.timestamp,
            'block_height': self.block_height,
        }


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
        current_state: str,
        future_state: Optional[str],
        time_separation: float
    ) -> float:
        """
        Tachyonic term: V_retro = λ·f(s_future, s_current)·exp(-t/τ)
        
        Future state creates backward-in-time potential.
        Decays exponentially with time separation.
        """
        if future_state is None:
            return 0.0
        
        # Hamming distance as state divergence
        divergence = sum(c1 != c2 for c1, c2 in zip(current_state, future_state))
        divergence /= len(current_state)  # Normalize
        
        # Exponential decay with time
        decay = np.exp(-time_separation / self.t_target)
        
        return self.lambda_retro * divergence * decay
    
    def total_hamiltonian(
        self,
        state: BlockState,
        consensus_state: str,
        future_state: Optional[BlockState] = None
    ) -> float:
        """H_total = T + V + V_retro"""
        # State divergence from consensus
        divergence = sum(
            c1 != c2 for c1, c2 in zip(state.state_hash, consensus_state)
        ) / len(state.state_hash)
        
        H = self.kinetic_energy(state.validation_rate)
        H += self.potential_energy(divergence)
        
        if future_state:
            time_sep = future_state.timestamp - state.timestamp
            H += self.retrocausal_potential(
                state.state_hash,
                future_state.state_hash,
                time_sep
            )
        
        return H
    
    def validation_force(
        self,
        current_state: BlockState,
        consensus_state: str,
        future_state: Optional[BlockState] = None
    ) -> float:
        """
        F = -∂H/∂(state) = pull toward consensus + retrocausal pull
        
        Returns: adjustment to validation rate
        """
        # Forward consensus force
        divergence = sum(
            c1 != c2 for c1, c2 in zip(current_state.state_hash, consensus_state)
        ) / len(current_state.state_hash)
        
        F_consensus = -self.kappa * divergence
        
        # Retrocausal force from future
        F_retro = 0.0
        if future_state:
            future_div = sum(
                c1 != c2 
                for c1, c2 in zip(current_state.state_hash, future_state.state_hash)
            ) / len(current_state.state_hash)
            
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
        consensus_target: Target consensus state
        initial_state: Genesis block
    
    Returns:
        Complete blockchain history
    """
    history = PolarsBlockchainHistory()
    current_state = initial_state
    history.add_block(current_state)
    
    for i in range(1, n_blocks):
        # Future state (simulated oracle for demo)
        # In reality, this would be unknown
        future_state = None
        
        # Compute force
        F = hamiltonian.validation_force(current_state, consensus_target, future_state)
        
        # Update validation rate (momentum)
        new_rate = current_state.validation_rate + 0.1 * F
        
        # Generate new block
        new_state = BlockState(
            state_hash=consensus_target[:i % len(consensus_target)] + 
                       consensus_target[i % len(consensus_target):],
            validation_rate=new_rate,
            timestamp=current_state.timestamp + hamiltonian.t_target,
            block_height=i
        )
        
        history.add_block(new_state)
        current_state = new_state
    
    return history
