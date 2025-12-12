import sys
sys.path.insert(0, 'src')
from domains.market_dynamics import MarketHamiltonian, MarketState

def run_test():
    H1 = MarketHamiltonian(liquidity_mass=1.0, volatility=0.0, mean_reversion_strength=0.5, equilibrium_price=100.0)
    s = MarketState(price=110.0, momentum=0.0)
    for i in range(1, 501):
        s = H1.evolve_tick(s, dt=0.01)
        if i <= 20 or i % 100 == 0:
            print(i, s.price, s.momentum)
    print('final', s.price, s.momentum)

if __name__ == '__main__':
    run_test()
