import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Simulated historical market data
np.random.seed(0)
dates = pd.date_range(start='2020-01-01', periods=1000)
stock_prices = pd.Series(np.random.normal(loc=0.001, scale=0.02, size=len(dates)).cumsum() + 100, index=dates)

# Traditional strategies
# Buy and Hold
buy_and_hold = stock_prices / stock_prices.iloc[0] - 1

# Momentum Strategy
momentum = stock_prices.pct_change(periods=20).shift(-20)

# Mean Reversion Strategy
mean_reversion = -stock_prices.pct_change(periods=20).shift(-20)

# Quantum Decision Layer (Placeholder)
quantum_decision_layer = (stock_prices.pct_change() > 0).astype(int)  # Placeholder for actual QDL logic

# Calculate performance metrics
performance_metrics = {}

strategies = {'Buy and Hold': buy_and_hold, 'Momentum': momentum, 'Mean Reversion': mean_reversion, 'Quantum Decision Layer': quantum_decision_layer}

for strategy_name, strategy in strategies.items():
    returns = strategy[1:]
    sharpe_ratio = np.mean(returns) / np.std(returns) * np.sqrt(252)
    max_drawdown = (returns.cumsum() - returns.cumsum().cummax()).min()
    win_rate = np.mean(returns > 0)
    performance_metrics[strategy_name] = {'Sharpe Ratio': sharpe_ratio, 'Max Drawdown': max_drawdown, 'Win Rate': win_rate}

# Display results
performance_df = pd.DataFrame(performance_metrics).T
print(performance_df)

# Visualization
performance_df[['Sharpe Ratio', 'Max Drawdown', 'Win Rate']].plot(kind='bar', subplots=True, figsize=(12, 8), title='Performance Metrics')
plt.tight_layout()
plt.show()