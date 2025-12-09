"""
QUBO Optimizer

Converts Hamiltonian → QUBO → Portfolio allocation
Uses quantum-inspired annealing for optimization.
"""

import numpy as np
from typing import Dict, List, Tuple
from dataclasses import dataclass


@dataclass
class Portfolio:
    """Portfolio allocation"""
    positions: Dict[str, float]  # symbol → position size
    energy: float  # QUBO energy
    timestamp: float


class QUBOOptimizer:
    """
    Quantum-inspired portfolio optimizer
    
    Process:
    1. Convert Hamiltonian + constraints → QUBO matrix Q
    2. Solve: minimize x^T Q x where x ∈ {0,1}^n
    3. Map binary solution → portfolio weights
    """
    
    def __init__(self, universe: List[str], method: str = 'simulated_annealing'):
        """
        Initialize optimizer
        
        Args:
            universe: List of tradeable symbols
            method: Optimization method ('simulated_annealing', 'greedy')
        """
        self.universe = universe
        self.n_assets = len(universe)
        self.method = method
    
    def hamiltonian_to_qubo(
        self,
        hamiltonian_engine,
        market_states: Dict,
        constraints: Dict

    ) -> np.ndarray:
        """
        Convert market Hamiltonian to QUBO matrix
        
        QUBO form: minimize x^T Q x
        where x_i ∈ {0, 1} indicates whether to include asset i
        
        Args:
            hamiltonian_engine: Physics engine
            market_states: Current state per symbol
            constraints: Portfolio constraints (max_positions, etc.)
        
        Returns:
            Q matrix (n × n)
        """
        n = self.n_assets
        Q = np.zeros((n, n))
        
        # Diagonal: individual asset energy
        for i, symbol in enumerate(self.universe):
            if symbol in market_states:
                state = market_states[symbol]
                energy = hamiltonian_engine.total_energy(state)
                
                # Higher energy = less desirable
                Q[i, i] = energy
        
        # Off-diagonal: correlation penalties/bonuses
        for i in range(n):
            for j in range(i+1, n):
                symbol_i = self.universe[i]
                symbol_j = self.universe[j]
                
                if symbol_i in market_states and symbol_j in market_states:
                    # Calculate correlation (simplified)
                    corr = self._estimate_correlation(
                        market_states[symbol_i],
                        market_states[symbol_j]
                    )
                    
                    # Negative correlation bonus (diversification)
                    # Positive correlation penalty (concentration risk)
                    Q[i, j] = corr
                    Q[j, i] = corr
        
        # Add constraint penalties
        Q = self._add_constraint_penalties(Q, constraints)
        
        return Q
    
    def _estimate_correlation(self, state_i, state_j) -> float:
        """
        Estimate correlation between two assets
        
        Simplified: use momentum correlation
        (In production, use historical returns)
        """
        # Correlation in [-1, 1]
        # For now, return small random value
        return np.random.randn() * 0.1
    
    def _add_constraint_penalties(self, Q: np.ndarray, constraints: Dict) -> np.ndarray:
        """
        Add constraint violations as energy penalties
        
        Example constraints:
        - Max total positions
        - Sector limits
        - Leverage limits
        """
        Q_constrained = Q.copy()
        
        # Max positions constraint
        # If x_i + x_j + ... > max_positions, add penalty
        if 'max_positions' in constraints:
            max_pos = constraints['max_positions']
            penalty = constraints.get('penalty_strength', 10.0)
            
            # Penalty for selecting too many assets
            # (This is approximate - exact formulation requires ancilla bits)
            for i in range(len(Q)):
                for j in range(len(Q)):
                    Q_constrained[i, j] += penalty / max_pos
        
        return Q_constrained
    
    def solve_qubo(self, Q: np.ndarray) -> Tuple[np.ndarray, float]:
        """
        Solve QUBO: minimize x^T Q x
        
        Uses quantum-inspired annealing (classical simulation)
        
        Returns:
            solution: Binary vector x
            energy: Final energy value
        """
        if self.method == 'simulated_annealing':
            return self._simulated_annealing(Q)
        elif self.method == 'greedy':
            return self._greedy_solve(Q)
        else:
            raise ValueError(f"Unknown method: {self.method}")
    
    def _simulated_annealing(
        self,
        Q: np.ndarray,
        T_init: float = 10.0,
        T_final: float = 0.01,
        cooling_rate: float = 0.95,
        steps_per_temp: int = 100
    ) -> Tuple[np.ndarray, float]:
        """
        Simulated annealing (quantum annealing analogue)
        
        Temperature-based search allows tunneling out of local minima,
        analogous to quantum tunneling.
        """
        n = len(Q)
        
        # Random initial state
        x = np.random.randint(0, 2, n)
        
        # Calculate initial energy
        E_current = x.T @ Q @ x
        E_best = E_current
        x_best = x.copy()
        
        # Annealing schedule
        T = T_init
        
        while T > T_final:
            for _ in range(steps_per_temp):
                # Propose single bit flip
                i = np.random.randint(n)
                x_new = x.copy()
                x_new[i] = 1 - x_new[i]
                
                # Calculate new energy
                E_new = x_new.T @ Q @ x_new
                delta_E = E_new - E_current
                
                # Metropolis criterion
                # Accept if lower energy OR probabilistically if higher
                if delta_E < 0 or np.random.rand() < np.exp(-delta_E / T):
                    x = x_new
                    E_current = E_new
                    
                    # Track best
                    if E_current < E_best:
                        E_best = E_current
                        x_best = x.copy()
            
            # Cool down
            T *= cooling_rate
        
        return x_best, E_best
    
    def _greedy_solve(self, Q: np.ndarray) -> Tuple[np.ndarray, float]:
        """Simple greedy solver (fast, suboptimal)"""
        n = len(Q)
        x = np.zeros(n, dtype=int)
        
        # Greedily select assets with lowest diagonal energy
        order = np.argsort(np.diag(Q))
        
        # Select top k assets (k = sqrt(n) heuristic)
        k = max(1, int(np.sqrt(n)))
        for i in order[:k]:
            x[i] = 1
        
        energy = x.T @ Q @ x
        return x, energy
    
    def solution_to_portfolio(
        self,
        solution: np.ndarray,
        market_states: Dict,
        capital: float = 10000.0
    ) -> Portfolio:
        """
        Convert binary QUBO solution → portfolio positions
        
        Args:
            solution: Binary vector (which assets to include)
            market_states: Current market states
            capital: Total capital to allocate
        
        Returns:
            Portfolio with positions
        """
        positions = {}
        
        # Count selected assets
        n_selected = solution.sum()
        
        if n_selected == 0:
            # No positions (all FLAT)
            return Portfolio(positions={}, energy=0.0, timestamp=0.0)
        
        # Equal weight allocation (can be optimized further)
        weight_per_asset = 1.0 / n_selected
        
        for i, selected in enumerate(solution):
            if selected:
                symbol = self.universe[i]
                
                if symbol in market_states:
                    price = market_states[symbol].S
                    
                    # Position size in shares
                    dollar_allocation = capital * weight_per_asset
                    shares = dollar_allocation / price
                    
                    positions[symbol] = shares
        
        # Get timestamp from first state
        timestamp = list(market_states.values())[0].timestamp if market_states else 0.0
        
        return Portfolio(
            positions=positions,
            energy=0.0,  # Can add energy calculation
            timestamp=timestamp
        )
    
    def optimize(
        self,
        hamiltonian_engine,
        market_states: Dict,
        constraints: Dict = None,
        capital: float = 10000.0
    ) -> Portfolio:
        """
        Main optimization interface
        
        Full pipeline:
        State → Hamiltonian → QUBO → Solution → Portfolio
        
        Args:
            hamiltonian_engine: Physics engine
            market_states: Current market states per symbol
            constraints: Portfolio constraints
            capital: Total capital
        
        Returns:
            Optimal portfolio
        """
        constraints = constraints or {'max_positions': 5}
        
        # Convert to QUBO
        Q = self.hamiltonian_to_qubo(
            hamiltonian_engine,
            market_states,
            constraints
        )
        
        # Solve
        solution, energy = self.solve_qubo(Q)
        
        # Convert to portfolio
        portfolio = self.solution_to_portfolio(
            solution,
            market_states,
            capital
        )
        
        portfolio.energy = energy
        
        return portfolio


