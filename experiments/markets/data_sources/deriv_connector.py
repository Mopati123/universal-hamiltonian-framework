"""
Deriv API Data Collector

Connects to Deriv.com WebSocket API for tick streaming and historical data.
Supports both real-time and historical tick data collection.
"""

import asyncio
import websockets
import json
import pandas as pd
from datetime import datetime
import time


class DerivDataCollector:
    """
    Collector for Deriv.com tick data via WebSocket API.
    
    Features:
    - Real-time tick streaming
    - Historical tick data
    - Multiple symbol support
    - Automatic reconnection
    """
    
    def __init__(self, app_id="1089"):
        """
        Initialize Deriv collector.
        
        Args:
            app_id (str): Deriv API app ID (default is public demo)
        """
        self.app_id = app_id
        self.ws_url = f"wss://ws.binaryws.com/websockets/v3?app_id={app_id}"
        self.tick_data = []
        self.is_streaming = False
    
    async def get_tick_stream(self, symbol="R_100", duration=3600, callback=None):
        """
        Stream real-time tick data.
        
        Args:
            symbol (str): Symbol to stream (e.g., "R_100", "frxEURUSD")
            duration (int): Streaming duration in seconds
            callback (callable): Optional callback for each tick
        
        Returns:
            pd.DataFrame: Collected ticks
        """
        async with websockets.connect(self.ws_url) as websocket:
            # Subscribe to tick stream
            subscribe_msg = {
                "ticks": symbol,
                "subscribe": 1
            }
            await websocket.send(json.dumps(subscribe_msg))
            
            print(f"📡 Deriv: Streaming {symbol} ticks for {duration}s...")
            
            start_time = time.time()
            self.is_streaming = True
            tick_count = 0
            
            while (time.time() - start_time) < duration and self.is_streaming:
                try:
                    response = await asyncio.wait_for(websocket.recv(), timeout=10)
                    data = json.loads(response)
                    
                    if 'tick' in data:
                        tick = data['tick']
                        
                        tick_record = {
                            'timestamp': pd.to_datetime(tick['epoch'], unit='s'),
                            'last_price': float(tick['quote']),
                            'symbol': tick['symbol'],
                            'source': 'Deriv'
                        }
                        
                        self.tick_data.append(tick_record)
                        tick_count += 1
                        
                        if callback:
                            callback(tick_record)
                        
                        if tick_count % 100 == 0:
                            print(f"   📊 {tick_count} ticks received...")
                
                except asyncio.TimeoutError:
                    print("   ⚠️  Tick timeout, continuing...")
                    continue
                except Exception as e:
                    print(f"   ❌ Error: {e}")
                    break
            
            # Unsubscribe
            forget_msg = {"forget_all": "ticks"}
            await websocket.send(json.dumps(forget_msg))
            
            print(f"✅ Deriv: Streaming complete. {tick_count} ticks collected.")
            
            return self.to_dataframe()
    
    def get_historical_ticks(self, symbol="R_100", count=5000, end="latest"):
        """
        Get historical tick data.
        
        Args:
            symbol (str): Symbol name
            count (int): Number of ticks to retrieve
            end (str): End point ('latest' or Unix timestamp)
        
        Returns:
            pd.DataFrame: Historical ticks
        """
        async def fetch_history():
            async with websockets.connect(self.ws_url) as websocket:
                request = {
                    "ticks_history": symbol,
                    "count": count,
                    "end": end,
                    "style": "ticks"
                }
                
                print(f"📥 Deriv: Fetching {count} historical ticks for {symbol}...")
                
                await websocket.send(json.dumps(request))
                response = await websocket.recv()
                data = json.loads(response)
                
                if 'error' in data:
                    print(f"❌ Deriv Error: {data['error']['message']}")
                    return pd.DataFrame()
                
                if 'history' in data:
                    history = data['history']
                    
                    df = pd.DataFrame({
                        'timestamp': pd.to_datetime(history['times'], unit='s'),
                        'last_price': history['prices']
                    })
                    df['symbol'] = symbol
                    df['source'] = 'Deriv'
                    
                    print(f"✅ Deriv: Retrieved {len(df):,} historical ticks")
                    print(f"   Period: {df['timestamp'].min()} to {df['timestamp'].max()}")
                    
                    return df
                
                return pd.DataFrame()
        
        return asyncio.run(fetch_history())
    
    def get_candles(self, symbol="R_100", interval=60, count=1000):
        """
        Get OHLC candles.
        
        Args:
            symbol (str): Symbol name
            interval (int): Candle interval in seconds (60, 300, 3600, etc.)
            count (int): Number of candles
        
        Returns:
            pd.DataFrame: OHLC data
        """
        async def fetch_candles():
            async with websockets.connect(self.ws_url) as websocket:
                request = {
                    "ticks_history": symbol,
                    "adjust_start_time": 1,
                    "count": count,
                    "end": "latest",
                    "start": 1,
                    "style": "candles",
                    "granularity": interval
                }
                
                print(f"📥 Deriv: Fetching {count} candles ({interval}s) for {symbol}...")
                
                await websocket.send(json.dumps(request))
                response = await websocket.recv()
                data = json.loads(response)
                
                if 'candles' in data:
                    candles = data['candles']
                    
                    df = pd.DataFrame(candles)
                    df['epoch'] = pd.to_datetime(df['epoch'], unit='s')
                    df = df.rename(columns={
                        'epoch': 'timestamp',
                        'open': 'open',
                        'high': 'high',
                        'low': 'low',
                        'close': 'close'
                    })
                    df['symbol'] = symbol
                    df['source'] = 'Deriv'
                    
                    print(f"✅ Deriv: Retrieved {len(df)} candles")
                    
                    return df
                
                return pd.DataFrame()
        
        return asyncio.run(fetch_candles())
    
    def stop_streaming(self):
        """Stop active tick stream."""
        self.is_streaming = False
        print("🛑 Deriv: Stopping stream...")
    
    def to_dataframe(self):
        """Convert collected ticks to DataFrame."""
        if not self.tick_data:
            return pd.DataFrame()
        
        return pd.DataFrame(self.tick_data)
    
    def clear_data(self):
        """Clear collected tick data."""
        self.tick_data = []


# Example usage
if __name__ == "__main__":
    # Initialize collector
    collector = DerivDataCollector(app_id="1089")  # Public demo app_id
    
    # Get historical ticks
    print("\n=== Historical Ticks ===")
    historical_ticks = collector.get_historical_ticks("R_100", count=1000)
    print(historical_ticks.head())
    print(f"Shape: {historical_ticks.shape}")
    
    # Get candles
    print("\n=== Candles ===")
    candles = collector.get_candles("R_100", interval=60, count=100)
    print(candles.head())
    
    # Stream ticks for 10 seconds
    print("\n=== Live Stream (10s) ===")
    live_ticks = asyncio.run(collector.get_tick_stream("R_100", duration=10))
    print(live_ticks.head())
    print(f"Live ticks collected: {len(live_ticks)}")
