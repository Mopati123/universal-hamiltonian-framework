"""
Unified Data Pipeline

Combines data from multiple sources (MT5, Deriv, TradingView, Alpaca, yfinance)
into a single, aligned dataset for Hamiltonian analysis.

Features:
- Timestamp alignment across sources
- Consensus price calculation
- Phase space variable computation (S, p)
- Missing data handling
- Export to Hamiltonian-ready format
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')


class UnifiedDataPipeline:
    """
    Pipeline for unifying multi-source market data.
    
    Process:
    1. Collect data from all sources
    2. Align timestamps (within tolerance)
    3. Calculate consensus prices
    4. Compute phase space variables (S, p)
    5. Export for Hamiltonian analysis
    """
    
    def __init__(self):
        self.data_sources = {
            'MT5': None,
            'Deriv': None,
            'TradingView': None,
            'Alpaca': None,
            'yfinance': None
        }
        self.unified_data = None
        self.phase_space_data = None
    
    def add_source_data(self, source_name, data):
        """
        Add data from a source.
        
        Args:
            source_name (str): Name of source ('MT5', 'Deriv', etc.)
            data (pd.DataFrame): Data with 'timestamp' and price columns
        """
        if source_name not in self.data_sources:
            raise ValueError(f"Unknown source: {source_name}")
        
        if data is None or data.empty:
            print(f"⚠️  Warning: No data provided for {source_name}")
            return
        
        # Ensure timestamp column
        if 'timestamp' not in data.columns:
            raise ValueError(f"{source_name} data must have 'timestamp' column")
        
        # Convert to datetime
        data = data.copy()
        data['timestamp'] = pd.to_datetime(data['timestamp'])
        
        self.data_sources[source_name] = data
        
        print(f"✅ Added {len(data):,} records from {source_name}")
        print(f"   Period: {data['timestamp'].min()} to {data['timestamp'].max()}")
    
    def align_timestamps(self, tolerance_ms=1000, method='nearest'):
        """
        Align data across sources by timestamp.
        
        Args:
            tolerance_ms (int): Tolerance in milliseconds for alignment
            method (str): Alignment method ('nearest', 'forward', 'backward')
        
        Returns:
            pd.DataFrame: Combined data with aligned timestamps
        """
        print(f"\n🔄 Aligning timestamps (tolerance={tolerance_ms}ms, method={method})...")
        
        active_sources = {k: v for k, v in self.data_sources.items() if v is not None}
        
        if not active_sources:
            raise Exception("No data sources added")
        
        print(f"   Sources: {', '.join(active_sources.keys())}")
        
        # Combine all data
        all_dfs = []
        for source, df in active_sources.items():
            df_copy = df.copy()
            df_copy['source'] = source
            all_dfs.append(df_copy)
        
        combined = pd.concat(all_dfs, ignore_index=True)
        
        # Sort by timestamp
        combined = combined.sort_values('timestamp').reset_index(drop=True)
        
        # Round timestamps to alignment tolerance
        combined['timestamp_aligned'] = combined['timestamp'].dt.floor(f'{tolerance_ms}ms')
        
        print(f"✅ Combined {len(combined):,} records from {len(active_sources)} sources")
        print(f"   Time range: {combined['timestamp'].min()} to {combined['timestamp'].max()}")
        
        return combined
    
    def create_unified_dataset(self, resample_freq='1S', agg_method='last'):
        """
        Create unified dataset with consensus pricing.
        
        Args:
            resample_freq (str): Resampling frequency ('1S', '100ms', '1Min', etc.)
            agg_method (str): Aggregation method ('last', 'mean', 'median')
        
        Returns:
            pd.DataFrame: Unified dataset with one row per time interval
        """
        print(f"\n📊 Creating unified dataset (freq={resample_freq}, agg={agg_method})...")
        
        aligned = self.align_timestamps()
        
        # Separate price data by source
        price_cols = ['last_price', 'close', 'bid_price', 'ask_price']
        
        # Create pivot table
        result_dfs = []
        
        for price_col in price_cols:
            if price_col in aligned.columns:
                pivot = aligned.pivot_table(
                    index='timestamp_aligned',
                    columns='source',
                    values=price_col,
                    aggfunc=agg_method
                )
                
                # Rename columns
                pivot.columns = [f'{price_col}_{src}' for src in pivot.columns]
                result_dfs.append(pivot)
        
        # Combine all price types
        if result_dfs:
            unified = pd.concat(result_dfs, axis=1)
        else:
            raise Exception("No price columns found in data")
        
        # Resample to consistent frequency
        unified = unified.resample(resample_freq).last()
        
        # Forward fill missing values (carry last known price)
        unified = unified.fillna(method='ffill')
        
        # Calculate consensus price (average across all price columns)
        all_price_cols = [col for col in unified.columns if any(p in col for p in price_cols)]
        unified['consensus_price'] = unified[all_price_cols].mean(axis=1, skipna=True)
        
        # Calculate bid-ask spread if available
        bid_cols = [col for col in unified.columns if 'bid_price' in col]
        ask_cols = [col for col in unified.columns if 'ask_price' in col]
        
        if bid_cols and ask_cols:
            unified['avg_bid'] = unified[bid_cols].mean(axis=1, skipna=True)
            unified['avg_ask'] = unified[ask_cols].mean(axis=1, skipna=True)
            unified['spread'] = unified['avg_ask'] - unified['avg_bid']
            unified['spread_pct'] = (unified['spread'] / unified['consensus_price']) * 100
        
        # Calculate data quality metrics
        unified['sources_count'] = unified[all_price_cols].notna().sum(axis=1)
        unified['price_std'] = unified[all_price_cols].std(axis=1, skipna=True)
        unified['price_cv'] = (unified['price_std'] / unified['consensus_price']) * 100  # Coefficient of variation
        
        self.unified_data = unified
        
        print(f"✅ Unified dataset created: {len(unified):,} records")
        print(f"   Frequency: {resample_freq}")
        print(f"   Avg sources per timestamp: {unified['sources_count'].mean():.1f}")
        print(f"   Price consensus std dev: ${unified['price_std'].mean():.4f}")
        
        return unified
    
    def calculate_phase_space_variables(self):
        """
        Calculate Hamiltonian phase space variables (S, p).
        
        Returns:
            pd.DataFrame: Data with phase space coordinates
        """
        print(f"\n⚛️  Calculating phase space variables (S, p)...")
        
        if self.unified_data is None:
            raise Exception("Create unified dataset first")
        
        df = self.unified_data.copy()
        
        # Configuration variable (q): Stock price
        df['S'] = df['consensus_price']
        
        # Momentum variable (p): Price change rate
        df['dS'] = df['S'].diff()
        df['dt'] = df.index.to_series().diff().dt.total_seconds()
        df['p'] = df['dS'] / df['dt']  # Price velocity ($/second)
        
        # Replace inf values
        df['p'] = df['p'].replace([np.inf, -np.inf], np.nan)
        
        # Calculate volatility (for Hamiltonian)
        df['returns'] = df['S'].pct_change()
        df['volatility_5min'] = df['returns'].rolling(window=300).std() * np.sqrt(252 * 252)  # Annualized
        df['volatility_1min'] = df['returns'].rolling(window=60).std() * np.sqrt(252 * 252)
        
        # Calculate Hamiltonian components
        r = 0.05 / 252 / 252  # Risk-free rate per second (approximate)
        sigma = df['volatility_1min'].fillna(df['volatility_1min'].mean())
        
        df['H_kinetic'] = 0.5 * sigma**2 * df['S']**2 * df['p']**2  # Kinetic energy
        df['H_drift'] = r * df['S'] * df['p']  # Drift term
        df['H_total'] = df['H_kinetic'] + df['H_drift']  # Total Hamiltonian
        
        # Forward fill NaNs
        df = df.fillna(method='ffill')
        
        # Drop remaining NaNs
        initial_len = len(df)
        df = df.dropna(subset=['S', 'p'])
        dropped = initial_len - len(df)
        
        self.phase_space_data = df
        
        print(f"✅ Phase space calculated")
        print(f"   Valid records: {len(df):,} (dropped {dropped} with NaN)")
        print(f"   S (price) range: ${df['S'].min():.2f} - ${df['S'].max():.2f}")
        print(f"   p (momentum) range: {df['p'].min():.4f} - {df['p'].max():.4f} $/s")
        print(f"   H (Hamiltonian) mean: {df['H_total'].mean():.6f}")
        
        return df
    
    def detect_arbitrage_opportunities(self, threshold_pct=0.05):
        """
        Detect cross-platform arbitrage opportunities.
        
        Args:
            threshold_pct (float): Minimum price difference as percentage
        
        Returns:
            pd.DataFrame: Timestamps with arbitrage opportunities
        """
        print(f"\n💰 Detecting arbitrage opportunities (threshold={threshold_pct}%)...")
        
        if self.unified_data is None:
            raise Exception("Create unified dataset first")
        
        df = self.unified_data.copy()
        
        # Get all price columns
        price_cols = [col for col in df.columns if 'price' in col and 'consensus' not in col]
        
        if len(price_cols) < 2:
            print("⚠️  Need at least 2 price sources for arbitrage detection")
            return pd.DataFrame()
        
        # Calculate min and max prices across sources
        df['price_min'] = df[price_cols].min(axis=1)
        df['price_max'] = df[price_cols].max(axis=1)
        df['price_spread_abs'] = df['price_max'] - df['price_min']
        df['price_spread_pct'] = (df['price_spread_abs'] / df['consensus_price']) * 100
        
        # Find arbitrage opportunities
        arbitrage = df[df['price_spread_pct'] > threshold_pct].copy()
        
        if len(arbitrage) > 0:
            # Identify which sources have min/max
            for idx in arbitrage.index:
                row_prices = df.loc[idx, price_cols]
                arbitrage.loc[idx, 'buy_from'] = row_prices.idxmin()
                arbitrage.loc[idx, 'sell_to'] = row_prices.idxmax()
            
            print(f"✅ Found {len(arbitrage)} arbitrage opportunities")
            print(f"   Max spread: {arbitrage['price_spread_pct'].max():.4f}%")
            print(f"   Avg spread: {arbitrage['price_spread_pct'].mean():.4f}%")
        else:
            print(f"✅ No arbitrage opportunities (threshold {threshold_pct}%)")
        
        return arbitrage[['price_min', 'price_max', 'price_spread_abs', 'price_spread_pct', 'buy_from', 'sell_to']]
    
    def export_for_hamiltonian(self, output_file='unified_market_data.csv'):
        """
        Export processed data for Hamiltonian analysis.
        
        Args:
            output_file (str): Output CSV filename
        
        Returns:
            pd.DataFrame: Exported data
        """
        print(f"\n💾 Exporting data for Hamiltonian analysis...")
        
        if self.phase_space_data is None:
            raise Exception("Calculate phase space variables first")
        
        # Select key columns for export
        export_cols = [
            'S', 'p',  # Phase space
            'consensus_price', 'spread', 'spread_pct',  # Pricing
            'volatility_1min', 'volatility_5min',  # Volatility
            'H_kinetic', 'H_drift', 'H_total',  # Hamiltonian
            'sources_count', 'price_std', 'price_cv'  # Quality metrics
        ]
        
        # Only include columns that exist
        export_cols = [col for col in export_cols if col in self.phase_space_data.columns]
        
        export_df = self.phase_space_data[export_cols].copy()
        
        # Save to CSV
        export_df.to_csv(output_file)
        
        print(f"✅ Exported to {output_file}")
        print(f"   Records: {len(export_df):,}")
        print(f"   Columns: {len(export_cols)}")
        print(f"   File size: {export_df.memory_usage(deep=True).sum() / 1024:.1f} KB")
        
        return export_df
    
    def get_summary_stats(self):
        """Get summary statistics of unified dataset."""
        
        if self.phase_space_data is None:
            print("❌ No phase space data available")
            return None
        
        df = self.phase_space_data
        
        stats = {
            'records': len(df),
            'time_range': f"{df.index.min()} to {df.index.max()}",
            'duration': str(df.index.max() - df.index.min()),
            
            'price_mean': df['S'].mean(),
            'price_std': df['S'].std(),
            'price_min': df['S'].min(),
            'price_max': df['S'].max(),
            
            'momentum_mean': df['p'].mean(),
            'momentum_std': df['p'].std(),
            
            'hamiltonian_mean': df['H_total'].mean(),
            'hamiltonian_std': df['H_total'].std(),
            
            'avg_sources': df['sources_count'].mean(),
            'avg_spread_pct': df.get('spread_pct', pd.Series([0])).mean()
        }
        
        print("\n📊 Summary Statistics:")
        print(f"   Records: {stats['records']:,}")
        print(f"   Duration: {stats['duration']}")
        print(f"   Price: ${stats['price_mean']:.2f} ± ${stats['price_std']:.2f}")
        print(f"   Momentum: {stats['momentum_mean']:.6f} ± {stats['momentum_std']:.6f} $/s")
        print(f"   Hamiltonian: {stats['hamiltonian_mean']:.6f} ± {stats['hamiltonian_std']:.6f}")
        print(f"   Avg sources/timestamp: {stats['avg_sources']:.1f}")
        print(f"   Avg spread: {stats['avg_spread_pct']:.4f}%")
        
        return stats


# Example usage
if __name__ == "__main__":
    print("=" * 70)
    print("Unified Data Pipeline - Example Usage")
    print("=" * 70)
    
    # This would normally use real data from the collectors
    # Creating synthetic example data
    
    import numpy as np
    
    # Simulate data from different sources
    timestamps = pd.date_range('2024-12-08 09:30:00', periods=1000, freq='1S')
    base_price = 450.0
    
    # MT5 data
    mt5_data = pd.DataFrame({
        'timestamp': timestamps,
        'last_price': base_price + np.random.randn(len(timestamps)) * 0.1,
        'symbol': 'SPY'
    })
    
    # Alpaca data
    alpaca_data = pd.DataFrame({
        'timestamp': timestamps + pd.Timedelta('100ms'),  # Slight delay
        'last_price': base_price + np.random.randn(len(timestamps)) * 0.12,
        'symbol': 'SPY'
    })
    
    # Create pipeline
    pipeline = UnifiedDataPipeline()
    
    # Add data sources
    pipeline.add_source_data('MT5', mt5_data)
    pipeline.add_source_data('Alpaca', alpaca_data)
    
    # Create unified dataset
    unified = pipeline.create_unified_dataset(resample_freq='1S')
    
    # Calculate phase space
    phase_space = pipeline.calculate_phase_space_variables()
    
    # Detect arbitrage
    arbitrage = pipeline.detect_arbitrage_opportunities(threshold_pct=0.1)
    
    # Export
    export_data = pipeline.export_for_hamiltonian('example_unified_data.csv')
    
    # Summary stats
    stats = pipeline.get_summary_stats()
    
    print("\n✅ Pipeline demonstration complete!")
