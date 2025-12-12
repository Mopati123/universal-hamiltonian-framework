import sys
sys.path.insert(0, 'src')
from compiler import define_system
from core import PhaseSpace
import numpy as np

@define_system
class Pendulum:
    coordinates = ['theta']
    def kinetic(self, p):
        return p.ptheta**2 / 2
    def potential(self, q):
        g, L = 9.8, 1.0
        return g * L * (1 - np.cos(q.theta))

system = Pendulum()
initial = PhaseSpace(q=np.array([0.1]), p=np.array([0.0]))
t, q_traj, p_traj = system.evolve(initial, t_max=10.0, dt=0.01)

crossings = []
for i in range(1, len(q_traj)):
    if q_traj[i-1, 0] * q_traj[i, 0] < 0:
        crossings.append(t[i])

print('len crossings', len(crossings))
print('crossings[:6]', crossings[:6])
if len(crossings) >= 2:
    print('crossings[1]-crossings[0]', crossings[1] - crossings[0])
    if len(crossings) >= 3:
        print('crossings[2]-crossings[0]', crossings[2] - crossings[0])
    print('expected T=', 2 * np.pi * np.sqrt(1.0 / 9.8))
