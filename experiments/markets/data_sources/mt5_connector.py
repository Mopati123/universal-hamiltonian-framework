"""
MT5 (MetaTrader 5) Data Collector

Connects to MetaTrader 5 platform to collect raw tick data.
Requires MT5 terminal to be installed and account configured.
"""

import MetaTrader5 as mt5
from datetime import datetime, timedelta
import pandas as pd
import numpy as np


class MT5DataCollector:
    """
    Collector for MetaTrader 5 tick data.
    
    Features:
    - Raw tick data collection
    - OHLCV bars
    - Account connection management
    - Symbol information
    """
    
    def __init__(self):
        self.initialized = False
        self.account_info = None
    
    def connect(self, account=None, password=None, server=None):
        """
        Initialize MT5 connection.
        
        Args:
            account (int, optional): Trading account number
            password (str, optional): Account password
            server (str, optional): Broker server name
        
        Returns:
            bool: True if connection successful
        """
        # Initialize MT5
        if not mt5.initialize():
            error = mt5.last_error()
            print(f"❌ MT5 initialization failed: {error}")
            return False
        
        # Login if credentials provided
        if account and password and server:
            authorized = mt5.login(account, password=password, server=server)
            if not authorized:
                error = mt5.last_error()
                print(f"❌ MT5 login failed: {error}")
                mt5.shutdown()
                return False
        
        self.initialized = True
        self.account_info = mt5.account_info()
        
        if self.account_info:
            print(f"✅ MT5 Connected")
            print(f"   Account: {self.account_info.login}")
            print(f"   Server: {self.account_info.server}")
            print(f"   Balance: ${self.account_info.balance:.2f}")
        else:
            print(f"✅ MT5 Connected (demo mode)")
        
        return True
    
    def get_tick_data(self, symbol="EURUSD", start_date=None, end_date=None, count=10000):
        """
        Pull raw tick data from MT5.
        
        Args:
            symbol (str): Trading symbol (e.g., "EURUSD", "BTCUSD")
            start_date (str): Start date 'YYYY-MM-DD'
            end_date (str): End date 'YYYY-MM-DD'
            count (int): Number of ticks if dates not provided
        
        Returns:
            pd.DataFrame: Tick data with columns [timestamp, bid, ask, last, volume, source]
        """
        if not self.initialized:
            raise Exception("MT5 not connected. Call connect() first.")
        
        # Get ticks
        if start_date and end_date:
            start = datetime.strptime(start_date, '%Y-%m-%d')
            end = datetime.strptime(end_date, '%Y-%m-%d')
            ticks = mt5.copy_ticks_range(symbol, start, end, mt5.COPY_TICKS_ALL)
        else:
            ticks = mt5.copy_ticks_from(symbol, datetime.now() - timedelta(days=1), count, mt5.COPY_TICKS_ALL)
        
        if ticks is None or len(ticks) == 0:
            error = mt5.last_error()
            print(f"❌ No ticks retrieved: {error}")
            return pd.DataFrame()
        
        # Convert to DataFrame
        df = pd.DataFrame(ticks)
        df['time'] = pd.to_datetime(df['time'], unit='s')
        df['time_msc'] = pd.to_datetime(df['time_msc'], unit='ms')
        
        # Rename for consistency
        df = df.rename(columns={
            'time_msc': 'timestamp',
            'bid': 'bid_price',
            'ask': 'ask_price',
            'last': 'last_price',
            'volume': 'tick_volume'
        })
        
        # Add metadata
        df['source'] = 'MT5'
        df['symbol'] = symbol
        
        # Select relevant columns
        df = df[['timestamp', 'bid_price', 'ask_price', 'last_price', 'tick_volume', 'symbol', 'source']]
        
        print(f"✅ MT5: Retrieved {len(df):,} ticks for {symbol}")
        print(f"   Period: {df['timestamp'].min()} to {df['timestamp'].max()}")
        
        return df
    
    def get_bars(self, symbol="EURUSD", timeframe=mt5.TIMEFRAME_M1, start_date=None, count=1000):
        """
        Get OHLCV bars from MT5.
        
        Args:
            symbol (str): Trading symbol
            timeframe: MT5 timeframe constant (e.g., mt5.TIMEFRAME_M1)
            start_date (str): Start date 'YYYY-MM-DD'
            count (int): Number of bars
        
        Returns:
            pd.DataFrame: OHLCV data
        """
        if not self.initialized:
            raise Exception("MT5 not connected. Call connect() first.")
        
        if start_date:
            start = datetime.strptime(start_date, '%Y-%m-%d')
            rates = mt5.copy_rates_from(symbol, timeframe, start, count)
        else:
            rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, count)
        
        if rates is None or len(rates) == 0:
            error = mt5.last_error()
            print(f"❌ No bars retrieved: {error}")
            return pd.DataFrame()
        
        df = pd.DataFrame(rates)
        df['time'] = pd.to_datetime(df['time'], unit='s')
        df = df.rename(columns={'time': 'timestamp'})
        df['source'] = 'MT5'
        df['symbol'] = symbol
        
        print(f"✅ MT5: Retrieved {len(df)} bars for {symbol}")
        
        return df
    
    def get_symbol_info(self, symbol="EURUSD"):
        """Get symbol specifications."""
        if not self.initialized:
            raise Exception("MT5 not connected")
        
        info = mt5.symbol_info(symbol)
        if info is None:
            return None
        
        return {
            'symbol': symbol,
            'point': info.point,
            'digits': info.digits,
            'spread': info.spread,
            'trade_contract_size': info.trade_contract_size,
            'trade_tick_size': info.trade_tick_size,
            'trade_tick_value': info.trade_tick_value
        }
    
    def disconnect(self):
        """Close MT5 connection."""
        if self.initialized:
            mt5.shutdown()
            self.initialized = False
            print("✅ MT5 disconnected")


# Example usage
if __name__ == "__main__":
    # Initialize collector
    collector = MT5DataCollector()
    
    # Connect (demo mode - no credentials needed for quotes)
    if collector.connect():
        
        # Get tick data
        ticks = collector.get_tick_data("EURUSD", count=5000)
        print(f"\nTick data shape: {ticks.shape}")
        print(ticks.head())
        
        # Get 1-minute bars
        bars = collector.get_bars("EURUSD", mt5.TIMEFRAME_M1, count=100)
        print(f"\nBars shape: {bars.shape}")
        print(bars.head())
        
        # Get symbol info
        info = collector.get_symbol_info("EURUSD")
        print(f"\nSymbol info: {info}")
        
        # Disconnect
        collector.disconnect()