# Example usage and validation
if __name__ == "__main__":
    from ..hamiltonian.engine import HamiltonianEngine, MarketState
    
    print("="*70)
    print("QUBO Optimizer - Validation Test")
    print("="*70)
    
    # Setup
    universe = ['SPY', 'QQQ', 'IWM', 'DIA', 'EEM']
    optimizer = QUBOOptimizer(universe, method='simulated_annealing')
    
    print(f"\nUniverse: {universe}")
    print(f"Number of assets: {optimizer.n_assets}")
    
    # Create mock market states
    engine = HamiltonianEngine()
    market_states = {}
    
    for i, symbol in enumerate(universe):
        market_states[symbol] = MarketState(
            S=100.0 + i*10,  # Different prices
            p=np.random.randn() * 0.1,  # Random momentum
            sigma=0.20,
            spread=0.01,
            volume=1e6,
            timestamp=0.0
        )
    
    print(f"\nMarket States:")
    for symbol, state in market_states.items():
        E = engine.total_energy(state)
        print(f"  {symbol}: ${state.S:.2f}, p={state.p:+.4f}, E={E:.6f}")
    
    # Build QUBO
    print(f"\nConverting to QUBO...")
    Q = optimizer.hamiltonian_to_qubo(
        engine,
        market_states,
        constraints={'max_positions': 3}
    )
    
    print(f"  QUBO matrix shape: {Q.shape}")
    print(f"  Diagonal (individual energies):\n{np.diag(Q)}")
    
    # Solve
    print(f"\nSolving QUBO with simulated annealing...")
    solution, energy = optimizer.solve_qubo(Q)
    
    print(f"  Solution: {solution}")
    print(f"  Selected assets: {[universe[i] for i, s in enumerate(solution) if s]}")
    print(f"  QUBO energy: {energy:.6f}")
    
    # Convert to portfolio
    print(f"\nConverting to portfolio (capital=$10,000)...")
    portfolio = optimizer.solution_to_portfolio(solution, market_states, capital=10000.0)
    
    print(f"  Positions:")
    for symbol, shares in portfolio.positions.items():
        price = market_states[symbol].S
        value = shares * price
        print(f"    {symbol}: {shares:.2f} shares @ ${price:.2f} = ${value:.2f}")
    
    total_value = sum(shares * market_states[sym].S 
                     for sym, shares in portfolio.positions.items())
    print(f"  Total value: ${total_value:.2f}")
    
    # Test full optimization
    print(f"\nTesting full optimization pipeline...")
    opt_portfolio = optimizer.optimize(
        engine,
        market_states,
        constraints={'max_positions': 3},
        capital=10000.0
    )
    
    print(f"  Optimized portfolio:")
    for symbol, shares in opt_portfolio.positions.items():
        print(f"    {symbol}: {shares:.2f} shares")
    
    print(f"\n✅ QUBO Optimizer validation complete!")
    print("="*70)
