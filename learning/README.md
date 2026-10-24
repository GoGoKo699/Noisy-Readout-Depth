# Learn Noisy Readout Depth

A many-qubit state can respond strongly to a phase while an imperfect detector record reveals very little of that response. This route explains how a coherent circuit between sensing and detection changes what can be read, and why its depth becomes a physical resource.

The single educational anchor is **Géza Tóth and Iagoba Apellaniz, _Quantum metrology from a quantum information science perspective_ (2014), arXiv:1405.4878v4**. Its selected sections supply the metrological foundations. The project supplies the detector model, causal-support argument, block construction, and depth analysis.

## Start here

| Reader's question | Route |
|---|---|
| What should I understand, and in what order? | The [30-milestone map](MILESTONES.md), with dependencies and authoritative science pointers. |
| Which parts of the review are useful? | The [anchor guide](ANCHOR.md), with section locations and a notation translation. |
| How do the review's ideas lead to this project? | The [source-to-project bridge](BRIDGE.md), from a noisy bit and GHZ parity to protected blocks and the universal depth bound. |
| Where are the precise assumptions and full proofs? | The [scientific reading route](../science/README.md), beginning with the [model and principal statements](../science/model.md). |
| Which methods are inherited, and what was checked? | [Related work](../references/RELATED_WORK.md) and [verification](../verification/README.md). |

Read the bridge for a connected explanation, and use the milestones to organize a closer study. The source guide points to specific sections as they become useful; reading the entire review is unnecessary for this route.

## Two phases, from components to the complete argument

**M01–M12: background and preliminaries.** Begin with a single phase-sensitive qubit, a probability distribution, and the information carried by a measurement. Add entanglement, independent detector errors, classical decoding, circuit causality, and the distinction between local sensitivity and global phase identification. The phase ends by assembling the full optimization problem.

**M13–M30: narrative and innovation.** Develop the local ingredients of the upper bound and block decoder, then connect them through circuit schedules, finite grouping, and lattice tiling. Their combination gives the depth frontier. The final milestones integrate general detectors, resource accounting, necessary assumptions, and attribution into the complete contribution.

The allocation reflects the scientific structure: three prerequisite languages—local estimation, causal circuits, and classical reliability—support a longer argument that combines a universal bound with an explicit attainable protocol. Every milestone is an understanding target for the project, independent of any reader's prior assessment.

## Keep the physical question in view

The sensing state is supplied. The optimized resource is an ideal coherent **readout circuit after sensing**, followed by **one round of independent noisy detection**. A large, even phase-uniform, local Fisher information does not identify which GHZ fringe contains an unknown global phase. The matching geometric construction uses a full cubic grid. These distinctions remain in force throughout the learning route; their mathematical homes are the [model](../science/model.md) and [interpretation](../science/interpretation.md).

[Repository overview](../README.md) · [Milestones](MILESTONES.md) · [Anchor](ANCHOR.md) · [Bridge](BRIDGE.md)
