import sys
sys.path.insert(0, 'src')
from compiler import define_system
import numpy as np

@define_system
class Independent:
    coordinates = ['x1','x2']
    def kinetic(self,p):
        return (p.px1**2 + p.px2**2)/2
    def potential(self,q):
        return 0.5*(q.x1**2 + q.x2**2)

@define_system
class Coupled:
    coordinates = ['x1','x2']
    def kinetic(self,p):
        return (p.px1**2 + p.px2**2)/2
    def potential(self,q):
        V_ind = 0.5 * (q.x1**2 + q.x2**2)
        V_coup = 0.5 * (q.x1 - q.x2)**2
        return V_ind + V_coup

ind = Independent()
coup = Coupled()

state = np.array([1.0,0.8,0.2,-0.1])
q = state[:2]
p = state[2:]

H_ind_full = ind.hamiltonian(q,p)
qA_full = np.zeros_like(q)
pA_full = np.zeros_like(p)
qB_full = np.zeros_like(q)
pB_full = np.zeros_like(p)
qA_full[0] = q[0]
pA_full[0] = p[0]
qB_full[1] = q[1]
pB_full[1] = p[1]
H_ind_A = ind.hamiltonian(qA_full, pA_full)
H_ind_B = ind.hamiltonian(qB_full, pB_full)

H_coup_full = coup.hamiltonian(q,p)
H_coup_A = coup.hamiltonian(qA_full, pA_full)
H_coup_B = coup.hamiltonian(qB_full, pB_full)

print('ind full', H_ind_full, 'A', H_ind_A, 'B', H_ind_B, 'sum', H_ind_A + H_ind_B)
print('coup full', H_coup_full, 'A', H_coup_A, 'B', H_coup_B, 'sum', H_coup_A + H_coup_B)
print('coup coupling energy', H_coup_full - (H_coup_A + H_coup_B))
