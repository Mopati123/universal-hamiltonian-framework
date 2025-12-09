"""
Trading System

Main quantum-inspired trading system integrating all components.
This is what users run to actually trade.
"""

import sys
from pathlib import Path

# Add experiments path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

import numpy as np
import polars as pl  # Lazy execution = quantum superposition!
from typing import Dict, List
from datetime import datetime
import time

from ..hamiltonian.engine import HamiltonianEngine, MarketState
from ..quantum.wavefunction import QuantumDecisionLayer, TradingAction
from ..optimization.qubo import QUBOOptimizer, Portfolio

# Import Phase 2 data connectors
try:
    from experiments.markets.data_sources import (
        UnifiedDataPipeline,
        AlpacaDataCollector
    )
    DATA_AVAILABLE = True
except ImportError:
    DATA_AVAILABLE = False
    print("⚠️  Warning: Phase 2 data connectors not found. Using simulation mode.")


class TradingSystem:
    """
    Complete quantum-inspired trading system
    
    Architecture:
    Data → Hamiltonian → Quantum Layer → QUBO → Execution
    
    This is the practical application of Universal Hamiltonian Framework.
    """
    
    def __init__(
        self,
        universe: List[str] = None,
        capital: float = 10000.0,
        mode: str = 'simulation'
    ):
        """
        Initialize trading system
        
        Args:
            universe: List of symbols to trade
            capital: Total capital
            mode: 'simulation' or 'live'
        """
        self.universe = universe or ['SPY']
        self.capital = capital
        self.mode = mode
        
        # Initialize components
        self.hamiltonian_engine = HamiltonianEngine()
        self.quantum_layer = QuantumDecisionLayer()
        self.optimizer = QUBOOptimizer(self.universe)
        
        # Data pipeline (if available)
        if DATA_AVAILABLE and mode == 'live':
            self.data_pipeline = UnifiedDataPipeline()
            self.data_collector = AlpacaDataCollector()
        else:
            self.data_pipeline = None
            self.data_collector = None
        
        # State
        self.market_states = {}
        self.current_portfolio = Portfolio(positions={}, energy=0.0, timestamp=0.0)
        self.running = False
        
        # Logging
        self.log = []
    
    def initialize_market_states(self):
        """Initialize or update market states from data"""
        
        if self.mode == 'simulation':
            # Simulation: generate random states
            for symbol in self.universe:
                self.market_states[symbol] = MarketState(
                    S=100.0 + np.random.randn() * 10,
                    p=np.random.randn() * 0.1,
                    sigma=0.20,
                    spread=0.01,
                    volume=1e6,
                    timestamp=time.time()
                )
        
        elif self.mode == 'live' and DATA_AVAILABLE:
            # Live: get from real data
            for symbol in self.universe:
                try:
                    quote = self.data_collector.get_latest_quote(symbol)
                    
                    if quote:
                        self.market_states[symbol] = MarketState(
                            S=(quote['bid_price'] + quote['ask_price']) / 2,
                            p=0.0,  # Calculate from tick-to-tick
                            sigma=0.20,  # Estimate from recent volatility
                            spread=quote['spread'],
                            volume=quote['bid_size'] + quote['ask_size'],
                            timestamp=quote['timestamp'].timestamp()
                        )
                except Exception as e:
                    print(f"⚠️  Could not get data for {symbol}: {e}")
        
        else:
            raise ValueError(f"Invalid mode: {self.mode}")
    
    def event_loop_iteration(self):
        """
        Single iteration of event loop
        
        Process:
        1. Update market states
        2. Calculate Hamiltonian energies
        3. Update quantum wavefunction (VQE)
        4. Optimize portfolio (QUBO)
        5. Measure action
        6. Execute (simulated or real)
        7. Log results
        """
        
        # 1. UPDATE MARKET STATES
        self.initialize_market_states()
        
        # 2. CALCULATE HAMILTONIAN
        energies = {}
        for symbol, state in self.market_states.items():
            energies[symbol] = self.hamiltonian_engine.total_energy(state)
        
        # 3. UPDATE QUANTUM LAYER
        # Use first symbol's state for single-asset decision
        # (Multi-asset would use entangled state)
        primary_symbol = self.universe[0]
        primary_state = self.market_states[primary_symbol]
        
        trading_costs = {
            'LONG': 0.01,    # 1 cent per share
            'FLAT': 0.0,
            'SHORT': 0.01,
            'HEDGE': 0.02
        }
        
        self.quantum_layer.variational_update(
            self.hamiltonian_engine,
            primary_state,
            trading_costs
        )
        
        # 4. OPTIMIZE PORTFOLIO (QUBO)
        portfolio = self.optimizer.optimize(
            self.hamiltonian_engine,
            self.market_states,
            constraints={'max_positions': len(self.universe)},
            capital=self.capital
        )
        
        # 5. MEASURE ACTION
        action = self.quantum_layer.measure()
        
        # 6. EXECUTE (simulated for now)
        # In live mode, this would submit real orders
        execution_result = self._simulate_execution(portfolio, action)
        
        # 7. LOG
        log_entry = {
            'timestamp': time.time(),
            'market_states': self.market_states.copy(),
            'energies': energies,
            'quantum_probs': self.quantum_layer.probabilities().copy(),
            'action': action.value,
            'portfolio': portfolio,
            'execution': execution_result
        }
        self.log.append(log_entry)
        
        return log_entry
    
    def _simulate_execution(self, portfolio: Portfolio, action: TradingAction) -> Dict:
        """Simulate order execution"""
        
        # Calculate PnL from current vs new portfolio
        current_value = sum(
            shares * self.market_states[sym].S
            for sym, shares in self.current_portfolio.positions.items()
            if sym in self.market_states
        )
        
        new_value = sum(
            shares * self.market_states[sym].S
            for sym, shares in portfolio.positions.items()
            if sym in self.market_states
        )
        
        pnl = new_value - current_value
        
        # Update current portfolio
        self.current_portfolio = portfolio
        
        return {
            'action': action.value,
            'pnl': pnl,
            'current_value': new_value,
            'positions': portfolio.positions
        }
    
    def run(self, iterations: int = 10, delay: float = 1.0):
        """
        Run trading system for specified iterations
        
        Args:
            iterations: Number of event loop iterations
            delay: Seconds between iterations
        """
        print("="*70)
        print("QUANTUM-INSPIRED TRADING SYSTEM")
        print("="*70)
        print(f"\nConfiguration:")
        print(f"  Universe: {self.universe}")
        print(f"  Capital: ${self.capital:,.2f}")
        print(f"  Mode: {self.mode}")
        print(f"  Iterations: {iterations}")
        print(f"  Delay: {delay}s")
        print(f"\nStarting event loop...\n")
        
        self.running = True
        
        for i in range(iterations):
            if not self.running:
                break
            
            print(f"[Iteration {i+1}/{iterations}]")
            
            try:
                log_entry = self.event_loop_iteration()
                
                # Display results
                self._print_iteration_summary(log_entry)
                
            except Exception as e:
                print(f"❌ Error: {e}")
                import traceback
                traceback.print_exc()
            
            if i < iterations - 1:
                time.sleep(delay)
        
        print(f"\n{'='*70}")
        print(f"Event loop complete. Processed {len(self.log)} iterations.")
        print(f"{'='*70}\n")
        
        self._print_final_summary()
    
    def _print_iteration_summary(self, log_entry: Dict):
        """Print summary of single iteration"""
        
        # Show energies
        print(f"  Hamiltonian energies:")
        for symbol, energy in log_entry['energies'].items():
            state = log_entry['market_states'][symbol]
            print(f"    {symbol}: ${state.S:.2f}, E={energy:.6f}")
        
        # Show quantum state
        print(f"  Quantum layer:")
        probs = log_entry['quantum_probs']
        actions = list(TradingAction)
        for action, prob in zip(actions, probs):
            marker = "→" if action.value == log_entry['action'] else " "
            print(f"    {marker} {action.value}: {prob:.3f}")
        
        # Show action taken
        print(f"  ✓ Measured: {log_entry['action']}")
        
        # Show portfolio
        portfolio = log_entry['portfolio']
        if portfolio.positions:
            print(f"  Portfolio:")
            for symbol, shares in portfolio.positions.items():
                price = log_entry['market_states'][symbol].S
                value = shares * price
                print(f"    {symbol}: {shares:.2f} shares @ ${price:.2f} = ${value:.2f}")
        else:
            print(f"  Portfolio: FLAT (no positions)")
        
        # Show PnL
        pnl = log_entry['execution']['pnl']
        current_value = log_entry['execution']['current_value']
        print(f"  PnL: ${pnl:+.2f}, Total value: ${current_value:.2f}")
        
        print()
    
    def _print_final_summary(self):
        """Print summary of all iterations"""
        
        if not self.log:
            print("No data to summarize.")
            return
        
        # Calculate statistics
        pnls = [entry['execution']['pnl'] for entry in self.log]
        total_pnl = sum(pnls)
        avg_pnl = np.mean(pnls)
        std_pnl = np.std(pnls)
        
        actions_taken = [entry['action'] for entry in self.log]
        action_counts = {action.value: actions_taken.count(action.value) 
                        for action in TradingAction}
        
        print("📊 FINAL SUMMARY")
        print("="*70)
        print(f"\nPerformance:")
        print(f"  Total PnL: ${total_pnl:+.2f}")
        print(f"  Average PnL: ${avg_pnl:+.2f}")
        print(f"  Std Dev: ${std_pnl:.2f}")
        print(f"  Sharpe ratio: {avg_pnl / std_pnl:.2f}" if std_pnl > 0 else "  Sharpe ratio: N/A")
        
        print(f"\nAction distribution:")
        for action, count in action_counts.items():
            pct = count / len(self.log) * 100
            print(f"  {action}: {count} ({pct:.1f}%)")
        
        # Save log
        self.save_log()
        
        print(f"\n✅ Log saved to: trading_log.csv")
        print("="*70)
    
    def save_log(self, filename: str = 'trading_log.csv'):
        """
        Save trading log to CSV using Polars lazy execution
        
        Quantum insight: Build query in superposition (lazy),
        collapse to file only at the end (.collect() + write)
        """
        
        if not self.log:
            return
        
        # Flatten log for CSV (stay in superposition - use dict)
        rows = []
        for entry in self.log:
            row = {
                'timestamp': entry['timestamp'],
                'action': entry['action'],
                'pnl': entry['execution']['pnl'],
                'portfolio_value': entry['execution']['current_value']
            }
            
            # Add energies
            for symbol, energy in entry['energies'].items():
                row[f'{symbol}_energy'] = energy
                row[f'{symbol}_price'] = entry['market_states'][symbol].S
            
            rows.append(row)
        
        # Quantum collapse: Create lazy frame → optimize → write
        # This is lazy execution = superposition until write!
        (
            pl.LazyFrame(rows)
            .select([  # Define schema in superposition
                pl.col('timestamp'),
                pl.col('action'),
                pl.col('pnl'),
                pl.col('portfolio_value'),
                pl.col('^.*_energy$'),  # All energy columns
                pl.col('^.*_price$')    # All price columns
            ])
            .collect()  # ← Wavefunction collapse!
            .write_csv(filename)
        )
        
        # Alternative eager mode (if lazy not needed):
        # pl.DataFrame(rows).write_csv(filename)
    
    def stop(self):
        """Stop event loop"""
        self.running = False


# Main execution
if __name__ == "__main__":
    print("\n" + "="*70)
    print("QUANTUM-INSPIRED TRADING SYSTEM - DEMO")
    print("Practical Application of Universal Hamiltonian Framework")
    print("="*70 + "\n")
    
    # Create system
    system = TradingSystem(
        universe=['SPY', 'QQQ'],
        capital=10000.0,
        mode='simulation'
    )
    
    # Run for 10 iterations
    system.run(iterations=10, delay=0.5)
    
    print("\n🎉 Demo complete!")
    print("This demonstrates how mathematics underpins trading.")
    print("Check 'trading_log.csv' for detailed results.\n")
