# The science of noisy readout depth

Entanglement can make a phase change accumulate across many sensors, but this does not ensure that an imperfect apparatus can read the phase out. This project asks how much coherent control is needed **after sensing and before detection** to retain that sensitivity.

The answer has two parts. An upper bound applies to every input state and every allowed readout circuit. A block construction attains the resulting depth orders without additional qubits. The useful resource is the number of outputs reached by an initially local phase generator, together with the overlap between those causal supports.

## Reading route

| Scientific question | Authoritative account |
|---|---|
| What is optimized, and what does the result say? | [Model and principal statements](model.md) |
| Why does independent detector noise limit every probe? | [Causal-support converse](converse.md) |
| How can small readout blocks protect a large sensing phase? | [Block readout construction](construction.md) |
| How much information is available at each depth? | [Finite-size precision frontier](frontier.md) |
| Does the result extend beyond symmetric bit flips? | [General classical detectors](detectors.md) |
| What are the physical meaning and necessary boundaries? | [Interpretation and limits](interpretation.md) |
| Which ingredients are inherited, and which comparison is being made? | [Related work](../references/RELATED_WORK.md) |
| Which finite statements have been checked computationally? | [Verification](../verification/README.md) |

The proofs form a short dependency structure. The detector-to-erasure comparison and an environmental gauge give the support-intersection bound. Circuit causality turns it into architecture-dependent upper bounds. The block construction, its decoding error, and an explicit packing argument give the lower bounds. These meet in the logarithmic-order lattice frontier and the optimal orders of depth for Heisenberg-scale local Fisher information.

Throughout, the physical generator is a sum of single-qubit Pauli operators, detector errors are independent, readout gates are ideal, and only one terminal measurement round is allowed. Preparation cost and global phase identification are separate resources. The [model](model.md) fixes these qualifications before any asymptotic statement.
