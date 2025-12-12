import sys
sys.path.insert(0, 'src')
from domains.market_dynamics import MarketHamiltonian, MarketState
import numpy as np

H = MarketHamiltonian(liquidity_mass=1.0, volatility=0.0, mean_reversion_strength=0.5, damping=0.5, equilibrium_price=100.0)
s = MarketState(price=110.0, momentum=0.0)
print('init', s.price, s.momentum)
for i in range(1, 11):
    q, p = s.price, s.momentum
    F = H.force(q)
    p_half = p + 0.5 * 0.01 * F
    noise = 0.0
    p_half_noisy = p_half + noise
    q_new = q + 0.01 * p_half_noisy / H.lambda_liq
    F_new = H.force(q_new)
    p_new = p_half_noisy + 0.5 * 0.01 * F_new
    gamma = H.damping
    p_new = p_new * (1.0 - gamma * 0.01)
    s = MarketState(price=q_new, momentum=p_new)
    print(i, 'q', q_new, 'p_half', p_half, 'p_new', p_new, 'F', F, 'F_new', F_new)
