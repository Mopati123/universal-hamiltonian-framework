"""
Symbolic Engine - SymPy-based Mathematics

Automatic differentiation, Poisson brackets, conservation laws.
Code generation for Mojo/Cython backends.
"""

import sympy as sp
from sympy import symbols, diff, simplify, lambdify, Matrix
from typing import List, Tuple, Dict, Callable
import numpy as np


class SymbolicHamiltonian:
    """
    Symbolic representation of Hamiltonian system.
    
    Handles:
    - Automatic differentiation
    - Poisson brackets
    - Canonical transformations
    - Conservation law detection (Noether's theorem)
    """
    
    def __init__(self, n_dof: int):
        self.n_dof = n_dof
        
        # Create symbolic variables
        self.q = sp.symbols(f'q0:{n_dof}', real=True)
        self.p = sp.symbols(f'p0:{n_dof}', real=True)
        self.t = sp.Symbol('t', real=True)
        
        # Hamiltonian expression (to be defined)
        self.H = None
        
        # Cached expressions
        self._dH_dq = None
        self._dH_dp = None
    
    def set_hamiltonian(self, H_expr: sp.Expr):
        """Define the Hamiltonian expression"""
        self.H = H_expr
        self._dH_dq = None  # Clear cache
        self._dH_dp = None
    
    def hamilton_equations(self) -> Tuple[List[sp.Expr], List[sp.Expr]]:
        """
        Derive Hamilton's equations symbolically.
        
        Returns:
            (dq/dt, dp/dt)
        """
        if self.H is None:
            raise ValueError("Hamiltonian not defined")
        
        # dq/dt = ∂H/∂p
        if self._dH_dp is None:
            self._dH_dp = [diff(self.H, p_i) for p_i in self.p]
        
        # dp/dt = -∂H/∂q
        if self._dH_dq is None:
            self._dH_dq = [-diff(self.H, q_i) for q_i in self.q]
        
        return self._dH_dp, self._dH_dq
    
    def poisson_bracket(self, f: sp.Expr, g: sp.Expr) -> sp.Expr:
        """
        {f, g} = Σᵢ (∂f/∂qᵢ ∂g/∂pᵢ - ∂f/∂pᵢ ∂g/∂qᵢ)
        """
        result = 0
        for q_i, p_i in zip(self.q, self.p):
            result += diff(f, q_i) * diff(g, p_i) - diff(f, p_i) * diff(g, q_i)
        
        return simplify(result)
    
    def find_conserved_quantities(self) -> Dict[str, sp.Expr]:
        """
        Find conserved quantities via Noether's theorem.
        
        A quantity Q is conserved if {Q, H} = 0
        """
        conserved = {'energy': self.H}
        
        # Total linear momentum
        P_total = sum(self.p)
        if simplify(self.poisson_bracket(P_total, self.H)) == 0:
            conserved['momentum'] = P_total
        
        # Angular momentum (for 2D+)
        if self.n_dof >= 2:
            L_z = self.q[0] * self.p[1] - self.q[1] * self.p[0]
            if simplify(self.poisson_bracket(L_z, self.H)) == 0:
                conserved['angular_momentum'] = L_z
        
        # Action variables (for integrable systems)
        # Check if H = H(I) only (function of actions)
        # (Advanced - would require action-angle transformation)
        
        return conserved
    
    def symplectic_matrix(self) -> Matrix:
        """
        Construct symplectic matrix J:
        J = [[ 0,  I],
             [-I,  0]]
        
        where I is n×n identity
        """
        n = self.n_dof
        zeros = sp.zeros(n, n)
        identity = sp.eye(n)
        
        J = Matrix.vstack(
            Matrix.hstack(zeros, identity),
            Matrix.hstack(-identity, zeros)
        )
        
        return J
    
    def generate_equations_of_motion(self) -> Callable:
        """
        Generate numerical function for equations of motion.
        
        Returns:
            function(t, state) -> dstate/dt
        """
        dq_dt, dp_dt = self.hamilton_equations()
        
        # Combine into single state vector derivative
        dstate_dt = dq_dt + dp_dt
        
        # Convert to numerical function
        # state = [q0, q1, ..., p0, p1, ...]
        f_numerical = lambdify(
            [self.q + self.p],
            dstate_dt,
            modules='numpy'
        )
        
        def equations_of_motion(t, state):
            """ODE right-hand side: dstate/dt = f(state)"""
            return np.array(f_numerical(*state), dtype=float)
        
        return equations_of_motion
    
    def generate_cython_code(self) -> str:
        """
        Generate Cython code for fast numerical integration.
        
        Returns:
            Cython function source code
        """
        dq_dt, dp_dt = self.hamilton_equations()
        
        code = "# cython: language_level=3\n"
        code += "import numpy as np\n"
        code += "cimport numpy as cnp\n\n"
        code += "cpdef cnp.ndarray[double, ndim=1] hamilton_rhs(\n"
        code += "    cnp.ndarray[double, ndim=1] q,\n"
        code += "    cnp.ndarray[double, ndim=1] p\n"
        code += "):\n"
        code += f"    cdef int n = {self.n_dof}\n"
        code += "    cdef cnp.ndarray[double, ndim=1] dstate = np.zeros(2*n)\n\n"
        
        # Generate dq/dt
        for i, expr in enumerate(dq_dt):
            code += f"    dstate[{i}] = {sp.ccode(expr)}\n"
        
        # Generate dp/dt
        for i, expr in enumerate(dp_dt):
            code += f"    dstate[{self.n_dof + i}] = {sp.ccode(expr)}\n"
        
        code += "\n    return dstate\n"
        
        return code
    
    def linearize_around_equilibrium(self, q_eq: List[float], p_eq: List[float]) -> Matrix:
        """
        Linearize dynamics around equilibrium point.
        
        Returns:
            Jacobian matrix at (q_eq, p_eq)
        """
        dq_dt, dp_dt = self.hamilton_equations()
        
        # State vector and its derivative
        state = list(self.q) + list(self.p)
        dstate_dt = dq_dt + dp_dt
        
        # Jacobian matrix
        n = len(state)
        J = sp.zeros(n, n)
        
        for i, f_i in enumerate(dstate_dt):
            for j, var_j in enumerate(state):
                J[i, j] = diff(f_i, var_j)
        
        # Evaluate at equilibrium
        subs_dict = {**{q_i: q_val for q_i, q_val in zip(self.q, q_eq)},
                     **{p_i: p_val for p_i, p_val in zip(self.p, p_eq)}}
        
        return J.subs(subs_dict)


