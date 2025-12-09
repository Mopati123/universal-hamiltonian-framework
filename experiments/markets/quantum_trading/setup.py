"""
Setup script for Cython compilation

Compiles .pyx files to C extensions for maximum performance.

Usage:
    python setup.py build_ext --inplace
"""

from setuptools import setup, Extension
from Cython.Build import cythonize
import numpy as np

extensions = [
    Extension(
        "hamiltonian_fast",
        ["hamiltonian_fast.pyx"],
        include_dirs=[np.get_include()],
        extra_compile_args=['-O3', '-march=native', '-fopenmp'],
        extra_link_args=['-fopenmp'],
    )
]

setup(
    name="QuantumTradingFast",
    ext_modules=cythonize(
        extensions,
        compiler_directives={
            'language_level': "3",
            'boundscheck': False,
            'wraparound': False,
            'cdivision': True,
            'nonecheck': False,
        }
    ),
    include_dirs=[np.get_include()],
)
