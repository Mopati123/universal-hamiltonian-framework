from setuptools import setup, Extension
from Cython.Build import cythonize
import numpy as np

# Cython extensions for performance-critical numerical code
extensions = [
    Extension(
        "uvh.core.canonical_transforms",
        ["src/core/canonical_transforms.pyx"],
        include_dirs=[np.get_include()],
        extra_compile_args=["/O2"] if hasattr(__builtins__, '_is_windows') else ["-O3", "-march=native"],
    ),
    Extension(
        "uvh.domains.classical_mechanics",
        ["src/domains/classical_mechanics.pyx"],
        include_dirs=[np.get_include()],
        extra_compile_args=["/O2"] if hasattr(__builtins__, '_is_windows') else ["-O3", "-march=native"],
    ),
]

setup(
    name="universal-hamiltonian-framework",
    ext_modules=cythonize(
        extensions,
        compiler_directives={
            'language_level': "3",
            'boundscheck': False,
            'wraparound': False,
            'cdivision': True,
            'embedsignature': True,
        }
    ),
    include_dirs=[np.get_include()],
)
