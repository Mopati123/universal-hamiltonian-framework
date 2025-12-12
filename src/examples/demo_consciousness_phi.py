"""
Minimal IntegratedInformationCalculator wrapper for tests.

This module mirrors the calculation used by the examples directory, but
is placed inside `src/examples` so tests importing `examples.*` find it
when `src` is added to sys.path by the test runner.
"""

import numpy as np
from itertools import combinations
from typing import List, Tuple


class IntegratedInformationCalculator:
    def __init__(self, system_hamiltonian):
        self.H_full = system_hamiltonian

    def compute_phi(self, state: np.ndarray, partition_method: str = 'mip') -> float:
        n_dof = len(state) // 2
        if n_dof <= 1:
            return 0.0

        # sampling-based Gaussian approximation: estimate covariance around state
        n_samples = 256
        # noise scale proportional to typical magnitude or fallback
        mag = np.max(np.abs(state))
        noise_scale = max(1e-6, 1e-3 * mag)
        samples = np.tile(state, (n_samples, 1)) + np.random.normal(0, noise_scale, size=(n_samples, len(state)))

        # Compute full covariance matrix with jitter for stability
        cov_full = np.cov(samples, rowvar=False)
        eps = 1e-8
        cov_full += eps * np.eye(cov_full.shape[0])

        def logdet(mat):
            sign, ld = np.linalg.slogdet(mat)
            return ld if sign > 0 else float('inf')

        logdet_full = logdet(cov_full)

        min_mi = float('inf')
        mean_mi = 0.0
        parts = list(self._generate_bipartitions(n_dof))
        mi_list = []
        for partition in parts:
            partA, partB = partition
            # indices for q and p variables in full vector
            idxA = [i for i in partA] + [n_dof + i for i in partA]
            idxB = [i for i in partB] + [n_dof + i for i in partB]
            covA = cov_full[np.ix_(idxA, idxA)] + eps * np.eye(len(idxA))
            covB = cov_full[np.ix_(idxB, idxB)] + eps * np.eye(len(idxB))
            logdetA = logdet(covA)
            logdetB = logdet(covB)
            # mutual information for this partition: I(A;B) = H(A)+H(B)-H(A,B)
            mi = 0.5 * (logdetA + logdetB - logdet_full)
            mean_mi += mi
            mi_list.append(mi)
            if mi < min_mi:
                min_mi = mi

        mean_mi /= len(parts)

        if partition_method == 'mip':
            phi = min_mi
        else:
            phi = mean_mi
        # If system Hamiltonian is available, use coupling energy across the MIP
        if self.H_full is not None and len(parts) > 0:
            try:
                n = n_dof
                q = state[:n]
                p = state[n:]
                H_full_val = float(self.H_full.hamiltonian(q, p))
                # Use MIP found above (min_mi) partition: pick partition with minimal mi
                # Find partition corresponding to min_mi
                min_partition_idx = int(np.argmin(mi_list)) if len(mi_list) > 0 else 0
                part_A, part_B = parts[min_partition_idx]
                # Build full-length q/p arrays for subsystem hamiltonians with other coords zeroed
                qA_full = np.zeros_like(q)
                pA_full = np.zeros_like(p)
                qB_full = np.zeros_like(q)
                pB_full = np.zeros_like(p)
                qA_full[part_A] = q[part_A]
                pA_full[part_A] = p[part_A]
                qB_full[part_B] = q[part_B]
                pB_full[part_B] = p[part_B]
                H_A = float(self.H_full.hamiltonian(qA_full, pA_full))
                H_B = float(self.H_full.hamiltonian(qB_full, pB_full))
                coupling_energy = H_full_val - (H_A + H_B)
                phi += abs(coupling_energy)
            except Exception:
                # In case the Hamiltonian interface does not accept partitioned inputs
                pass

        return max(0.0, phi)

    def _phase_space_information(self, state: np.ndarray) -> float:
        n_dof = len(state) // 2
        q = state[:n_dof]
        p = state[n_dof:]
        volume = np.sqrt(np.sum(q**2) * np.sum(p**2))
        return float(np.log(volume + 1e-10))

    def _partition_information(self, state: np.ndarray, partition: Tuple[List[int], List[int]]) -> float:
        part_A, part_B = partition
        n_dof = len(state) // 2
        q_full = state[:n_dof]
        p_full = state[n_dof:]
        state_A = np.concatenate([q_full[part_A], p_full[part_A]])
        state_B = np.concatenate([q_full[part_B], p_full[part_B]])
        return self._phase_space_information(state_A) + self._phase_space_information(state_B)

    def _generate_bipartitions(self, n_dof: int):
        dofs = list(range(n_dof))
        partitions = []
        for i in range(1, n_dof):
            for subset_A in combinations(dofs, i):
                subset_A = list(subset_A)
                subset_B = [d for d in dofs if d not in subset_A]
                partitions.append((subset_A, subset_B))
        return partitions
