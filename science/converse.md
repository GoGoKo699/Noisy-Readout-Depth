# A converse from erased causal supports

This page proves T1 in the [model](model.md). The argument bounds the complete measurement record for every input state. Its key quantity is the intersection of the supports of the phase generators after the readout circuit.

The underlying use of purification and environmental unitary freedom is established quantum-metrology machinery. In particular, branch-dependent gauges for noise on overlapping subsets appear in [Zhou, Liu and Jiang, Appendix C](../references/RELATED_WORK.md#zhou2021). The specific calculation here chooses a gauge adapted to independent erasures and evaluates its covariance by support intersections.

## 1. An informative channel above the noisy detector

Let $\eta=2p$. Replace each final noisy detector, for the purpose of an upper bound, by a quantum erasure channel:

```math
\mathcal E_\eta(\sigma)
=(1-\eta)\sigma\oplus
\eta\,\operatorname{Tr}(\sigma)\lvert e\rangle\langle e\rvert.
```

The receiver can tell whether the output was erased. Measure a retained qubit ideally in the computational basis; replace an erased output by a fresh fair bit; then discard the flag. The resulting classical bit is flipped with probability $\eta/2=p$. Applying this rule independently to every output exactly reproduces the original detector channel, even for entangled inputs.

Consequently,

```math
F_C(\theta)\le
F_Q\!\left[
\mathcal E_\eta^{\otimes N}
\left(V\rho_\theta V^\dagger\right)\right].
```

No physical erasure detector is assumed available in the construction. It is a stronger hypothetical receiver used only to upper-bound the actual apparatus.

Write

```math
\sigma_\theta=V\rho_\theta V^\dagger
=e^{-i\theta H'}\sigma e^{i\theta H'},
\qquad
H'=\sum_i h_i,\quad h_i=V(Z_i/2)V^\dagger.
```

The $h_i$ commute, each has operator norm $1/2$, and $C_i$ is any support containing $h_i$. Using a larger causal support can weaken the bound but cannot invalidate it.

## 2. A legitimate environmental gauge

Purify $\sigma_\theta$ with an inaccessible mathematical reference $R$. An erasure dilation has branches indexed by the erased set $E\subseteq\{1,\ldots,N\}$, with probability

```math
w_E=\eta^{\lvert E\rvert}(1-\eta)^{N-\lvert E\rvert}.
```

Let $T_E$ move the qubits in $E$ to the environment and the other qubits to the receiver. Include orthogonal copies of the erasure-set flag on both sides. Tracing the environment gives the flagged erasure channel. The reference $R$ is also traced when obtaining the physical receiver state.

For each generator define

```math
a_i(E)=\frac{\mathbf1_{\{C_i\subseteq E\}}}{\eta^{\lvert C_i\rvert}},
\qquad
A_E=\sum_i a_i(E)h_i.
```

Whenever a term appears in $A_E$, its entire support is in the erased subsystem. Thus $A_E$ is an actual operator on the environment of branch $E$. Overlap between supports causes no obstruction: sums of operators supported on $E$ still act on $E$.

Fix a parameter point $\theta_0$. Applying the environmental unitary
$\exp[i(\theta-\theta_0)A_E]$, controlled on the erasure flag, changes a purification but leaves the receiver state unchanged. At $\theta_0$, the derivative of this purification is

```math
-i\sum_E\sqrt{w_E}\,T_EK_E
\lvert\psi_{\theta_0}\rangle,
\qquad
K_E=H'-A_E=\sum_i[1-a_i(E)]h_i.
```

The environmental operator intertwines through $T_E$ with the same operator on the erased input factors. This justifies the derivative expression. The gauge is a proof choice local to $\theta_0$, not a parameter-dependent operation performed by the experimenter.

Independence of erasures gives $\mathbb E_E[a_i]=1$. Therefore

```math
\sum_Ew_EK_E=0.
```

The overlap of the chosen purification with its derivative is zero. The pure-state QFI formula and monotonicity under partial trace then imply

```math
F_C(\theta_0)
\le 4\left\langle\psi_{\theta_0}\left|
\sum_Ew_EK_E^2
\right|\psi_{\theta_0}\right\rangle
\le4\left\|\sum_Ew_EK_E^2\right\|.
```

This holds for an arbitrary mixed input because its purification was arbitrary.

## 3. Evaluate the covariance

For any pair of supports,

```math
\begin{aligned}
\mathbb E_E[a_i a_j]
&=\frac{\Pr(C_i\cup C_j\subseteq E)}
{\eta^{\lvert C_i\rvert+\lvert C_j\rvert}}\\
&=\eta^{-\lvert C_i\cap C_j\rvert}.
\end{aligned}
```

It follows that

```math
c_{ij}:=\mathbb E_E[(1-a_i)(1-a_j)]
=\eta^{-\lvert C_i\cap C_j\rvert}-1,
\qquad
\sum_Ew_EK_E^2=\sum_{i,j}c_{ij}h_ih_j.
```

All coefficients are nonnegative. Disjoint supports contribute exactly zero; this cancellation is the source of the extensive, rather than automatically quadratic, bound at fixed depth. Since $\|h_ih_j\|\le1/4$,

```math
F_C(\theta)\le\sum_{i,j}
\left[\eta^{-\lvert C_i\cap C_j\rvert}-1\right].
```

The operator-norm step can in fact be an equality: the common eigenvector $V\lvert0^N\rangle$ has $h_i=+1/2$ for every $i$. This observation concerns this chosen gauge's norm only; it does not show that any probe attains the resulting channel-information bound.

There are at most $N\Delta$ ordered pairs with overlapping supports, and every intersection has size at most $s$. Hence

```math
F_C(\theta)\le N\Delta(\eta^{-s}-1).
```

Taking the minimum with the ideal bound $N^2$ completes T1.

## 4. Circuit causality

### Cubic lattice

Under nearest-neighbor layers, $C_i$ is contained in the lattice ball of graph radius $d$ about input site $i$. An enclosing cube gives

```math
s\le(2d+1)^D.
```

If $C_i$ intersects $C_j$, the sites $i,j$ are at graph distance at most $2d$. A second enclosing cube gives

```math
\Delta\le(4d+1)^D.
```

Open boundaries only reduce these counts. This proves the geometric bound in T2. If each site has a fixed bounded number of physical qubits, the same argument introduces density factors; an unbounded number of qubits at a site does not obey the stated one-qubit-per-site constants.

### All-to-all layers

A two-qubit layer can at most double a forward causal cone, so $s\le2^d$. Likewise, an output qubit has at most $2^d$ input qubits in its backward causal cone. A fixed support $C_i$ can therefore intersect the supports of at most

```math
\lvert C_i\rvert\,2^d\le4^d
```

input generators. Counting a generator more than once only enlarges this upper bound. This proves T3's converse.

## Ancillas and classical settings

The principal model has exactly $N$ sensing and measured qubits. If one explicitly includes parameter-independent physical ancillas, the same proof works with erasures over **all physical output qubits**, while the sum over $i$ still ranges only over sensing generators. Every physical output available to the experimenter must have its specified noisy detector. Geometric density must count those ancillas as well. The proof does not supply free noiseless quantum outputs or unbounded density.

For a labeled, parameter-independent random setting, Fisher information is the average of the conditional values, so a common bound applies. Classical data processing can only decrease Fisher information. If a protocol postselects, its success probability and success/failure flag are part of the accounting.

For sequential repetitions whose choices depend on earlier classical records, the score chain rule makes the total Fisher information a sum of conditional per-shot informations. The per-shot bound still applies when the depth and detector assumptions hold on every shot. This is not a claim about a joint coherent decoder across several stored sensing runs; that would be a different physical circuit.

## What the calculation establishes

The proof never moves detector noise through $V$ or assumes that the input is a product state. It replaces the detector by a more informative erasure channel, then uses a valid environmental gauge. The exact support covariance is proved analytically. [Finite verification](../verification/README.md) checks that covariance by enumeration and checks the information inequalities on small explicit circuits.
