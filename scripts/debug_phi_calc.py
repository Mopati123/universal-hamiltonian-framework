import sys
sys.path.insert(0, 'src')
from compiler import define_system
from examples.demo_consciousness_phi import IntegratedInformationCalculator
import numpy as np

@define_system
class Independent:
    coordinates = ['x1', 'x2']
    def kinetic(self, p): return (p.px1**2 + p.px2**2) / 2
    def potential(self, q): return 0.5 * (q.x1**2 + q.x2**2)

@define_system
class Coupled:
    coordinates = ['x1', 'x2']
    def kinetic(self, p): return (p.px1**2 + p.px2**2) / 2
    def potential(self, q):
        V_ind = 0.5 * (q.x1**2 + q.x2**2)
        V_coup = 0.5 * (q.x1 - q.x2)**2
        return V_ind + V_coup

ind = Independent()
coup = Coupled()

state = np.array([1.0, 0.8, 0.2, -0.1])

calc_ind = IntegratedInformationCalculator(ind)
calc_coup = IntegratedInformationCalculator(coup)

phi_ind = calc_ind.compute_phi(state)
phi_coup = calc_coup.compute_phi(state)

print('phi_ind', phi_ind)
print('phi_coup', phi_coup)
print('difference', phi_coup - phi_ind)
