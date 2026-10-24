# Physical meaning, resources and limits

## A sensing state and a readable record are different resources

Under the additive generator $H=\sum_iZ_i/2$, a GHZ probe acquires a relative phase $N\theta$. Ideal local $X$ measurements reveal this through the parity of the outcomes. The measurement need not be collective when the detectors are perfect.

For independent BSC detectors, raw parity has visibility

```math
v_{\rm raw}=(1-2p)^N.
```

Its quadrature Fisher information is $N^2(1-2p)^{2N}$, exponentially small at fixed $p>0$. This example explains the difficulty but does not prove an all-probe limitation. Other states can do much better than this fragile raw-parity protocol. The [converse](converse.md) supplies the state-independent statement: **every fixed-depth readout has at most extensive information** in the specified model.

## What the converse measures

After readout, the initially local generator $Z_i/2$ has support $C_i$. In the erasure comparison, an environment sometimes receives that whole support. Probability-reweighting those events produces an unbiased environmental representation of the generator. The residual fluctuation bounds the information that can remain with the receiver.

Independent erasures make residuals on disjoint supports cancel in the covariance. Only intersecting supports contribute:

```math
\mathbb E[(1-a_i)(1-a_j)]
=\eta^{-\lvert C_i\cap C_j\rvert}-1.
```

Circuit depth limits both the size of each support and how many other supports it can meet. This is why the bound constrains arbitrary input entanglement rather than one chosen state.

