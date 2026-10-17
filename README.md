# PS-C1: Tunable H₂ Ground-State VQE Benchmark

**Team Name:** Quantum Mind  
**Team Lead:** Mohammad Hasan Iqbal  
**Problem:** Qiskit Fall Fest 2026 Phase 1, PS-C1  
**Track:** Quantum Chemistry (VQE / ab initio)

This project uses the supplied `H2.ipynb` as its algorithm source and adapts its shot-based VQE workflow into a reproducible, tunable comparison on the fixed Processor A and Processor B coupling maps. The unchanged source notebook is preserved as `H2_source.ipynb`; `main.ipynb` adds the architecture benchmark around reusable Python modules. The repository includes architecture JSON, CSV outputs, and a report.

## Scientific setup

`H2.ipynb` supplies a reduced two-qubit STO-3G Hamiltonian and a one-parameter number-preserving ansatz, estimates Pauli terms with finite shots, optimizes with COBYLA, and compares with exact diagonalization. The Hamiltonian coefficients are documented for **R = 0.735 Å**; this is near the challenge's **0.74 Å** equilibrium. Nuclear repulsion is added to the electronic Hamiltonian so the total energy can be compared with the approximately **−1.137 Hartree** reference. To use exactly 0.740 Å, regenerate the Hamiltonian with Qiskit Nature/PySCF rather than silently treating the supplied coefficients as exact at that geometry.

## Architecture and noise

- Processor A: 5 physical qubits; edges `(0,1), (1,2), (1,3), (3,4)`.
- Processor B: 9 physical qubits; edges `(0,1), (1,2), (1,6), (2,3), (2,6), (2,5), (3,4), (4,5), (5,6), (6,7), (6,8), (8,0)`.
- Basis gates: `rz`, `sx`, `x`, `cx`; transpilation defaults to optimization level 1 and seed 42.
- Noise values are intentionally `null`: the supplied configuration PDF says they are not verified. Ideal simulation is the default. Before enabling noise, enter the same official rates in both processor JSON files and set `run_noisy` to `true` in `config.json`.

## Run

```bash
python -m pip install -r requirements.txt
jupyter notebook main.ipynb
```

Or run the experiment from a terminal:

```bash
python -m src.experiment
```

Tune `config.json` for shots, seeds, optimizer iterations, initial logical-to-physical layout, and noise mode. Run from this project directory. Outputs are written to `results/ab_comparison.csv` and `results/convergence.csv`.

## Included structure

```text
main.ipynb
H2_source.ipynb
config.json
requirements.txt
processors/processor_A.json
processors/processor_B.json
src/problem.py
src/processors.py
src/metrics.py
src/experiment.py
src/visualization.py
results/tables/
results/figures/
report.md
```

The results folders start empty and are populated by the notebook/CLI. Energy accuracy, depth, CX count, SWAP count, and physical qubit width are recorded. SWAP gates may be decomposed during transpilation, so the explicit SWAP count can be zero even when routing adds CX gates; compare routed CX count and depth as well.
