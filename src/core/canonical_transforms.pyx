# cython: language_level=3
# cython: boundscheck=False
# cython: wraparound=False
# cython: cdivision=True
"""
Canonical Transformations - Cython Implementation

High-performance coordinate transformations preserving symplectic structure.
Implements generating functions and Poisson bracket algebra.
"""

import numpy as np
cimport numpy as cnp
cimport cython
from libc.math cimport sin, cos, sqrt, atan2

ctypedef cnp.float64_t DTYPE_t

@cython.boundscheck(False)
@cython.wraparound(False)
cpdef cnp.ndarray[DTYPE_t, ndim=1] generating_function_F2(
    cnp.ndarray[DTYPE_t, ndim=1] q,
    cnp.ndarray[DTYPE_t, ndim=1] P,
    double alpha
):
    """
    Type-2 generating function: F₂(q, P)
    
    Generates canonical transformation:
    p_i = ∂F₂/∂q_i
    Q_i = ∂F₂/∂P_i
    
    Example: F₂ = q·P + α·f(q, P) for perturbative transforms
    """
    cdef int n = q.shape[0]
    cdef cnp.ndarray[DTYPE_t, ndim=1] Q = np.zeros(n, dtype=np.float64)
    cdef cnp.ndarray[DTYPE_t, ndim=1] p = np.zeros(n, dtype=np.float64)
    cdef int i
    
    # Identity transformation: F₂ = q·P
    for i in range(n):
        p[i] = P[i]
        Q[i] = q[i]
    
    return Q


@cython.boundscheck(False)
@cython.wraparound(False)
cpdef tuple action_angle_variables(
    cnp.ndarray[DTYPE_t, ndim=1] q,
    cnp.ndarray[DTYPE_t, ndim=1] p,
    double omega
):
    """
    Transform to action-angle variables (I, θ) for harmonic oscillator.
    
    For H = p²/2m + ½mω²q²:
    I = (p² + m²ω²q²) / (2mω)  (action - conserved)
    θ = atan2(p, mωq)           (angle - increases linearly)
    
    Returns: (I, theta)
    """
    cdef int n = q.shape[0]
    cdef cnp.ndarray[DTYPE_t, ndim=1] I = np.zeros(n, dtype=np.float64)
    cdef cnp.ndarray[DTYPE_t, ndim=1] theta = np.zeros(n, dtype=np.float64)
    cdef int i
    cdef double m = 1.0  # Unit mass
    
    for i in range(n):
        # Action variable
        I[i] = (p[i]**2 + m**2 * omega**2 * q[i]**2) / (2.0 * m * omega)
        
        # Angle variable
        theta[i] = atan2(p[i], m * omega * q[i])
    
    return I, theta


@cython.boundscheck(False)
@cython.wraparound(False)
cpdef double poisson_bracket(
    cnp.ndarray[DTYPE_t, ndim=1] f_q,
    cnp.ndarray[DTYPE_t, ndim=1] f_p,
    cnp.ndarray[DTYPE_t, ndim=1] g_q,
    cnp.ndarray[DTYPE_t, ndim=1] g_p
):
    """
    Compute Poisson bracket: {f, g} = Σᵢ (∂f/∂qᵢ ∂g/∂pᵢ - ∂f/∂pᵢ ∂g/∂qᵢ)
    
    Args:
        f_q: ∂f/∂q (gradient w.r.t. positions)
        f_p: ∂f/∂p (gradient w.r.t. momenta)
        g_q: ∂g/∂q
        g_p: ∂g/∂p
    
    Returns:
        Poisson bracket scalar value
    """
    cdef int n = f_q.shape[0]
    cdef double result = 0.0
    cdef int i
    
    for i in range(n):
        result += f_q[i] * g_p[i] - f_p[i] * g_q[i]
    
    return result


@cython.boundscheck(False)
@cython.wraparound(False)
cpdef bint is_canonical_transform(
    cnp.ndarray[DTYPE_t, ndim=2] M,
    double tol=1e-10
):
    """
    Check if transformation matrix M is symplectic (canonical).
    
    A transformation is canonical if: M^T J M = J
    where J = [[0, I], [-I, 0]] is the symplectic matrix.
    
    Args:
        M: 2n×2n transformation matrix
        tol: Numerical tolerance
    
    Returns:
        True if transformation is canonical
    """
    cdef int n = M.shape[0] // 2
    cdef cnp.ndarray[DTYPE_t, ndim=2] J = np.zeros((2*n, 2*n), dtype=np.float64)
    cdef int i, j
    
    # Construct symplectic matrix J
    for i in range(n):
        J[i, n+i] = 1.0
        J[n+i, i] = -1.0
    
    # Compute M^T J M
    cdef cnp.ndarray[DTYPE_t, ndim=2] result = M.T @ J @ M
    
    # Check if result equals J
    cdef double max_diff = 0.0
    for i in range(2*n):
        for j in range(2*n):
            max_diff = max(max_diff, abs(result[i,j] - J[i,j]))
    
    return max_diff < tol


@cython.boundscheck(False)
@cython.wraparound(False)
cpdef cnp.ndarray[DTYPE_t, ndim=1] symplectic_gradient(
    cnp.ndarray[DTYPE_t, ndim=1] q,
    cnp.ndarray[DTYPE_t, ndim=1] p,
    object hamiltonian_func,
    double epsilon=1e-7
):
    """
    Compute symplectic gradient: (∂H/∂p, -∂H/∂q)
    
    This gives Hamilton's equations:
    dq/dt = ∂H/∂p
    dp/dt = -∂H/∂q
    
    Uses finite differences for numerical gradient.
    """
    cdef int n = q.shape[0]
    cdef cnp.ndarray[DTYPE_t, ndim=1] grad_q = np.zeros(n, dtype=np.float64)
    cdef cnp.ndarray[DTYPE_t, ndim=1] grad_p = np.zeros(n, dtype=np.float64)
    cdef cnp.ndarray[DTYPE_t, ndim=1] result = np.zeros(2*n, dtype=np.float64)
    cdef int i
    cdef double H_plus, H_minus
    
    # Numerical gradient w.r.t. positions
    for i in range(n):
        q[i] += epsilon
        H_plus = hamiltonian_func(q, p)
        q[i] -= 2*epsilon
        H_minus = hamiltonian_func(q, p)
        q[i] += epsilon  # Restore
        grad_q[i] = (H_plus - H_minus) / (2*epsilon)
    
    # Numerical gradient w.r.t. momenta
    for i in range(n):
        p[i] += epsilon
        H_plus = hamiltonian_func(q, p)
        p[i] -= 2*epsilon
        H_minus = hamiltonian_func(q, p)
        p[i] += epsilon  # Restore
        grad_p[i] = (H_plus - H_minus) / (2*epsilon)
    
    # Pack as (dq/dt, dp/dt) = (∂H/∂p, -∂H/∂q)
    for i in range(n):
        result[i] = grad_p[i]        # dq/dt
        result[n+i] = -grad_q[i]     # dp/dt
    
    return result