This information-leakage interpretation uses established environmental and channel-bound ideas; [the provenance](../references/RELATED_WORK.md#zhou2021) is part of the scientific account. The explicit circuit specialization, rather than a new general complementarity principle, produces the resource law here.

## Why the block construction reaches the threshold

There are two different sizes in the construction. A GHZ **sensing group** of $M$ qubits supplies phase $M\theta$. A **readout block** of $b$ qubits protects one logical measurement bit. Compression keeps the group phase on the block leaders; re-expansion makes each leader's bit redundant.

The block decision error decreases exponentially in $b$. Parity over about $M/b$ blocks remains reliable when their total error is small. Thus a block volume of order $\log M$ is enough. Filling that volume takes depth of order $(\log M)^{1/D}$ on a full grid or $\log\log M$ with all-to-all pairings.

At smaller depth, the optimal strategy in the proof uses many smaller GHZ groups rather than one global group. Their informations add. This produces the lattice frontier: the logarithm of the enhancement over $N$ grows proportionally, up to constants, to the available readout volume until it reaches the $N^2$ ceiling.

The construction does not restore an arbitrary unknown quantum state after detector noise. It protects the classical information needed for one phase-sensitive observable. That narrower task is sufficient for the attained Fisher information.

## Resource accounting

| Resource | Accounting in this project |
|---|---|
| Sensing qubits | $N$; inactive leftovers are put in $Z$ eigenstates |
| Signal | One parallel encoding by $\sum_iZ_i/2$ |
| Input state | Arbitrary supplied state; construction uses independent GHZ groups |
| Coherent readout | Ideal parameter-independent two-qubit gates; disjoint layers define $d$ |
| One-qubit gates | Allowed between layers; bounded extra local layers suffice in the construction |
| Added qubits | None required for attainment |
| Readout CNOT count | Exactly $2(N'-K)$ for $K$ active blocks covering $N'$ qubits |
| Detectors | One terminal independent detector use per physical qubit |
| Classical work | Linear majority/parity work; finite-alphabet likelihood processing is also linear in the number of outputs |
| Random choices | Recorded phase settings; general asymmetric detectors also use independent block complements |
| Optimized performance | Per-shot local classical Fisher information |

### Preparation remains a separate cost

The group state can be entangled across many readout blocks before the signal is applied. The readout circuit never creates that initial entanglement. Starting from product qubits under the same unitary gate restrictions, a global GHZ state on a full grid has preparation depth of order $L=N^{1/D}$; an all-to-all fanout prepares it in order $\log N$ layers.

The lower order follows from causality: distant GHZ qubits have nonzero correlations, whereas observables with disjoint backward cones on a product input have factorized expectations. On a grid this forces a depth proportional to the diameter. All-to-all, pairwise intersection of the backward cones for $N$ outputs requires an exponentially growing cone, giving an order-$\log N$ lower bound. The standard fanout schedules give matching orders.

Consequently the smaller terminal readout depth proved here does not imply the same improvement in total sensing-cycle depth. Preparation, storage lifetime and the sensing dynamics must be included in an application-specific comparison.

## Assumptions with concrete failure modes

### Correlated detector noise can preserve parity

Let $N$ be even and divide the measured bits into pairs. Independently for each pair, flip **both** bits with probability $p$. Each individual detector has marginal error $p$, yet every error flips an even number of bits. Total parity is unchanged.

Local $X$ readout of a GHZ state then retains ideal parity information with zero entangling depth. Therefore fixed single-detector error rates do not imply the converse without the stated independence or an appropriate independent-erasure degradation. This counterexample concerns correlations between detector errors, not correlations of the input state, which the theorem permits.

### Repeated QND readout trades depth for measurement rounds

Suppose, outside the present model, each computational bit can be measured repeatedly without changing it, with independent assignment errors on successive rounds. Apply local Hadamards to a GHZ probe, repeat each detector measurement $r$ times, and majority-decode each bit. With $r=O(\log N)$, the total probability of a wrongly decoded parity can be kept small.

This uses zero entangling depth after sensing, but order $\log N$ measurement rounds and order $N\log N$ detector uses. The single-terminal-round condition is therefore substantive. A joint tradeoff between coherent depth and measurement rounds would need a different theorem.

### Gate and sensing noise are not corrected by this result

For a concrete example, apply independent phase flips of probability $\gamma\in(0,1/2)$ to a GHZ state before readout. Its off-diagonal coherence is multiplied by
$\kappa=(1-2\gamma)^N$. The state's QFI is then

```math
F_Q=N^2\kappa^2=N^2(1-2\gamma)^{2N}.
```

This follows by viewing the state as an equatorial two-level Bloch vector of length $\kappa$ rotating at frequency $N$. Any later parameter-independent readout is bounded by that QFI. Thus the present decoder does not repair this fixed pre-readout dephasing. It is not a fault-tolerant sensing or noisy-gate theorem.

### Detector parameters must be fixed in the asymptotic law

The explicit finite bounds retain their $p$ dependence. The stated scaling laws hold with fixed $p\in(0,1/2)$, and their constants are not uniform near the endpoints.

At $p=0$, local GHZ readout already suffices. If $p=p_N$ decreases with size and $Np_N$ remains bounded, raw parity can retain a nonzero fraction of ideal quadrature information, since $(1-2p_N)^{2N}$ need not vanish. At $p=1/2$, every reported bit is independent of the ideal bit and no terminal information remains.

### Local sensitivity does not remove phase aliases

For a GHZ group of size $M$, even the phase-labeled record is periodic under
$\theta\mapsto\theta+2\pi/M$. The two-setting construction prevents vanishing slopes; the continuous setting makes the local information phase independent. Neither distinguishes these identical fringes.

A global estimation guarantee would need additional scale information, a prior restriction or a multiscale sensing design, together with its full resource accounting. No such guarantee is asserted here.

### Geometry and ancillary systems must be counted

The geometric lower construction uses full cubes. A collection of isolated qubits placed in a $D$-dimensional space need not support it. Conversely, unlimited qubit density or unbounded-fan-in gates can violate the causal-volume estimates. Measured physical ancillas may be analyzed by the extended converse only when their detectors and density are included; no free accessible noiseless quantum output is present in the main model.

## Scientific scope of the comparison

The [related-work account](../references/RELATED_WORK.md) distinguishes the contribution from product-local/global noisy-readout endpoints, the established global GHZ decoder, and ideal-detector readout-depth transitions with the same asymptotic exponents. The project does not claim to introduce purification bounds, repetition decoding, or the first relation between circuit depth and observability.

The central result is the explicit arbitrary-probe ceiling under independent terminal detector noise, together with matching lattice logarithmic enhancement and matched threshold orders. Its constants are conservative, the all-to-all leading coefficient remains open, and the finite checks do not certify publication priority or replace the proofs.
