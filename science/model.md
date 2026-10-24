# Model and principal statements

## The physical question

A Greenberger–Horne–Zeilinger (GHZ) probe acquires a phase proportional to the number of sensors. With ideal detection, local measurements can reveal that phase. Independent assignment errors make the parity of many measured bits unreliable, even when the input state and sensing dynamics are perfect. Coherent operations before the terminal measurements can reorganize the information into a form that tolerates those errors.

The local-versus-global control distinction and recovery under unrestricted global readout are established results of [Len et al. (2022)](../references/RELATED_WORK.md#len2022) and [Zhou, Michalakis and Gefen (2023)](../references/RELATED_WORK.md#zhou2023). Here the resource is the **depth of the readout circuit** between those endpoints. The main comparison permits arbitrary input states, so a limitation of one fragile GHZ readout is not mistaken for a limitation of every sensing protocol.

## Sensors, circuit and detector

There are $N$ qubit sensors. An arbitrary parameter-independent state $\rho$ undergoes

```math
\rho_\theta=e^{-i\theta H}\rho e^{i\theta H},
\qquad H=\frac12\sum_{i=1}^{N}Z_i.
```

The parameter $\theta$ is dimensionless; a physical coupling or sensing time can be restored by the chain rule for Fisher information. A parameter-independent unitary $V$ then acts on these same $N$ qubits. Its depth $d$ counts layers of disjoint two-qubit gates. Arbitrary one-qubit gates may occur between layers and do not increase $d$.

Finally, every qubit is measured in the computational basis, and each measured bit is independently flipped with probability $p$. Unless stated otherwise, $0<p<1/2$ is fixed as $N$ grows. There is one terminal detector round. There are no intermediate measurements or extra quantum output systems.

The allowed experiment may draw a classical setting independently of $\theta$, choose the corresponding input and readout, and retain the setting in its record. Its Fisher information is the probability-weighted average of the conditional Fisher informations. Arbitrary classical processing is allowed. In particular, the upper bounds apply to the complete raw detector record before any decoding or estimator is chosen.

The principal model needs no physical ancillas. A mathematical reference used to purify a mixed input does not become an accessible noiseless measurement channel. The [converse](converse.md#ancillas-and-classical-settings) also explains a separately accounted extension when physical ancillas are explicitly included.

## Architectures

**Cubic lattice.** For the matching upper and lower bounds, the sensors occupy every site of an open $D$-dimensional cubic grid of side $L$, with $N=L^D$. Two-qubit gates join nearest neighbors. The dimension $D$ is fixed. The upper bound alone holds for arbitrary occupied subsets of the lattice, and extends with density-dependent constants to bounded qubit density. Matching achievability is not asserted for an arbitrary sparse or disconnected layout.

**All-to-all connectivity.** Any disjoint pairs may interact in a layer. Gates still have two-qubit fan-in: a many-qubit gate is not a single allowed layer.

## The information being bounded

For an outcome record $x$ with probability $P_\theta(x)$, the classical Fisher information is

```math
F_C(\theta)=\sum_{x:P_\theta(x)>0}
\frac{[\partial_\theta P_\theta(x)]^2}{P_\theta(x)}.
```

This is a local measure of sensitivity. The quantum Fisher information (QFI) is the largest classical Fisher information over measurements. Monotonicity under parameter-independent channels gives

```math
F_C(\theta)\le F_Q(\rho_\theta)\le N^2.
```

For a pure unitary family, $F_Q=4\operatorname{Var}(H)$; the spectral width of $H$ is $N$, which proves the last bound, including mixed states by purification. Product equatorial probes have QFI $N$ and GHZ probes have QFI $N^2$. The standard local-estimation definitions are reviewed in [Tóth and Apellaniz](../references/references.bib) and [Paris](../references/references.bib).

With independent repetitions and the usual local regularity and unbiasedness conditions, Fisher information governs the Cramér–Rao lower bound on estimator variance. A large value does not resolve the many identical fringes of a GHZ likelihood. No global phase-risk claim is inferred here.

For a clean phase-uniform frontier, define

```math
\mathcal F(N,d)=
\sup_{\mathcal P:\,\mathrm{depth}(\mathcal P)\le d}
\inf_{\theta\in\mathbb R}F_C(\mathcal P;\theta).
```

The supremum includes the labeled classical settings described above. This optimizes the smallest **local** Fisher information over phase; it is not a minimax estimation error. All upper bounds hold pointwise for every protocol. The lower bounds use a single protocol valid at every phase, so the same scaling also holds for optimization at any chosen operating point.

## Principal results

### T1. The support-intersection converse

Let $C_i$ support $h_i=V(Z_i/2)V^\dagger$, and put $\eta=2p$. The forward circuit light cone is always an admissible choice. For every input state and every phase,

```math
F_C(\theta)\le
\min\left\{N^2,\,
\sum_{i,j=1}^{N}
\left[\eta^{-\lvert C_i\cap C_j\rvert}-1\right]\right\}.
```

If $s=\max_i\lvert C_i\rvert$ and
$\Delta=\max_i\lvert\{j:C_i\cap C_j\ne\varnothing\}\rvert$, then

```math
F_C(\theta)\le
\min\{N^2,N\Delta(\eta^{-s}-1)\}.
```

The proof and its inherited channel-bound machinery are in the [converse](converse.md).

### T2. Geometric precision frontier

For every fixed $p\in(0,1/2)$ and fixed positive integer $D$, there are positive constants depending only on $p,D$ such that, for $N=L^D\ge2$ and every integer $d\ge0$,

```math
\log\left(1+\frac{\mathcal F(N,d)}{N}\right)
=\Theta_{p,D}\!\left(
\min\{(d+1)^D,\log(1+N)\}\right).
```

This notation denotes upper and lower inequalities with uniform constants, not equality of their leading coefficients. An explicit upper bound is

```math
F_C(\theta)\le
\min\left\{N^2,\,
N(4d+1)^D
\left[(2p)^{-(2d+1)^D}-1\right]\right\}.
```

The [frontier proof](frontier.md) gives a finite-size lower bound, including nondivisible block sizes and the $d=0$ endpoint. It follows that Heisenberg-scale information $\mathcal F=\Theta(N^2)$ requires and can be achieved with readout depth

```math
d=\Theta_{p,D}\big((\log N)^{1/D}\big).
```

### T3. All-to-all depth threshold

For all-to-all two-qubit layers,

```math
F_C(\theta)\le
\min\{N^2,N4^d[(2p)^{-2^d}-1]\}.
```

A constructive lower bound has an exponential enhancement in a block size of order $2^{\lfloor d/2\rfloor}$, until the $N^2$ ceiling is reached. Together these establish that the necessary and sufficient order of readout depth for $\Theta(N^2)$ information is

```math
d=\Theta_p(\log\log N).
```

The leading constant in this depth threshold and a matching all-to-all frontier at a fixed depth are **not** determined: the lower and upper bounds contain different exponential functions of $d$. Their exact forms are stated in [the frontier](frontier.md#all-to-all-connectivity).

### T4. Attainment and detector generality

The [construction](construction.md) uses GHZ sensing groups and parallel blocks that compress, rotate and fan out a logical bit. It uses at most $2N$ CNOT gates and no additional qubits. A single large GHZ group, blocks of logarithmic size, and a recorded uniform phase offset give $F_C/N^2\to1$ on full cubic grids and with all-to-all connectivity, at the depth orders above.

For a fixed informative classical binary-input detector with a finite output alphabet, define

```math
\eta=\sum_y\min\{P(y\mid0),P(y\mid1)\}.
```

When $0<\eta<1$, the same converse holds with this $\eta$, and the same depth orders and logarithmic lattice frontier follow from exponential discrimination of repeated detector outputs. [General detectors](detectors.md) proves the statement, including asymmetric error handling.

## Boundaries that affect the result

Independence of the detectors, bounded gate fan-in, and a single terminal measurement round are load-bearing. Readout gates are ideal. Probe preparation, sensing decoherence, physical gate durations and classical computation are outside this particular depth optimization. The [interpretation](interpretation.md) gives counterexamples and resource comparisons that show why these distinctions matter.

The proofs establish a model-specific mathematical contribution. The [related-work comparison](../references/RELATED_WORK.md) attributes the global readout primitive and the purification method, and distinguishes a recent ideal-detector depth transition with the same exponents.
