"""Load the fixed Phase 1 processor maps and optional synthetic noise."""
import json
from pathlib import Path
from qiskit.transpiler import CouplingMap
from qiskit_aer.noise import NoiseModel, depolarizing_error, ReadoutError

ROOT = Path(__file__).resolve().parents[1]

def load_processor(name):
    path = ROOT / "processors" / f"{name}.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    data["coupling_map"] = CouplingMap(data["coupling_edges"])
    return data

def noise_model(config):
    """Build homogeneous noise only when all rates are explicitly configured."""
    rates = config["noise"]
    vals = [rates.get(k) for k in ("one_qubit_depolarizing", "cx_depolarizing", "readout_error")]
    if any(v is None for v in vals):
        return None
    p1, pcx, pr = map(float, vals)
    model = NoiseModel()
    model.add_all_qubit_quantum_error(depolarizing_error(p1, 1), ["x", "sx"])
    model.add_all_qubit_quantum_error(depolarizing_error(pcx, 2), ["cx"])
    model.add_all_qubit_readout_error(ReadoutError([[1-pr, pr], [pr, 1-pr]]))
    return model
