import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class BacktestingFramework:
    def __init__(self, tickers, start_date, end_date):
        self.tickers = tickers
        self.start_date = start_date
        self.end_date = end_date
        self.data = self.load_data()

    def load_data(self):
        data = yf.download(self.tickers, start=self.start_date, end=self.end_date)
        return data['Adj Close']

    def calculate_returns(self):
        returns = self.data.pct_change().dropna()
        return returns

    def backtest_strategy(self, strategy_function):
        returns = self.calculate_returns()
        strategy_returns = strategy_function(returns)
        cumulative_returns = (1 + strategy_returns).cumprod() - 1
        performance = self.calculate_performance(strategy_returns)
        return cumulative_returns, performance

    def calculate_performance(self, strategy_returns):
        total_return = strategy_returns.sum()
        annualized_return = total_return * 252 / len(strategy_returns)
        max_drawdown = self.calculate_drawdown(strategy_returns)
        return {
            'Total Return': total_return,
            'Annualized Return': annualized_return,
            'Max Drawdown': max_drawdown,
        }

    def calculate_drawdown(self, returns):
        cumulative_returns = (1 + returns).cumprod()
        peak = cumulative_returns.cummax()
        drawdown = (cumulative_returns - peak) / peak
        max_drawdown = drawdown.min()
        return max_drawdown

    def plot_results(self, cumulative_returns):
        plt.figure(figsize=(14, 7))
        plt.plot(cumulative_returns, label='Strategy Cumulative Returns')
        plt.title('Backtest Results')
        plt.xlabel('Date')
        plt.ylabel('Cumulative Returns')
        plt.legend()
        plt.grid(True)
        plt.show()

# Example Strategy

def quantum_decision_layer(returns):
    # This is a placeholder for the actual Quantum Decision Layer strategy
    return returns['AAPL'] * 0.01  # Example strategy

if __name__ == '__main__':
    tickers = ['AAPL', 'MSFT', 'GOOGL']
    start_date = '2020-01-01'
    end_date = '2023-01-01'
    backtest = BacktestingFramework(tickers, start_date, end_date)
    cumulative_returns, performance = backtest.backtest_strategy(quantum_decision_layer)
    print(performance)
    backtest.plot_results(cumulative_returns)
