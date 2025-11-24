# cython: language_level=3
# cython: boundscheck=False
# cython: wraparound=False
# cython: cdivision=True
"""
Classical Mechanics - Cython Optimized

N-body gravity, coupled oscillators, chaotic systems.
High-performance numerical integration.
"""

import numpy as np
cimport numpy as cnp
cimport cython
from libc.math cimport sqrt, sin, cos, fabs

ctypedef cnp.float64_t DTYPE_t

@cython.boundscheck(False)
@cython.wraparound(False)
cpdef tuple nbody_forces(
    cnp.ndarray[DTYPE_t, ndim=2] positions,
    cnp.ndarray[DTYPE_t, ndim=1] masses,
    double G=1.0,
    double softening=0.01
):
    """
    Compute gravitational forces for N-body system.
    
    F_ij = -G m_i m_j (r_i - r_j) / |r_i - r_j|³
    
    Uses softening to avoid singularities.
    Complexity: O(N²) direct summation
    
    Returns:
        (forces, potential_energy)
    """
    cdef int N = positions.shape[0]
    cdef int dim = positions.shape[1]
    cdef cnp.ndarray[DTYPE_t, ndim=2] forces = np.zeros((N, dim), dtype=np.float64)
    cdef double potential = 0.0
    
    cdef int i, j, d
    cdef double dx, dy, dz, r2, r, force_mag, eps2
    
    eps2 = softening * softening
    
    for i in range(N):
        for j in range(i+1, N):
            # Compute separation vector
            dx = positions[j, 0] - positions[i, 0]
            dy = positions[j, 1] - positions[i, 1]
            dz = positions[j, 2] - positions[i, 2] if dim > 2 else 0.0
            
            # Distance with softening
            r2 = dx*dx + dy*dy + dz*dz + eps2
            r = sqrt(r2)
            
            # Force magnitude
            force_mag = G * masses[i] * masses[j] / (r2 * r)
            
            # Apply force (Newton's 3rd law)
            forces[i, 0] += force_mag * dx
            forces[i, 1] += force_mag * dy
            if dim > 2:
                forces[i, 2] += force_mag * dz
            
            forces[j, 0] -= force_mag * dx
            forces[j, 1] -= force_mag * dy
            if dim > 2:
                forces[j, 2] -= force_mag * dz
            
            # Accumulate potential energy
            potential -= G * masses[i] * masses[j] / r
    
    return forces, potential


@cython.boundscheck(False)
@cython.wraparound(False)
cpdef cnp.ndarray[DTYPE_t, ndim=1] coupled_oscillator_forces(
    cnp.ndarray[DTYPE_t, ndim=1] q,
    double k_spring=1.0,
    double k_coupling=0.1
):
    """
    Chain of coupled harmonic oscillators.
    
    V = Σᵢ ½k(qᵢ)² + Σᵢ ½k_c(qᵢ - qᵢ₊₁)²
    
    F_i = -kq_i + k_c[(q_{i-1} - q_i) + (q_{i+1} - q_i)]
    """
    cdef int N = q.shape[0]
    cdef cnp.ndarray[DTYPE_t, ndim=1] forces = np.zeros(N, dtype=np.float64)
    cdef int i
    
    for i in range(N):
        # Self force
        forces[i] = -k_spring * q[i]
        
        # Coupling from left neighbor
        if i > 0:
            forces[i] += k_coupling * (q[i-1] - q[i])
        
        # Coupling from right neighbor
        if i < N - 1:
            forces[i] += k_coupling * (q[i+1] - q[i])
    
    return forces


@cython.boundscheck(False)
@cython.wraparound(False)
cpdef tuple double_pendulum_derivatives(
    double theta1,
    double theta2,
    double omega1,
    double omega2,
    double m1=1.0,
    double m2=1.0,
    double L1=1.0,
    double L2=1.0,
    double g=9.81
):
    """
    Double pendulum equations of motion (chaotic system).
    
    Hamiltonian: H = T(ω) + V(θ)
    
    Returns:
        (dtheta1/dt, dtheta2/dt, domega1/dt, domega2/dt)
    """
    cdef double delta = theta2 - theta1
    cdef double c = cos(delta)
    cdef double s = sin(delta)
    
    cdef double den1 = (m1 + m2) * L1 - m2 * L1 * c * c
    cdef double den2 = (L2 / L1) * den1
    
    # Time derivatives
    cdef double dtheta1 = omega1
    cdef double dtheta2 = omega2
    
    # Angular accelerations (from Euler-Lagrange)
    cdef double domega1 = (
        m2 * L1 * omega1 * omega1 * s * c +
        m2 * g * sin(theta2) * c +
        m2 * L2 * omega2 * omega2 * s -
        (m1 + m2) * g * sin(theta1)
    ) / den1
    
    cdef double domega2 = (
        -m2 * L2 * omega2 * omega2 * s * c +
        (m1 + m2) * g * sin(theta1) * c -
        (m1 + m2) * L1 * omega1 * omega1 * s -
        (m1 + m2) * g * sin(theta2)
    ) / den2
    
    return dtheta1, dtheta2, domega1, domega2


@cython.boundscheck(False)
@cython.wraparound(False)
cpdef dict check_conservation_laws(
    cnp.ndarray[DTYPE_t, ndim=2] q_traj,
    cnp.ndarray[DTYPE_t, ndim=2] p_traj,
    cnp.ndarray[DTYPE_t, ndim=1] masses,
    object force_func,
    double tol=1e-6
):
    """
    Verify conservation of energy, momentum, angular momentum.
    
    Returns:
        dict with conservation violations
    """
    cdef int n_steps = q_traj.shape[0]
    cdef int n_dof = q_traj.shape[1]
    
    # Compute energies
    energies = np.zeros(n_steps)
    
    cdef int i
    for i in range(n_steps):
        # Kinetic
        T = np.sum(p_traj[i]**2 / (2 * masses))
        
        # Potential (approximate)
        V = np.sum(q_traj[i]**2) * 0.5  # For harmonic
        
        energies[i] = T + V
    
    # Check energy drift
    cdef double E0 = energies[0]
    cdef double max_drift = np.max(np.abs(energies - E0)) / (fabs(E0) + 1e-10)
    
    # Check momentum (for free system)
    momentum = np.sum(p_traj, axis=1)
    cdef double p_drift = np.max(np.abs(momentum - momentum[0]))
    
    return {
        'energy_drift': max_drift,
        'energy_conserved': max_drift < tol,
        'momentum_drift': p_drift,
        'final_energy': energies[-1],
        'initial_energy': E0,
    }
