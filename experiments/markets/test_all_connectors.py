"""
Test All Data Connectors

This script tests connectivity to all data sources and reports which ones are working.
Run this after completing API setup to verify everything is configured correctly.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from experiments.markets.data_sources import (
    MT5DataCollector,
    DerivDataCollector,
    TradingViewDataCollector,
    AlpacaDataCollector,
    UnifiedDataPipeline
)
import pandas as pd


def test_mt5():
    """Test MT5 connection"""
    print("\n" + "="*70)
    print("Testing MT5 (MetaTrader 5)")
    print("="*70)
    
    try:
        collector = MT5DataCollector()
        
        # Try to connect (works without credentials for quotes)
        if collector.connect():
            print("✅ MT5 connection successful")
            
            # Try to get some data
            ticks = collector.get_tick_data("EURUSD", count=10)
            
            if not ticks.empty:
                print(f"✅ MT5 tick data retrieval successful ({len(ticks)} ticks)")
                print(f"   Sample: {ticks.head(2)}")
                collector.disconnect()
                return True
            else:
                print("⚠️  MT5 connected but no data retrieved")
                collector.disconnect()
                return False
        else:
            print("❌ MT5 connection failed")
            return False
            
    except Exception as e:
        print(f"❌ MT5 Error: {e}")
        return False


def test_deriv():
    """Test Deriv connection"""
    print("\n" + "="*70)
    print("Testing Deriv API")
    print("="*70)
    
    try:
        # Use demo app_id
        collector = DerivDataCollector(app_id="1089")
        
        # Try to get historical data
        data = collector.get_historical_ticks("R_100", count=10)
        
        if not data.empty:
            print(f"✅ Deriv connection successful ({len(data)} ticks)")
            print(f"   Sample: {data.head(2)}")
            return True
        else:
            print("⚠️  Deriv connected but no data retrieved")
            return False
            
    except Exception as e:
        print(f"❌ Deriv Error: {e}")
        return False


def test_tradingview():
    """Test TradingView connection"""
    print("\n" + "="*70)
    print("Testing TradingView")
    print("="*70)
    
    try:
        collector = TradingViewDataCollector()
        
        # Get analysis for SPY
        analysis = collector.get_analysis("SPY")
        
        if analysis:
            print(f"✅ TradingView connection successful")
            print(f"   Recommendation: {analysis['recommendation']}")
            print(f"   Buy signals: {analysis['buy_signals']}")
            return True
        else:
            print("❌ TradingView returned no data")
            return False
            
    except Exception as e:
        print(f"❌ TradingView Error: {e}")
        return False


def test_alpaca():
    """Test Alpaca connection"""
    print("\n" + "="*70)
    print("Testing Alpaca")
    print("="*70)
    
    try:
        # Will use free tier (no auth)
        collector = AlpacaDataCollector()
        
        # Try to get some bars
        bars = collector.get_bars("SPY", limit=10)
        
        if not bars.empty:
            print(f"✅ Alpaca connection successful ({len(bars)} bars)")
            print(f"   Sample: {bars.head(2)}")
            return True
        else:
            print("⚠️  Alpaca connected but no data retrieved")
            return False
            
    except Exception as e:
        print(f"❌ Alpaca Error: {e}")
        print("   Note: If authentication failed, Alpaca may require API keys")
        return False


def test_unified_pipeline():
    """Test unified pipeline"""
    print("\n" + "="*70)
    print("Testing Unified Pipeline")
    print("="*70)
    
    try:
        # Create sample data
        timestamps = pd.date_range('2024-12-08 09:30:00', periods=100, freq='1S')
        
        data1 = pd.DataFrame({
            'timestamp': timestamps,
            'last_price': 450.0 + pd.np.random.randn(len(timestamps)) * 0.1
        })
        
        data2 = pd.DataFrame({
            'timestamp': timestamps,
            'last_price': 450.0 + pd.np.random.randn(len(timestamps)) * 0.1
        })
        
        # Create pipeline
        pipeline = UnifiedDataPipeline()
        pipeline.add_source_data('Source1', data1)
        pipeline.add_source_data('Source2', data2)
        
        # Process
        unified = pipeline.create_unified_dataset()
        phase_space = pipeline.calculate_phase_space_variables()
        
        if len(phase_space) > 0:
            print(f"✅ Unified pipeline successful")
            print(f"   Unified records: {len(phase_space)}")
            return True
        else:
            print("❌ Pipeline produced no data")
            return False
            
    except Exception as e:
        print(f"❌ Pipeline Error: {e}")
        return False


def main():
    """Run all tests"""
    print("\n" + "="*70)
    print("MULTI-SOURCE DATA CONNECTOR TEST SUITE")
    print("="*70)
    print("\nTesting all data source connections...")
    print("This will verify your API setup is working correctly.")
    
    results = {}
    
    # Run tests
    results['MT5'] = test_mt5()
    results['Deriv'] = test_deriv()
    results['TradingView'] = test_tradingview()
    results['Alpaca'] = test_alpaca()
    results['UnifiedPipeline'] = test_unified_pipeline()
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    
    passed = sum(results.values())
    total = len(results)
    
    for name, status in results.items():
        status_str = "✅ PASS" if status else "❌ FAIL"
        print(f"{name:20s}: {status_str}")
    
    print("\n" + "-"*70)
    print(f"Total: {passed}/{total} tests passed ({passed/total*100:.0f}%)")
    print("="*70)
    
    if passed == total:
        print("\n🎉 All tests passed! Your setup is complete.")
        print("You can now proceed to data collection.")
    elif passed > 0:
        print("\n⚠️  Some tests passed. You can proceed with working connectors.")
        print("Check API_SETUP.md for help with failed connectors.")
    else:
        print("\n❌ All tests failed. Please check API_SETUP.md for setup instructions.")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