# Predefined Hamiltonian templates
def harmonic_oscillator_hamiltonian(n_dof: int, k: float = 1.0, m: float = 1.0) -> SymbolicHamiltonian:
    """
    H = Σᵢ [pᵢ²/(2m) + ½kqᵢ²]
    """
    sh = SymbolicHamiltonian(n_dof)
    
    H = 0
    for q_i, p_i in zip(sh.q, sh.p):
        H += p_i**2 / (2*m) + sp.Rational(1,2) * k * q_i**2
    
    sh.set_hamiltonian(H)
    return sh


def coupled_oscillators_hamiltonian(n_dof: int, k: float = 1.0, k_c: float = 0.1, m: float = 1.0) -> SymbolicHamiltonian:
    """
    H = Σᵢ [pᵢ²/(2m) + ½kqᵢ²] + Σᵢ ½k_c(qᵢ - qᵢ₊₁)²
    """
    sh = SymbolicHamiltonian(n_dof)
    
    # Individual oscillators
    H = 0
    for q_i, p_i in zip(sh.q, sh.p):
        H += p_i**2 / (2*m) + sp.Rational(1,2) * k * q_i**2
    
    # Coupling terms
    for i in range(n_dof - 1):
        H += sp.Rational(1,2) * k_c * (sh.q[i] - sh.q[i+1])**2
    
    sh.set_hamiltonian(H)
    return sh


def kepler_hamiltonian() -> SymbolicHamiltonian:
    """
    Kepler problem: H = p²/(2m) - k/r
    
    2D polar coordinates
    """
    sh = SymbolicHamiltonian(n_dof=2)
    
    # q[0] = r, q[1] = θ
    # p[0] = p_r, p[1] = p_θ (angular momentum)
    
    r = sh.q[0]
    p_r = sh.p[0]
    p_theta = sh.p[1]
    
    m = 1.0
    k = 1.0
    
    H = p_r**2 / (2*m) + p_theta**2 / (2*m*r**2) - k/r
    
    sh.set_hamiltonian(H)
    return sh
