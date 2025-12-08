"""
Multi-Source Market Data Collection Package

This package provides connectors to multiple trading platforms and data sources:
- MT5 (MetaTrader 5): Raw tick data
- Deriv: WebSocket tick streaming
- TradingView: Technical analysis indicators
- Alpaca: Real-time quotes and bars
- yfinance: Options chains and historical data

All data is unified into a consistent format for Hamiltonian analysis.
"""

__version__ = "1.0.0"
__author__ = "Universal Hamiltonian Framework"

from .mt5_connector import MT5DataCollector
from .deriv_connector import DerivDataCollector
from .tradingview_connector import TradingViewDataCollector
from .alpaca_connector import AlpacaDataCollector
from .unified_pipeline import UnifiedDataPipeline

__all__ = [
    'MT5DataCollector',
    'DerivDataCollector',
    'TradingViewDataCollector',
    'AlpacaDataCollector',
    'UnifiedDataPipeline'
]
