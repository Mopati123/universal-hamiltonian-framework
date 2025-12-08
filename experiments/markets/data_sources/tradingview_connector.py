"""
TradingView Data Collector

Collects technical analysis indicators and recommendations from TradingView.
Useful for combining price action with technical signals.
"""

from tradingview_ta import TA_Handler, Interval, Exchange
import pandas as pd
from datetime import datetime


class TradingViewDataCollector:
    """
    Collector for TradingView technical analysis data.
    
    Features:
    - Technical indicators (RSI, MACD, Moving Averages, etc.)
    - Buy/Sell/Neutral recommendations
    - Multiple timeframes
    - Multiple exchanges
    """
    
    def __init__(self):
        self.handler = None
        self.last_analysis = None
    
    def get_analysis(self, symbol="SPY", exchange="AMEX", screener="america", 
                     interval=Interval.INTERVAL_1_MINUTE):
        """
        Get comprehensive technical analysis.
        
        Args:
            symbol (str): Trading symbol
            exchange (str): Exchange name ("AMEX", "NYSE", "NASDAQ", etc.)
            screener (str): Market screener ("america", "forex", "crypto")
            interval: Time interval (use Interval.INTERVAL_*)
        
        Returns:
            dict: Analysis results with recommendations and indicators
        """
        try:
            self.handler = TA_Handler(
                symbol=symbol,
                exchange=exchange,
                screener=screener,
                interval=interval
            )
            
            analysis = self.handler.get_analysis()
            self.last_analysis = analysis
            
            result = {
                'timestamp': pd.Timestamp.now(),
                'symbol': symbol,
                'interval': interval,
                
                # Overall recommendation
                'recommendation': analysis.summary['RECOMMENDATION'],
                'buy_signals': analysis.summary['BUY'],
                'sell_signals': analysis.summary['SELL'],
                'neutral_signals': analysis.summary['NEUTRAL'],
                
                # Oscillators
                'oscillators_rec': analysis.oscillators['RECOMMENDATION'],
                'oscillators_buy': analysis.oscillators['BUY'],
                'oscillators_sell': analysis.oscillators['SELL'],
                
                # Moving Averages
                'ma_rec': analysis.moving_averages['RECOMMENDATION'],
                'ma_buy': analysis.moving_averages['BUY'],
                'ma_sell': analysis.moving_averages['SELL'],
                
                'source': 'TradingView'
            }
            
            print(f"✅ TradingView: {symbol} - {result['recommendation']}")
            print(f"   Buy: {result['buy_signals']}, Sell: {result['sell_signals']}, Neutral: {result['neutral_signals']}")
            
            return result
            
        except Exception as e:
            print(f"❌ TradingView Error: {e}")
            return None
    
    def get_indicators(self):
        """
        Get detailed indicator values.
        
        Returns:
            pd.DataFrame: All indicator values
        """
        if not self.last_analysis:
            raise Exception("Run get_analysis() first")
        
        indicators = self.last_analysis.indicators
        
        df = pd.DataFrame({
            'indicator': list(indicators.keys()),
            'value': list(indicators.values())
        })
        
        # Add timestamp
        df['timestamp'] = pd.Timestamp.now()
        df['source'] = 'TradingView'
        
        return df
    
    def get_key_indicators(self):
        """
        Get important indicators only.
        
        Returns:
            dict: Key indicator values (RSI, MACD, Moving Averages)
        """
        if not self.last_analysis:
            raise Exception("Run get_analysis() first")
        
        ind = self.last_analysis.indicators
        
        key_ind = {
            'timestamp': pd.Timestamp.now(),
            
            # Momentum
            'RSI': ind.get('RSI', None),
            'Stoch.K': ind.get('Stoch.K', None),
            'CCI': ind.get('CCI20', None),
            
            # Trend
            'MACD': ind.get('MACD.macd', None),
            'MACD_signal': ind.get('MACD.signal', None),
            'ADX': ind.get('ADX', None),
            
            # Moving Averages
            'SMA10': ind.get('SMA10', None),
            'SMA20': ind.get('SMA20', None),
            'SMA50': ind.get('SMA50', None),
            'SMA200': ind.get('SMA200', None),
            'EMA10': ind.get('EMA10', None),
            'EMA20': ind.get('EMA20', None),
            
            # Volatility
            'BB_upper': ind.get('BB.upper', None),
            'BB_lower': ind.get('BB.lower', None),
            
            'source': 'TradingView'
        }
        
        print(f"✅ TradingView: Key indicators retrieved")
        print(f"   RSI: {key_ind['RSI']:.2f}")
        print(f"   MACD: {key_ind['MACD']:.4f}")
        
        return key_ind
    
    def get_multi_timeframe_analysis(self, symbol="SPY", exchange="AMEX", screener="america"):
        """
        Get analysis across multiple timeframes.
        
        Returns:
            pd.DataFrame: Recommendations for different timeframes
        """
        timeframes = {
            '1m': Interval.INTERVAL_1_MINUTE,
            '5m': Interval.INTERVAL_5_MINUTES,
            '15m': Interval.INTERVAL_15_MINUTES,
            '1h': Interval.INTERVAL_1_HOUR,
            '4h': Interval.INTERVAL_4_HOURS,
            '1d': Interval.INTERVAL_1_DAY
        }
        
        results = []
        
        print(f"📊 TradingView: Multi-timeframe analysis for {symbol}...")
        
        for tf_name, tf_interval in timeframes.items():
            analysis = self.get_analysis(symbol, exchange, screener, tf_interval)
            if analysis:
                analysis['timeframe'] = tf_name
                results.append(analysis)
        
        df = pd.DataFrame(results)
        
        print(f"✅ TradingView: {len(df)} timeframes analyzed")
        
        return df


# Example usage
if __name__ == "__main__":
    collector = TradingViewDataCollector()
    
    # Get analysis for SPY
    print("\n=== SPY Analysis ===")
    analysis = collector.get_analysis("SPY", exchange="AMEX", interval=Interval.INTERVAL_5_MINUTES)
    print(analysis)
    
    # Get key indicators
    print("\n=== Key Indicators ===")
    key_ind = collector.get_key_indicators()
    for k, v in key_ind.items():
        if k not in ['timestamp', 'source']:
            print(f"{k}: {v}")
    
    # Get all indicators
    print("\n=== All Indicators ===")
    all_ind = collector.get_indicators()
    print(all_ind.head(10))
    
    # Multi-timeframe analysis
    print("\n=== Multi-Timeframe ===")
    mtf = collector.get_multi_timeframe_analysis("SPY")
    print(mtf[['timeframe', 'recommendation', 'buy_signals', 'sell_signals']])
