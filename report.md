# PS-C1 Architecture and Results Report

## Method

The project follows the supplied `H2.ipynb`: a reduced two-qubit H₂ Hamiltonian, a one-parameter number-preserving ansatz, finite-shot Pauli expectation estimates, COBYLA optimization, and exact diagonalization. The source notebook is preserved at `H2_source.ipynb`; the benchmark notebook and reusable modules add Processor A/B routing. The electronic Hamiltonian receives the nuclear-repulsion term before reporting total energy. The supplied coefficients correspond to 0.735 Å, close to the requested 0.74 Å equilibrium; a 0.740 Å run requires regenerated coefficients.

## Processor comparison

The logical circuits are transpiled for the exact five-qubit Processor A and nine-qubit Processor B maps in `processors/`. The initial layout and optimizer budget are tunable. `results/ab_comparison.csv` records energy and error against exact/reference values alongside depth, CX count, SWAP count, and physical width. `results/convergence.csv` records each optimizer evaluation.

## Noise and limitations

The supplied processor configuration identifies the maps but does not verify noise rates. Therefore the project defaults to ideal simulation and refuses to run with noise enabled while rates remain unset. Populate both JSON configurations with the same officially confirmed rates before a noisy comparison. Since this reduced ansatz has only two logical qubits, topology effects can vary substantially with layout; report the selected layout and consider repeating across several layouts. Finite-shot energy estimates have sampling variance.

## Results

Run `main.ipynb` or `python -m src.experiment`; summarize the resulting CSV here after execution. No benchmark numbers are prefilled, so reported performance remains reproducible rather than fabricated.
