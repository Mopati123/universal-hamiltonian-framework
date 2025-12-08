"""
Alpaca API Data Collector

Connects to Alpaca Markets API for real-time quotes, bars, and trade data.
Supports both paper trading and live market data.
"""

from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest, StockQuotesRequest, StockTradesRequest
from alpaca.data.timeframe import TimeFrame, TimeFrameUnit
from datetime import datetime, timedelta
import pandas as pd


class AlpacaDataCollector:
    """
    Collector for Alpaca Markets data.
    
    Features:
    - Real-time quotes (bid/ask)
    - Historical bars (OHLCV)
    - Trade data
    - Multiple symbols
    """
    
    def __init__(self, api_key=None, api_secret=None):
        """
        Initialize Alpaca collector.
        
        Args:
            api_key (str): Alpaca API key
            api_secret (str): Alpaca API secret
        """
        if api_key and api_secret:
            self.client = StockHistoricalDataClient(api_key, api_secret)
            self.authenticated = True
            print("✅ Alpaca: Authenticated with API key")
        else:
            # Use free tier without authentication
            self.client = StockHistoricalDataClient()
            self.authenticated = False
            print("✅ Alpaca: Using free tier data")
    
    def get_bars(self, symbol="SPY", timeframe="1Min", start=None, end=None, limit=10000):
        """
        Get OHLCV bars.
        
        Args:
            symbol (str): Stock symbol
            timeframe (str): Bar size ("1Min", "5Min", "1Hour", "1Day")
            start (str): Start datetime 'YYYY-MM-DD HH:MM:SS'
            end (str): End datetime
            limit (int): Max bars to retrieve
        
        Returns:
            pd.DataFrame: OHLCV data
        """
        # Parse timeframe
        tf_map = {
            "1Min": TimeFrame(1, TimeFrameUnit.Minute),
            "5Min": TimeFrame(5, TimeFrameUnit.Minute),
            "15Min": TimeFrame(15, TimeFrameUnit.Minute),
            "1Hour": TimeFrame(1, TimeFrameUnit.Hour),
            "1Day": TimeFrame(1, TimeFrameUnit.Day)
        }
        
        tf = tf_map.get(timeframe, TimeFrame(1, TimeFrameUnit.Minute))
        
        # Parse dates
        if start:
            start_dt = pd.to_datetime(start)
        else:
            start_dt = datetime.now() - timedelta(days=1)
        
        if end:
            end_dt = pd.to_datetime(end)
        else:
            end_dt = datetime.now()
        
        # Create request
        request = StockBarsRequest(
            symbol_or_symbols=symbol,
            timeframe=tf,
            start=start_dt,
            end=end_dt,
            limit=limit
        )
        
        print(f"📥 Alpaca: Fetching {timeframe} bars for {symbol}...")
        
        try:
            # Get bars
            bars = self.client.get_stock_bars(request)
            
            # Convert to DataFrame
            df = bars.df
            
            if isinstance(df.index, pd.MultiIndex):
                # Reset multi-index if present
                df = df.reset_index()
            
            # Standardize columns
            if 'timestamp' not in df.columns and 'symbol' in df.columns:
                df = df.reset_index()
            
            df = df.rename(columns={
                'open': 'open',
                'high': 'high',
                'low': 'low',
                'close': 'close',
                'volume': 'volume',
                'trade_count': 'trade_count',
                'vwap': 'vwap'
            })
            
            df['source'] = 'Alpaca'
            df['symbol'] = symbol
            
            print(f"✅ Alpaca: Retrieved {len(df):,} bars")
            print(f"   Period: {df['timestamp'].min()} to {df['timestamp'].max()}")
            
            return df
            
        except Exception as e:
            print(f"❌ Alpaca Error: {e}")
            return pd.DataFrame()
    
    def get_quotes(self, symbol="SPY", start=None, end=None, limit=10000):
        """
        Get bid/ask quotes.
        
        Args:
            symbol (str): Stock symbol
            start (str): Start datetime
            end (str): End datetime
            limit (int): Max quotes
        
        Returns:
            pd.DataFrame: Quote data with bid/ask prices and sizes
        """
        if start:
            start_dt = pd.to_datetime(start)
        else:
            start_dt = datetime.now() - timedelta(hours=1)
        
        if end:
            end_dt = pd.to_datetime(end)
        else:
            end_dt = datetime.now()
        
        request = StockQuotesRequest(
            symbol_or_symbols=symbol,
            start=start_dt,
            end=end_dt,
            limit=limit
        )
        
        print(f"📥 Alpaca: Fetching quotes for {symbol}...")
        
        try:
            quotes = self.client.get_stock_quotes(request)
            df = quotes.df
            
            if isinstance(df.index, pd.MultiIndex):
                df = df.reset_index()
            
            df = df.rename(columns={
                'ask_price': 'ask_price',
                'bid_price': 'bid_price',
                'ask_size': 'ask_size',
                'bid_size': 'bid_size'
            })
            
            df['source'] = 'Alpaca'
            df['symbol'] = symbol
            df['spread'] = df['ask_price'] - df['bid_price']
            
            print(f"✅ Alpaca: Retrieved {len(df):,} quotes")
            print(f"   Avg spread: ${df['spread'].mean():.4f}")
            
            return df
            
        except Exception as e:
            print(f"❌ Alpaca Error: {e}")
            return pd.DataFrame()
    
    def get_trades(self, symbol="SPY", start=None, end=None, limit=10000):
        """
        Get individual trades.
        
        Args:
            symbol (str): Stock symbol
            start (str): Start datetime
            end (str): End datetime
            limit (int): Max trades
        
        Returns:
            pd.DataFrame: Trade data with price and size
        """
        if start:
            start_dt = pd.to_datetime(start)
        else:
            start_dt = datetime.now() - timedelta(minutes=30)
        
        if end:
            end_dt = pd.to_datetime(end)
        else:
            end_dt = datetime.now()
        
        request = StockTradesRequest(
            symbol_or_symbols=symbol,
            start=start_dt,
            end=end_dt,
            limit=limit
        )
        
        print(f"📥 Alpaca: Fetching trades for {symbol}...")
        
        try:
            trades = self.client.get_stock_trades(request)
            df = trades.df
            
            if isinstance(df.index, pd.MultiIndex):
                df = df.reset_index()
            
            df = df.rename(columns={
                'price': 'last_price',
                'size': 'volume'
            })
            
            df['source'] = 'Alpaca'
            df['symbol'] = symbol
            
            print(f"✅ Alpaca: Retrieved {len(df):,} trades")
            print(f"   Total volume: {df['volume'].sum():,}")
            
            return df
            
        except Exception as e:
            print(f"❌ Alpaca Error: {e}")
            return pd.DataFrame()
    
    def get_latest_quote(self, symbol="SPY"):
        """
        Get most recent quote (real-time if authenticated).
        
        Returns:
            dict: Latest bid/ask quote
        """
        try:
            # Get very recent quotes
            quotes = self.get_quotes(symbol, limit=1)
            
            if not quotes.empty:
                latest = quotes.iloc[-1]
                
                result = {
                    'timestamp': latest['timestamp'],
                    'symbol': symbol,
                    'bid_price': latest['bid_price'],
                    'ask_price': latest['ask_price'],
                    'bid_size': latest['bid_size'],
                    'ask_size': latest['ask_size'],
                    'spread': latest['spread'],
                    'source': 'Alpaca'
                }
                
                print(f"✅ Alpaca: Latest quote - Bid: ${result['bid_price']:.2f}, Ask: ${result['ask_price']:.2f}")
                
                return result
            
            return None
            
        except Exception as e:
            print(f"❌ Alpaca Error: {e}")
            return None


# Example usage
if __name__ == "__main__":
    # Initialize collector (free tier - no keys needed)
    collector = AlpacaDataCollector()
    
    # Get 1-minute bars
    print("\n=== 1-Minute Bars ===")
    bars = collector.get_bars("SPY", timeframe="1Min", limit=100)
    print(bars.head())
    print(f"Shape: {bars.shape}")
    
    # Get quotes (bid/ask)
    print("\n=== Quotes ===")
    quotes = collector.get_quotes("SPY", limit=100)
    print(quotes.head())
    
    # Get trades
    print("\n=== Trades ===")
    trades = collector.get_trades("SPY", limit=100)
    print(trades.head())
    
    # Get latest quote
    print("\n=== Latest Quote ===")
    latest = collector.get_latest_quote("SPY")
    print(latest)
