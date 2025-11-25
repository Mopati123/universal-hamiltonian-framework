"""
Meta-Framework: The Framework That Evolves Itself

This is the strange loop - the Universal Hamiltonian Framework
observing and evolving its own structure.

Treats the codebase as a Hamiltonian system and suggests natural
evolution paths based on energy minimization.
"""

import os
import ast
from typing import List, Dict, Tuple
from pathlib import Path
import numpy as np


class FrameworkEvolver:
    """
    Meta-Hamiltonian that treats the codebase as a phase-space system.
    
    Configuration (q): File structure, module organization
    Momentum (p): Dependencies, import relationships
    Energy (H): Coupling strength, code duplication, missing components
    
    Natural evolution → Minimize energy → Better structure
    """
    
    def __init__(self, framework_root: str):
        """
        Args:
            framework_root: Path to framework root directory
        """
        self.root = Path(framework_root)
        self.structure = {}
        self.coupling_matrix = None
        self.energy_gradients = {}
    
    def analyze_structure(self) -> Dict:
        """
        Scan codebase and build phase-space representation.
        
        Returns:
            Structure dict with files, modules, coupling
        """
        print("Analyzing framework structure...")
        
        # Find all Python files
        python_files = list(self.root.rglob('*.py'))
        
        structure = {
            'files': [],
            'modules': set(),
            'imports': {},
            'classes': {},
            'functions': {},
        }
        
        for file_path in python_files:
            if '__pycache__' in str(file_path):
                continue
            
            rel_path = file_path.relative_to(self.root)
            structure['files'].append(str(rel_path))
            
            # Parse file
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    tree = ast.parse(f.read())
                
                # Extract imports
                imports = []
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            imports.append(alias.name)
                    elif isinstance(node, ast.ImportFrom):
                        if node.module:
                            imports.append(node.module)
                
                structure['imports'][str(rel_path)] = imports
                
                # Extract classes
                classes = [node.name for node in ast.walk(tree) 
                          if isinstance(node, ast.ClassDef)]
                structure['classes'][str(rel_path)] = classes
                
                # Extract functions
                functions = [node.name for node in ast.walk(tree)
                            if isinstance(node, ast.FunctionDef)]
                structure['functions'][str(rel_path)] = functions
                
            except Exception as e:
                print(f"  Warning: Could not parse {rel_path}: {e}")
        
        self.structure = structure
        return structure
    
    def compute_coupling_matrix(self) -> np.ndarray:
        """
        Compute coupling strength between modules.
        
        Coupling = number of shared imports / total imports
        
        Returns:
            NxN coupling matrix (0 = no coupling, 1 = max coupling)
        """
        files = self.structure['files']
        n = len(files)
        
        coupling = np.zeros((n, n))
        
        for i, file_i in enumerate(files):
            imports_i = set(self.structure['imports'].get(file_i, []))
            
            for j, file_j in enumerate(files):
                if i == j:
                    coupling[i, j] = 1.0
                    continue
                
                imports_j = set(self.structure['imports'].get(file_j, []))
                
                if imports_i or imports_j:
                    shared = len(imports_i & imports_j)
                    total = len(imports_i | imports_j)
                    coupling[i, j] = shared / total if total > 0 else 0.0
        
        self.coupling_matrix = coupling
        return coupling
    
    def identify_energy_voids(self) -> List[Dict]:
        """
        Find missing components (infinite energy points).
        
        Returns:
            List of missing files/components that should exist
        """
        voids = []
        
        # Check for missing __init__.py files
        for directory in self.root.rglob('*'):
            if not directory.is_dir():
                continue
            if '__pycache__' in str(directory):
                continue
            
            # If directory has .py files but no __init__.py
            py_files = list(directory.glob('*.py'))
            init_file = directory / '__init__.py'
            
            if py_files and not init_file.exists():
                voids.append({
                    'type': 'missing_init',
                    'path': str(init_file.relative_to(self.root)),
                    'energy': float('inf'),
                    'reason': 'Directory with Python files needs __init__.py'
                })
        
        # Check for isolated modules (weak coupling)
        if self.coupling_matrix is not None:
            mean_coupling = self.coupling_matrix.mean(axis=1)
            
            for i, file in enumerate(self.structure['files']):
                if mean_coupling[i] < 0.1:  # Weak coupling threshold
                    voids.append({
                        'type': 'isolated_module',
                        'path': file,
                        'energy': 1.0 / (mean_coupling[i] + 0.01),
                        'reason': f'Weak coupling: {mean_coupling[i]:.3f}'
                    })
        
        # Sort by energy (highest first)
        voids.sort(key=lambda x: x['energy'], reverse=True)
        
        return voids
    
    def suggest_evolution(self) -> List[Dict]:
        """
        Suggest natural evolution paths following energy gradients.
        
        Returns:
            List of suggested changes (new files, refactorings, etc.)
        """
        suggestions = []
        
        # Analyze structure first
        if not self.structure:
            self.analyze_structure()
        
        if self.coupling_matrix is None:
            self.compute_coupling_matrix()
        
        # Find voids
        voids = self.identify_energy_voids()
        
        for void in voids[:5]:  # Top 5 highest energy
            if void['type'] == 'missing_init':
                suggestions.append({
                    'action': 'create_file',
                    'path': void['path'],
                    'priority': 'critical',
                    'reason': void['reason']
                })
        
        # Suggest coupling strengthening
        files = self.structure['files']
        n = len(files)
        
        for i in range(n):
            for j in range(i+1, n):
                coupling = self.coupling_matrix[i, j]
                
                # If both are in same subsystem but weakly coupled
                file_i, file_j = files[i], files[j]
                
                if self._same_subsystem(file_i, file_j) and coupling < 0.3:
                    suggestions.append({
                        'action': 'strengthen_coupling',
                        'files': [file_i, file_j],
                        'current_coupling': coupling,
                        'priority': 'medium',
                        'reason': 'Related modules should have stronger coupling'
                    })
        
        return suggestions
    
    def _same_subsystem(self, file1: str, file2: str) -> bool:
        """Check if two files are in the same subsystem"""
        parts1 = Path(file1).parts
        parts2 = Path(file2).parts
        
        if len(parts1) < 2 or len(parts2) < 2:
            return False
        
        # Same if first two path components match (e.g., src/core)
        return parts1[:2] == parts2[:2]
    
    def auto_generate_domain(self, specification: Dict) -> str:
        """
        Generate a new domain module from specification.
        
        Args:
            specification: Dict with 'name', 'coordinates', 'hamiltonian'
        
        Returns:
            Generated Python code
        """
        name = specification['name']
        coords = specification.get('coordinates', ['x'])
        
        code = f'''"""
{name} Domain - Auto-generated by Meta-Framework

This domain was automatically generated based on the specification:
{specification.get('description', 'No description provided')}
"""

from compiler import define_system
import numpy as np


@define_system
class {name}Hamiltonian:
    """
    {name} system as Hamiltonian.
    
    Coordinates: {', '.join(coords)}
    """
    coordinates = {coords}
    
    def kinetic(self, p):
        """Kinetic energy"""
        # TODO: Implement based on specification
        return sum(getattr(p, f'p{{c}}') ** 2 / 2 for c in self.coordinates)
    
    def potential(self, q):
        """Potential energy"""
        # TODO: Implement based on specification
        return sum(0.5 * getattr(q, c) ** 2 for c in self.coordinates)


# Additional domain-specific functions
def create_{name.lower()}_state(**kwargs):
    """Create initial state for {name} system"""
    from core import PhaseSpace
    
    q = np.array([kwargs.get(c, 0.0) for c in {coords}])
    p = np.zeros_like(q)
    
    return PhaseSpace(q=q, p=p)
'''
        
        return code
    
    def report(self):
        """Generate evolution report"""
        print("\n" + "="*70)
        print("META-FRAMEWORK EVOLUTION REPORT")
        print("="*70)
        print()
        
        # Structure summary
        print(f"Files analyzed: {len(self.structure.get('files', []))}")
        print(f"Total classes: {sum(len(v) for v in self.structure.get('classes', {}).values())}")
        print(f"Total functions: {sum(len(v) for v in self.structure.get('functions', {}).values())}")
        print()
        
        # Coupling analysis
        if self.coupling_matrix is not None:
            mean_coupling = self.coupling_matrix[self.coupling_matrix < 1.0].mean()
            print(f"Average coupling strength: {mean_coupling:.3f}")
            print()
        
        # Energy voids
        voids = self.identify_energy_voids()
        if voids:
            print(f"Energy voids detected: {len(voids)}")
            print("\nTop 3 highest energy:")
            for void in voids[:3]:
                print(f"  • {void['path']} (E={void['energy']:.2f})")
                print(f"    → {void['reason']}")
            print()
        
        # Suggestions
        suggestions = self.suggest_evolution()
        if suggestions:
            print(f"Evolution suggestions: {len(suggestions)}")
            print("\nTop priorities:")
            for sug in suggestions[:5]:
                print(f"  • {sug['action']}: {sug.get('path', sug.get('files', ''))}")
                print(f"    Priority: {sug['priority']}")
            print()
        
        print("="*70)
        print()


# Convenience function
def evolve_framework(framework_root: str = '.'):
    """
    Run meta-analysis and evolution on framework.
    
    Example:
        from meta import evolve_framework
        evolve_framework()
    """
    evolver = FrameworkEvolver(framework_root)
    evolver.analyze_structure()
    evolver.compute_coupling_matrix()
    evolver.report()
    
    return evolver


if __name__ == '__main__':
    # Self-evolution
    print("Framework observing itself...")
    evolver = evolve_framework('.')
    
    print("\nThe strange loop is complete.")
    print("The framework knows what it wants to become.")
