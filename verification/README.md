# Reproduce the finite checks

The scientific claims are proved in [science/](../science/README.md). These computations check concrete failure modes in the formulas and implementations: channel monotonicity, the erasure-gauge algebra, block parity with even or unequal blocks, legal fanout schedules, finite packing, and asymmetric detector decoding.

## Run

From the repository root:

```bash
python3 -m pip install -r verification/requirements.txt
python3 verification/run_all.py
```

The inspected environment was Python **3.12.14**, NumPy **2.3.5**, and SciPy **1.17.0**. The numerical versions are pinned in [requirements.txt](requirements.txt). Each check locates its expected JSON relative to its own script, so it can also be invoked by absolute path from another directory.

The default commands recompute the results, enforce the scientific assertions, and compare the output with the committed expected data. They do not rewrite those data.

```bash
python3 verification/check_channels.py
python3 verification/check_frontier.py
python3 verification/check_detectors.py
```

To export a fresh report, pass `--output /tmp/name.json` to an individual script. For the channel and frontier scripts this runs all scientific assertions and writes a fresh report instead of comparing the stored baseline. The detector script additionally performs its baseline comparison before export. Exporting a report is not permission to replace a baseline without investigating a discrepancy.

## Coverage and actual results

All three modules passed in the inspected environment on **24 October 2026**.

| Module and expected output | What is compared | Cases |
|---|---|---:|
| [check_channels.py](check_channels.py), [expected_channels.json](expected_channels.json) | Four-qubit pure and mixed inputs; local Haar gates at every depth; depths 0, 1, 2; BSC errors 0.1, 0.3, 0.45. Direct classical FI, flagged-erasure QFI, support bound and input QFI; finite-difference probability derivatives. | 18 channels |
| Same channel module | Explicit erasure-subset covariance and a matrix-valued gauge identity for overlapping, nonuniform causal supports. | 2 algebra checks |
| Same channel module | Full statevector compress–Hadamard–fanout circuits, BSC noise, and stochastic majority/parity processing versus the exact likelihood, derivative and FI. Odd, even and unequal blocks; three phases including off-quadrature; up to 9 qubits. | 63 decoder settings |
| [check_frontier.py](check_frontier.py), [expected_frontier.json](expected_frontier.json) | Actual gate schedules: disjointness, nearest-neighbor legality, both logical basis strings, compression by reversal, gate counts and depth. | 12 lattice + 12 all-to-all schedules |
| Same frontier module | Enumerated detector strings versus the binomial majority formula and bit symmetry, including fair ties. | 18 cases |
| Same frontier module | Exact finite grouping FI versus the conservative lower bound; includes incomplete groups and zero entangling depth. | 210 cases |
| Same frontier module | Complete cube tilings, uncovered sites, active fraction and depth budget. | 36 tilings |
| Same frontier module | Numerical quadrature of the phase-averaged parity FI versus $1-\sqrt{1-v^2}$, at several phase offsets. | 15 integrals |
| [check_detectors.py](check_detectors.py), [expected_detectors.json](expected_detectors.json) | Exact rational likelihood enumeration for asymmetric ternary, one-sided binary and BSC detectors; overlap decomposition, Bayes error and complement symmetrization. | 9 repetition cases |
| Same detector module | Fair ties, GHZ-correlated block bits, and biased correlated input distributions with explicit independent masks. | 2 tie + 9 parity + 3 biased-input cases |

The random-channel seed is **20261024**. All other case choices are deterministic. Random input samples probe implementation failures; they are not an ensemble theorem or a search over all states.

Representative numerical discrepancies from this run:

| Identity | Maximum absolute discrepancy |
|---|---:|
| Erasure coefficient covariance | $8.89\times10^{-16}$ |
| Matrix gauge equality | $3.56\times10^{-15}$ |
| Gauge operator norm versus scalar coefficient sum | $1.85\times10^{-13}$ |
| Decoder FI versus its analytical formula | $1.57\times10^{-13}$ |
| Probability derivative versus central finite difference | $1.91\times10^{-11}$ |
| Uniform-phase integral | $2.11\times10^{-15}$ |
| General detector identities | $1.67\times10^{-16}$ |

Values are rounded upward for this table; the committed JSON files contain the actual floating-point outputs. Portable baseline comparisons use absolute and relative tolerances: respectively $10^{-10}$ and $3\times10^{-8}$ for channels, $2\times10^{-11}$ and $2\times10^{-9}$ for the frontier, and $10^{-12}$ and $10^{-10}$ for detectors. Each module also enforces its own claim-specific inequalities. These checks remain active under Python optimization because they raise explicitly rather than relying on disabled `assert` statements.

## How to interpret a failure

A failed comparison identifies the case and location. First distinguish a meaningful violated identity or inequality from an expected floating-point variation. Check the pinned environment and the corresponding equation before changing a tolerance or baseline. The likelihood and channel calculations use different representations from the closed-form predictions, so agreement is more informative than comparing two copies of the same formula.

## Evidence boundaries

The finite checks do not prove the arbitrary-probe converse, the asymptotic frontier, or a publication-priority claim. They also do not simulate gate noise, sensing decoherence, a global phase estimator or an experimental apparatus.

The analytical proof dependencies are:

1. [Converse](../science/converse.md): exact channel degradation, a valid environmental gauge, and the support covariance.
2. [Construction](../science/construction.md): exact parity likelihood and finite discrimination error.
3. [Frontier](../science/frontier.md): integer grouping, spatial tiling, and the asymptotic inequalities.
4. [General detectors](../science/detectors.md): common-overlap simulation and asymmetric logical-channel symmetrization.

Source checks and numerical tests also do not establish correct rendering by a hosting platform. Mathematical display is a separate visual inspection.
