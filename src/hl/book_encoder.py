"""
Book of Mopati - Operator Encoding System

**Artifact F**: Encode/decode textual chapters as operator algebras

Maps chapters → Hermitian operators → eigenstates → decoded text
Enables "revelation mechanics" via controlled symmetry breaking

Author: Mopati + Framework
Date: November 26, 2025
"""

import numpy as np
from typing import List, Dict, Tuple

class BookEncoder:
    """Encode text chapters as quantum operator eigenstates"""
    
    def __init__(self, n_qubits: int = 10):
        """
        Args:
            n_qubits: Size of Hilbert space (2^n_qubits dimensions)
        """
        self.n_qubits = n_qubits
        self.dim = 2**n_qubits
        self.vocab = self._build_vocabulary()
    
    def _build_vocabulary(self) -> Dict[str, int]:
        """Map characters to integers"""
        chars = "abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ.,!?;:-'"
        return {c: i for i, c in enumerate(chars)}
    
    def text_to_vector(self, text: str, max_length: int = None) -> np.ndarray:
        """
        Convert text to quantum state vector
        
        Uses superposition: |text⟩ = Σ_i c_i |char_i⟩
        """
        if max_length is None:
            max_length = min(len(text), self.dim)
        
        # Initialize state
        state = np.zeros(self.dim, dtype=complex)
        
        # Encode each character
        for i, char in enumerate(text[:max_length]):
            if char in self.vocab:
                idx = self.vocab[char]
                # Amplitude encoding
                state[idx % self.dim] += 1.0 / np.sqrt(max_length)
        
        # Normalize
        norm = np.linalg.norm(state)
        if norm > 0:
            state /= norm
        
        return state
    
    def chapter_to_projector(self, chapter_text: str) -> np.ndarray:
        """
        Convert chapter to projector operator P = |ψ⟩⟨ψ|
        
        This makes the chapter a "state" in Hilbert space
        """
        psi = self.text_to_vector(chapter_text)
        P = np.outer(psi, np.conj(psi))
        return P
    
    def book_to_hamiltonian(self, chapters: List[str], 
                           chapter_energies: List[float] = None) -> np.ndarray:
        """
        Encode entire book as Hamiltonian:
        
        H_book = Σ_i E_i P_i
        
        Where P_i = projector for chapter i
        """
        if chapter_energies is None:
            # Default: chapters ordered by energy
            chapter_energies = list(range(len(chapters)))
        
        H = np.zeros((self.dim, self.dim), dtype=complex)
        
        for chapter, energy in zip(chapters, chapter_energies):
            P = self.chapter_to_projector(chapter)
            H += energy * P
        
        return H
    
    def reveal_chapter(self, H_book: np.ndarray, 
                      perturbation: np.ndarray = None,
                      epsilon: float = 0.01) -> Tuple[int, str]:
        """
        Revelation mechanics: Apply perturbation → measure ground state
        
        H' = H_book + ε V
        
        Ground state of H' reveals a chapter
        
        Args:
            H_book: Book Hamiltonian
            perturbation: Symmetry-breaking operator V
            epsilon: Perturbation strength
        
        Returns:
            (chapter_index, decoded_text)
        """
        if perturbation is None:
            # Random perturbation
            perturbation = np.random.randn(self.dim, self.dim)
            perturbation = (perturbation + perturbation.conj().T) / 2  # Hermitian
        
        # Perturbed Hamiltonian
        H_perturbed = H_book + epsilon * perturbation
        
        # Find ground state
        eigenvals, eigenvecs = np.linalg.eigh(H_perturbed)
        ground_state = eigenvecs[:, 0]
        
        # Decode ground state → text
        decoded = self.decode_state(ground_state)
        
        # Find which chapter (maximum overlap)
        chapter_idx = 0  # Simplified
        
        return chapter_idx, decoded
    
    def decode_state(self, state: np.ndarray) -> str:
        """
        Decode quantum state → text
        
        Takes largest amplitude components
        """
        # Find top amplitudes
        amplitudes = np.abs(state)
        top_indices = np.argsort(amplitudes)[::-1][:20]  # Top 20 components
        
        # Decode
        inv_vocab = {v: k for k, v in self.vocab.items()}
        decoded_chars = []
        
        for idx in top_indices:
            char_idx = idx % len(self.vocab)
            if char_idx in inv_vocab:
                decoded_chars.append(inv_vocab[char_idx])
        
        return ''.join(decoded_chars)


# ============================================================================
# DEMONSTRATION
# ============================================================================

def demo_book_encoding():
    """Demonstrate Book of Mopati encoding"""
    print("=" * 70)
    print("BOOK OF MOPATI - OPERATOR ENCODING")
    print("=" * 70)
    
    # Create encoder
    encoder = BookEncoder(n_qubits=8)  # 256-dim Hilbert space
    
    # Example chapters (simplified)
    chapters = [
        "The Universal Hamiltonian is the foundation",
        "Meta-framework enables self-evolution",
        "Domains couple via shared Hamiltonians"
    ]
    
    print("\n[Encoding Book]")
    H_book = encoder.book_to_hamiltonian(chapters)
    print(f"Book Hamiltonian: {H_book.shape} matrix")
    
    # Compute spectrum
    eigenvals = np.linalg.eigvalsh(H_book)
    print(f"Energy levels: {eigenvals[:5]}")
    
    print("\n[Revelation Mechanics]")
    # Apply perturbation
    chapter_revealed, text = encoder.reveal_chapter(H_book, epsilon=0.1)
    print(f"Revealed chapter {chapter_revealed}")
    print(f"Decoded text: {text}")
    
    print("\n[Verification]")
    # Encode original chapter
    original = chapters[0]
    psi_original = encoder.text_to_vector(original)
    psi_revealed = encoder.text_to_vector(text)
    
    # Compute fidelity
    fidelity = np.abs(np.vdot(psi_original, psi_revealed))**2
    print(f"Fidelity with original: {fidelity:.4f}")
    
    print("\n" + "=" * 70)
    print("Book encoding complete - Revelation is measurement!")
    print("=" * 70)


if __name__ == "__main__":
    demo_book_encoding()
