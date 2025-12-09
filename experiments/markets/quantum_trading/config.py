"""
Configuration Loader

Loads API credentials and settings from environment variables.
Ensures secure credential management for live trading.
"""

import os
from pathlib import Path
from typing import Dict, List
from dotenv import load_dotenv


class TradingConfig:
    """
    Configuration manager for quantum trading system.
    
    Loads credentials from .env file (never committed to Git).
    """
    
    def __init__(self, env_file: str = None):
        """
        Load configuration from .env file
        
        Args:
            env_file: Path to .env file (default: .env in markets directory)
        """
        if env_file is None:
            # Look for .env in markets directory
            markets_dir = Path(__file__).parent.parent
            env_file = markets_dir / '.env'
        
        # Load environment variables
        if os.path.exists(env_file):
            load_dotenv(env_file)
            print(f"✅ Loaded configuration from: {env_file}")
        else:
            print(f"⚠️  No .env file found at: {env_file}")
            print(f"   Using environment variables or defaults.")
            print(f"   For live trading, copy .env.template to .env and fill in credentials.")
    
    # -------------------------------------------------------------------------
    # MT5 Credentials
    # -------------------------------------------------------------------------
    
    @property
    def mt5_account(self) -> int:
        """MT5 account number"""
        return int(os.getenv('MT5_ACCOUNT', '0'))
    
    @property
    def mt5_password(self) -> str:
        """MT5 password"""
        return os.getenv('MT5_PASSWORD', '')
    
    @property
    def mt5_server(self) -> str:
        """MT5 server name"""
        return os.getenv('MT5_SERVER', 'MetaQuotes-Demo')
    
    @property
    def mt5_terminal_path(self) -> str:
        """Path to MT5 terminal executable"""
        return os.getenv('MT5_TERMINAL_PATH', 'C:/Program Files/MetaTrader 5/terminal64.exe')
    
    # -------------------------------------------------------------------------
    # Deriv Credentials
    # -------------------------------------------------------------------------
    
    @property
    def deriv_app_id(self) -> str:
        """Deriv app ID"""
        return os.getenv('DERIV_APP_ID', '1089')  # Default to demo app
    
    @property
    def deriv_api_token(self) -> str:
        """Deriv API token"""
        return os.getenv('DERIV_API_TOKEN', '')
    
    # -------------------------------------------------------------------------
    # Alpaca Credentials
    # -------------------------------------------------------------------------
    
    @property
    def alpaca_api_key(self) -> str:
        """Alpaca API key"""
        return os.getenv('ALPACA_API_KEY', '')
    
    @property
    def alpaca_api_secret(self) -> str:
        """Alpaca API secret"""
        return os.getenv('ALPACA_API_SECRET', '')
    
    @property
    def alpaca_base_url(self) -> str:
        """Alpaca base URL (paper or live)"""
        return os.getenv('ALPACA_BASE_URL', 'https://paper-api.alpaca.markets')
    
    # -------------------------------------------------------------------------
    # Trading System Configuration
    # -------------------------------------------------------------------------
    
    @property
    def trading_mode(self) -> str:
        """Trading mode: 'simulation' or 'live'"""
        mode = os.getenv('TRADING_MODE', 'simulation').lower()
        
        # Safety check for live trading
        if mode == 'live':
            require_confirmation = os.getenv('REQUIRE_EXPLICIT_LIVE_CONFIRMATION', 'true').lower() == 'true'
            
            if require_confirmation:
                print("\n" + "="*70)
                print("⚠️  WARNING: LIVE TRADING MODE ENABLED")
                print("="*70)
                print("This will trade with REAL MONEY!")
                print("Make sure:")
                print("  1. You've tested in simulation mode first")
                print("  2. Your API credentials are correct")
                print("  3. Risk limits are properly configured")
                print("  4. You understand the risks involved")
                print()
                
                confirmation = input("Type 'YES I UNDERSTAND' to proceed: ")
                
                if confirmation != 'YES I UNDERSTAND':
                    print("\n❌ Live trading not confirmed. Switching to simulation mode.")
                    return 'simulation'
                
                print("\n✅ Live trading confirmed. Starting...\n")
        
        return mode
    
    @property
    def trading_capital(self) -> float:
        """Total capital to trade"""
        return float(os.getenv('TRADING_CAPITAL', '10000.0'))
    
    @property
    def trading_universe(self) -> List[str]:
        """List of symbols to trade"""
        universe_str = os.getenv('TRADING_UNIVERSE', 'SPY')
        return [s.strip() for s in universe_str.split(',')]
    
    # -------------------------------------------------------------------------
    # Risk Limits
    # -------------------------------------------------------------------------
    
    @property
    def max_position_size(self) -> float:
        """Maximum position size per symbol"""
        return float(os.getenv('MAX_POSITION_SIZE', '5000.0'))
    
    @property
    def max_positions(self) -> int:
        """Maximum number of positions"""
        return int(os.getenv('MAX_POSITIONS', '5'))
    
    @property
    def max_drawdown(self) -> float:
        """Maximum drawdown (as fraction)"""
        return float(os.getenv('MAX_DRAWDOWN', '0.15'))
    
    @property
    def max_leverage(self) -> float:
        """Maximum leverage"""
        return float(os.getenv('MAX_LEVERAGE', '2.0'))
    
    # -------------------------------------------------------------------------
    # Execution Parameters
    # -------------------------------------------------------------------------
    
    @property
    def order_type(self) -> str:
        """Order type: 'market' or 'limit'"""
        return os.getenv('ORDER_TYPE', 'market')
    
    @property
    def time_in_force(self) -> str:
        """Time in force: 'day', 'gtc', 'ioc', 'fok'"""
        return os.getenv('TIME_IN_FORCE', 'day')
    
    # -------------------------------------------------------------------------
    # Safety Settings
    # -------------------------------------------------------------------------
    
    @property
    def dry_run(self) -> bool:
        """Dry run mode (simulate orders without executing)"""
        return os.getenv('DRY_RUN', 'false').lower() == 'true'
    
    @property
    def log_level(self) -> str:
        """Log level"""
        return os.getenv('LOG_LEVEL', 'INFO')
    
    # -------------------------------------------------------------------------
    # Data Source Configuration
    # -------------------------------------------------------------------------
    
    @property
    def enabled_data_sources(self) -> List[str]:
        """Which data sources to use"""
        sources_str = os.getenv('ENABLED_DATA_SOURCES', 'Alpaca,yfinance')
        return [s.strip() for s in sources_str.split(',')]
    
    @property
    def primary_execution_source(self) -> str:
        """Primary source for order execution"""
        return os.getenv('PRIMARY_EXECUTION_SOURCE', 'Alpaca')
    
    # -------------------------------------------------------------------------
    # Advanced Parameters
    # -------------------------------------------------------------------------
    
    @property
    def hamiltonian_params(self) -> Dict[str, float]:
        """Hamiltonian parameters"""
        return {
            'mean_reversion': float(os.getenv('HAMILTONIAN_MEAN_REVERSION', '0.1')),
            'equilibrium': float(os.getenv('HAMILTONIAN_EQUILIBRIUM', '450.0')),
            'drift': float(os.getenv('HAMILTONIAN_DRIFT', '0.0')),
            'friction': float(os.getenv('HAMILTONIAN_FRICTION', '0.01'))
        }
    
    @property
    def qubo_params(self) -> Dict:
        """QUBO optimizer parameters"""
        return {
            'method': os.getenv('QUBO_METHOD', 'simulated_annealing'),
            'max_iterations': int(os.getenv('QUBO_MAX_ITERATIONS', '1000')),
            'temperature_init': float(os.getenv('QUBO_TEMPERATURE_INIT', '10.0')),
            'temperature_final': float(os.getenv('QUBO_TEMPERATURE_FINAL', '0.01'))
        }
    
    @property
    def vqe_params(self) -> Dict:
        """VQE parameters"""
        return {
            'max_iterations': int(os.getenv('VQE_MAX_ITERATIONS', '100')),
            'tolerance': float(os.getenv('VQE_TOLERANCE', '1e-6'))
        }
    
    # -------------------------------------------------------------------------
    # Validation
    # -------------------------------------------------------------------------
    
    def validate(self) -> bool:
        """
        Validate configuration
        
        Returns:
            True if valid, raises exception otherwise
        """
        errors = []
        
        # Check mode
        if self.trading_mode not in ['simulation', 'live']:
            errors.append(f"Invalid trading mode: {self.trading_mode}")
        
        # Check live trading credentials
        if self.trading_mode == 'live':
            if self.primary_execution_source == 'Alpaca':
                if not self.alpaca_api_key or not self.alpaca_api_secret:
                    errors.append("Alpaca credentials missing for live trading")
            
            elif self.primary_execution_source == 'MT5':
                if not self.mt5_account or not self.mt5_password:
                    errors.append("MT5 credentials missing for live trading")
            
            elif self.primary_execution_source == 'Deriv':
                if not self.deriv_app_id or not self.deriv_api_token:
                    errors.append("Deriv credentials missing for live trading")
        
        # Check capital
        if self.trading_capital <= 0:
            errors.append(f"Invalid capital: {self.trading_capital}")
        
        # Check universe
        if not self.trading_universe:
            errors.append("Trading universe is empty")
        
        # Report errors
        if errors:
            print("\n❌ Configuration Errors:")
            for error in errors:
                print(f"   - {error}")
            raise ValueError("Invalid configuration. Fix errors above.")
        
        print("✅ Configuration validated")
        return True
    
    def print_summary(self):
        """Print configuration summary"""
        print("\n" + "="*70)
        print("TRADING SYSTEM CONFIGURATION")
        print("="*70)
        print(f"Mode: {self.trading_mode.upper()}")
        print(f"Capital: ${self.trading_capital:,.2f}")
        print(f"Universe: {', '.join(self.trading_universe)}")
        print(f"Max Positions: {self.max_positions}")
        print(f"Max Position Size: ${self.max_position_size:,.2f}")
        print(f"Max Drawdown: {self.max_drawdown*100:.1f}%")
        print(f"Primary Execution: {self.primary_execution_source}")
        print(f"Data Sources: {', '.join(self.enabled_data_sources)}")
        
        if self.trading_mode == 'live':
            print("\n⚠️  LIVE TRADING ENABLED - REAL MONEY AT RISK!")
        
        if self.dry_run:
            print("\n🔍 DRY RUN MODE - Orders will be simulated, not executed")
        
        print("="*70 + "\n")


# Global config instance
config = None

def get_config(env_file: str = None) -> TradingConfig:
    """Get configuration instance (singleton)"""
    global config
    if config is None:
        config = TradingConfig(env_file)
    return config


# Example usage
if __name__ == "__main__":
    print("Testing configuration loader...\n")
    
    cfg = get_config()
    cfg.print_summary()
    
    try:
        cfg.validate()
        print("\n✅ Configuration is valid!")
    except ValueError as e:
        print(f"\n❌ Configuration error: {e}")
