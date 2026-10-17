"""Reduced two-qubit H2 Hamiltonian used in the supplied Lab 5."""
from qiskit.quantum_info import SparsePauliOp

# Lab 5 reduced STO-3G coefficients at R=0.735 A (electronic Hamiltonian).
ELECTRONIC_TERMS = [
    ("II", -1.0523732458), ("IZ", 0.3979374248),
    ("ZI", -0.3979374248), ("ZZ", -0.0112801043),
    ("XX", 0.1809311998), ("YY", 0.1809311998),
]
R_ANGSTROM = 0.735
NUCLEAR_REPULSION_HARTREE = 1.0 / (R_ANGSTROM / 0.529177210903)
EXACT_TOTAL_HARTREE = -1.1372701746  # reference for this geometry/basis

def hamiltonian(include_nuclear=True):
    """Return the Pauli Hamiltonian, optionally including nuclear repulsion."""
    terms = list(ELECTRONIC_TERMS)
    if include_nuclear:
        terms[0] = ("II", terms[0][1] + NUCLEAR_REPULSION_HARTREE)
    return SparsePauliOp.from_list(terms)

def exact_ground_energy():
    import numpy as np
    return float(np.linalg.eigvalsh(hamiltonian().to_matrix()).min())
