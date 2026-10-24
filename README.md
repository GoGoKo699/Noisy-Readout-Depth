# Noisy Readout Depth

**How much coherent control is needed to turn an entangled sensing state into useful data when the detectors are imperfect?**

This project bounds the local Fisher information available from **every input state** after a depth-limited readout circuit and one round of independent noisy detection. A block construction attains the optimal orders of readout depth for Heisenberg-scale information.

There are $N$ qubit sensors with signal generator $H=\frac12\sum_iZ_i$. Readout gates are ideal, and every terminal bit is independently flipped with fixed probability $0<p<1/2$. Depth counts disjoint two-qubit layers; local gates and recorded classical settings are allowed.

| Readout connectivity | Necessary and sufficient depth order for $F_C=\Theta(N^2)$ |
|---|---|
| Full $D$-dimensional cubic grid, nearest-neighbor gates | $\Theta((\log N)^{1/D})$ |
| All-to-all two-qubit gates | $\Theta(\log\log N)$ |

The all-to-all result determines the order, with an unresolved gap in the leading depth coefficient. Geometric achievability uses a full grid; bounded density alone supplies the converse, not the matching construction.

## The information bound

Let $C_i$ support the transformed signal generator $VZ_iV^\dagger/2$. At every phase and for every probe,

```math
F_C\le
\min\left\{N^2,\,
\sum_{i,j}\left[(2p)^{-\lvert C_i\cap C_j\rvert}-1\right]\right\}.
```

Independent detector noise is bounded through a more informative erasure channel. An established environmental-gauge method, evaluated for these supports, makes disjoint contributions cancel. Circuit causality then gives the depth bounds.

On a full cubic grid, the optimum phase-uniform **local** information $\mathcal F(N,d)$ satisfies the sharper frontier

```math
\log\!\left(1+\frac{\mathcal F(N,d)}N\right)
=\Theta_{p,D}\!\left(
\min\{(d+1)^D,\log(1+N)\}\right).
```

The constants are uniform in size and depth for fixed $p,D$. This matches the order of the logarithmic enhancement, not its exact leading coefficient.

## Read the science

Start with the [scientific reading route](science/README.md) and [exact model and statements](science/model.md).

| To understand or check | Read |
|---|---|
| Why arbitrary entanglement cannot evade the bound | [Causal-support converse](science/converse.md) |
| How small readout blocks protect a large sensing phase | [Block construction](science/construction.md) |
| Integer packing, intermediate depth, and the threshold orders | [Finite-size frontier](science/frontier.md) |
| Asymmetric and nonbinary classical detector outputs | [General detectors](science/detectors.md) |
| Physical meaning, preparation cost, and counterexamples | [Interpretation and limits](science/interpretation.md) |
| Inherited methods and closest results | [Related work](references/RELATED_WORK.md) and [bibliography](references/references.bib) |
| Reproducible finite calculations | [Verification](verification/README.md) |

The construction uses GHZ sensing groups, compression within readout blocks, a leader rotation, and re-expansion before classical decoding. It needs no added qubits and at most $2N$ readout CNOT gates. Logarithmic blocks and a recorded uniform phase setting can recover $(1-o(1))N^2$ local information. The same depth orders hold for fixed informative classical detectors with nonzero output overlap.

The global decoder primitive and the general purification machinery are established prior work. A recent ideal-detector result has the same threshold exponents under different quantifiers. The [attribution account](references/RELATED_WORK.md) makes those distinctions explicit.

## Reproduce the checks

With the pinned numerical dependencies installed, run from the repository root:

```bash
python3 -m pip install -r verification/requirements.txt
python3 verification/run_all.py
```

The checks compare explicit small quantum circuits, detector distributions, circuit schedules, grouping calculations and a phase integral with the analytical formulas and committed expected outputs. General bounds and asymptotic claims rest on the written proofs. See [verification](verification/README.md) for commands, coverage and numerical tolerances.

## Scope

The optimized resource is terminal readout depth. The input probe is supplied; its preparation, sensing decoherence and noisy-gate behavior are separate costs. There is one terminal measurement round, independent detector noise, and bounded gate fan-in. The performance measure is local Fisher information, including a phase-uniform local guarantee; GHZ phase aliases remain. These assumptions are illustrated by explicit [counterexamples and resource comparisons](science/interpretation.md).

## Purpose and contact

This repository serves as a record of the work and a guide for the author’s self-directed learning. For discussion or potential collaboration, please contact Ruge Lin at [gogoko699@gmail.com](mailto:gogoko699@gmail.com).
