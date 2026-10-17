"""End-to-end shot-based VQE and A/B architecture benchmark."""
import json
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.optimize import minimize
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from .problem import hamiltonian, exact_ground_energy, EXACT_TOTAL_HARTREE
from .processors import load_processor, noise_model
from .metrics import compile_for_processor, circuit_metrics

ROOT = Path(__file__).resolve().parents[1]

def h2_ansatz(theta):
    """Lab 5 ansatz: prepare |01> and apply paired XY/YX entanglers."""
    qc = QuantumCircuit(2)
    qc.x(1)
    qc.sdg(0); qc.h(0); qc.h(1)
    qc.cx(0, 1); qc.rz(theta, 1); qc.cx(0, 1)
    qc.h(0); qc.s(0); qc.h(1)
    qc.h(0); qc.sdg(1); qc.h(1)
    qc.cx(0, 1); qc.rz(-theta, 1); qc.cx(0, 1)
    qc.h(0); qc.h(1); qc.s(1)
    return qc

def _parity(counts, qubits):
    total = sum(counts.values())
    return sum(((-1) ** sum(int(bits.replace(" ", "")[-1-q]) for q in qubits)) * n
               for bits, n in counts.items()) / total

def _measurement_circuit(theta, basis):
    qc = h2_ansatz(theta)
    if basis == "X": qc.h([0, 1])
    elif basis == "Y": qc.sdg([0, 1]); qc.h([0, 1])
    qc.measure_all()
    return qc

def _evaluate(theta, processor, backend, shots, seed, seed_transpiler, level, layout):
    counts_by_basis = {}
    compiled_ansatz = None
    for basis in ("Z", "X", "Y"):
        compiled = compile_for_processor(_measurement_circuit(theta, basis), processor,
                                        seed_transpiler, level, layout)
        if basis == "Z": compiled_ansatz = compiled
        result = backend.run(compiled, shots=shots, seed_simulator=seed).result()
        counts_by_basis[basis] = result.get_counts()
    z, x, y = (counts_by_basis[k] for k in ("Z", "X", "Y"))
    z0, z1, zz = _parity(z, [0]), _parity(z, [1]), _parity(z, [0, 1])
    xx, yy = _parity(x, [0, 1]), _parity(y, [0, 1])
    e = hamiltonian().coeffs
    energy = float(np.real(e[0] + e[1]*z0 + e[2]*z1 + e[3]*zz + e[4]*xx + e[5]*yy))
    return energy, compiled_ansatz

def run(config_path=ROOT / "config.json", output_dir=ROOT / "results"):
    config = json.loads(Path(config_path).read_text(encoding="utf-8"))
    output_dir = Path(output_dir); output_dir.mkdir(parents=True, exist_ok=True)
    records, curves = [], {}
    for name in ("processor_A", "processor_B"):
        processor = load_processor(name)
        model = noise_model(processor) if config["run_noisy"] else None
        if config["run_noisy"] and model is None:
            raise ValueError("Noisy run requested, but the official rates are unset. Configure identical rates in both processor JSON files.")
        backend = AerSimulator(noise_model=model)
        history = []
        last = {"compiled": None}
        def objective(values):
            theta = float(np.atleast_1d(values)[0])
            energy, compiled = _evaluate(theta, processor, backend, config["shots"],
                                         config["seed_simulator"], config["seed_transpiler"],
                                         config["optimization_level"], config["initial_layout"])
            history.append((theta, energy)); last["compiled"] = compiled
            return energy
        result = minimize(objective, np.array([config["initial_theta"]]), method="COBYLA",
                          options={"maxiter": config["max_iterations"], "rhobeg": 0.4})
        final_energy, compiled = _evaluate(float(result.x[0]), processor, backend,
                                           config["shots"], config["seed_simulator"],
                                           config["seed_transpiler"], config["optimization_level"],
                                           config["initial_layout"])
        curves[processor["name"]] = history
        metrics = circuit_metrics(compiled)
        records.append({"processor": processor["name"], "theta": float(result.x[0]),
                        "energy_hartree": final_energy, "exact_hartree": exact_ground_energy(),
                        "reference_hartree": config["expected_total_energy_hartree"],
                        "abs_error_vs_exact_hartree": abs(final_energy-exact_ground_energy()),
                        "abs_error_vs_reference_hartree": abs(final_energy-config["expected_total_energy_hartree"]),
                        "noise_enabled": bool(config["run_noisy"]), **metrics})
    pd.DataFrame(records).to_csv(output_dir / "ab_comparison.csv", index=False)
    pd.DataFrame([{"processor": name, "evaluation": i, "theta": theta, "energy_hartree": energy}
                  for name, vals in curves.items() for i, (theta, energy) in enumerate(vals)]).to_csv(
                      output_dir / "convergence.csv", index=False)
    return pd.DataFrame(records), curves

if __name__ == "__main__":
    table, _ = run()
    print(table.to_string(index=False))
