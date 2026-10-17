"""Transpilation and circuit resource metrics."""
from qiskit import transpile

def compile_for_processor(circuit, processor, seed=42, optimization_level=1, initial_layout=None):
    return transpile(
        circuit, basis_gates=processor["basis_gates"],
        coupling_map=processor["coupling_map"], optimization_level=optimization_level,
        seed_transpiler=seed, initial_layout=initial_layout,
    )

def circuit_metrics(circuit):
    ops = circuit.count_ops()
    return {
        "depth": int(circuit.depth() or 0),
        "cx_count": int(ops.get("cx", 0)),
        "swap_count": int(ops.get("swap", 0)),
        "transpiled_qubits": int(circuit.num_qubits),
    }
