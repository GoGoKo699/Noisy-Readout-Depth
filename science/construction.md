# Block readout that preserves a large sensing phase

The construction separates the size of a sensing group from the size of its coherent readout blocks. A sensing group can accumulate a phase proportional to all its qubits, while only small blocks need to interact during readout.

The compress–Hadamard–fanout primitive and majority decoding are inherited from [Zhou, Michalakis and Gefen, Sec. VII.C and Appendix H](../references/RELATED_WORK.md#zhou2023). The organization used here applies that primitive to many blocks and retains the parity between their decoded logical bits.

## 1. Compress each block without losing the group phase

Take $M=kb$ sensors partitioned into $k$ blocks of size $b$. Prepare a GHZ state across the whole sensing group. After the signal is encoded, and after an optional known local phase rotation, it is

```math
\lvert\psi_\theta\rangle=
\frac{\lvert0^M\rangle+
e^{i(M\theta+\phi)}\lvert1^M\rangle}{\sqrt2}.
```

In every block, choose a CNOT fanout circuit $U_b$ satisfying

```math
U_b\big(\lvert x\rangle\otimes\lvert0^{b-1}\rangle\big)
=\lvert x^b\rangle,\qquad x\in\{0,1\}.
```

The readout applies $U_b^\dagger$, then a Hadamard to the leader, then $U_b$, in parallel across blocks. Compression leaves the $k$ leaders in a GHZ state with the **original phase $M\theta$**, and returns the other sensors to $\lvert0\rangle$. Those same qubits serve as the repetition register during fanout. No fresh ancillas are required.

The Hadamards transform phase into a distribution over leader bits $z=(z_1,\ldots,z_k)$:

```math
\Pr_\theta(z)=2^{-k}
\left[1+(-1)^{z_1+\cdots+z_k}
\cos(M\theta+\phi)\right].
```

Fanout replaces each computational-basis bit $z_j$ by a block string $z_j^b$. This is a unitary repetition encoding of basis labels, not cloning an arbitrary unknown qubit. Before detector noise, the parity of the block labels has expectation $\cos(M\theta+\phi)$.

## 2. Majority decoding for every block size

Each of the $b$ physical outcomes in a block is independently flipped with probability $p$. Majority decoding, with an independent fair coin for an even-size tie, produces a binary symmetric logical error with probability

```math
\epsilon_b=
\sum_{r>b/2}\binom{b}{r}p^r(1-p)^{b-r}
+\frac{\mathbf1_{\{b\ {\rm even}\}}}{2}
\binom{b}{b/2}p^{b/2}(1-p)^{b/2}.
```

The tie term is present only for even $b$. The error is independent of the input logical bit. Distinct blocks have independent errors even though their ideal bits are correlated.

Let

```math
q=1-2p>0,\qquad
c_p=-\log\!\left(2\sqrt{p(1-p)}\right)>0.
```

Equal-prior maximum-likelihood testing gives majority with fair ties. Ignoring all but one outcome is an available test, so

```math
0<\epsilon_b\le p<\frac12.
```

For the two repeated detector distributions $P_0^{\otimes b},P_1^{\otimes b}$, the equal-prior error is half the sum of their pointwise minimum. Since $\min(a,b)\le\sqrt{ab}$,

```math
\epsilon_b
\le\frac12
\left(\sum_y\sqrt{P_0(y)P_1(y)}\right)^b
=\frac12e^{-c_pb}
\le e^{-c_pb}.
```

The weaker final inequality suffices for all constants in the [finite-size frontier](frontier.md).

## 3. Exact parity likelihood and information

After logical decoding, the parity $Y\in\lbrace+1,-1\rbrace$ has distribution

```math
\Pr_\theta(Y=y\mid\phi)
=\frac{1+yv\cos(M\theta+\phi)}2,
\qquad
v=(1-2\epsilon_b)^k.
```

Thus the Fisher information of this statistic is exactly

```math
F_\phi(\theta)=
M^2\frac{v^2\sin^2(M\theta+\phi)}
{1-v^2\cos^2(M\theta+\phi)}.
```

The complete raw detector record can have more information; this formula is an attained lower bound for that record. Since $0<v<1$, its denominator is strictly positive. At a calibrated quadrature, $M\theta+\phi=\pi/2$ modulo $\pi$,

```math
F_\phi=M^2v^2.
```

For unequal blocks of sizes $b_1,\ldots,b_k$, the same argument gives $M=\sum_j b_j$ and $v=\prod_j(1-2\epsilon_{b_j})$. Equal-size complete blocks are used below to make circuit depth and finite packing explicit.

## 4. A fixed experiment with sensitivity at every phase

A single parity setting has zero slope at some phases. This is addressed within the allowed readout model by retaining a random setting label.

### Two settings

Choose $\phi=0$ or $\pi/2$ with equal probability. One local $Z$ rotation in each sensing group supplies the relative phase; it requires no two-qubit layer. Retaining the chosen setting gives

```math
\begin{aligned}
F_{\rm two}(\theta)
&=\frac12F_0(\theta)+\frac12F_{\pi/2}(\theta)\\
&\ge\frac12M^2v^2.
\end{aligned}
```

To see the inequality, bound each denominator by one and add the sine-squared and cosine-squared numerators. The same two settings may be shared across all independent GHZ groups: conditioned on the setting, Fisher information adds across groups, and the subsequent average preserves the bound.

If $\sum_j\epsilon_{b_j}\le1/8$, the elementary product inequality yields

```math
v\ge1-2\sum_j\epsilon_{b_j}\ge\frac34,
\qquad
F_{\rm two}(\theta)\ge\frac9{32}M^2.
```

This finite condition is sufficient, not necessary.

### Uniformly random phase

The ideal control model also permits a recorded phase $\phi$ uniformly distributed on $[0,2\pi)$. Then

```math
F_{\rm uniform}(\theta)
=\frac1{2\pi}\int_0^{2\pi}F_\phi(\theta)\,d\phi
=M^2\left(1-\sqrt{1-v^2}\right).
```

The value is independent of $\theta$. For the integral, write

```math
\frac{v^2\sin^2x}{1-v^2\cos^2x}
=1-\frac{1-v^2}{1-v^2\cos^2x},
\qquad
\frac1{2\pi}\int_0^{2\pi}
\frac{dx}{1-v^2\cos^2x}
=\frac1{\sqrt{1-v^2}}.
```

Thus $v\to1$ recovers the full ideal information fraction uniformly over phase. This refinement allows a continuum of ideal local phase settings. The two fixed settings already suffice for every order-of-growth theorem.

Retaining the phase label is essential. Averaging the probability distribution over $\phi$ and discarding the label would remove the signal. Also, both versions retain the GHZ likelihood's period $2\pi/M$ in $\theta$; uniform local information does not resolve global aliases.

## 5. Depth and gate count

### A cubic readout block

For a cube of side $\ell$ and size $b=\ell^D$, place the leader at a corner. First fan out along one coordinate direction. Then fan out along parallel lines in the next direction, and continue through the $D$ directions. Each direction takes $\ell-1$ layers. Gates in a layer act on disjoint pairs, and each pair consists of neighboring sites.

This uses $b-1$ CNOT gates and at most $D(\ell-1)$ two-qubit layers. Reversing the circuit compresses the block. Compression plus re-expansion therefore costs

```math
d_b\le2D(\ell-1),\qquad
G_b=2(b-1).
```

All blocks execute the same schedule in parallel. The known phase rotations and leader Hadamards are local gates. Counting every gate layer instead of just two-qubit layers adds only a bounded number of layers.

### All-to-all connectivity

Start with one leader. At each fanout layer, every already reached qubit can control a CNOT into a distinct unreached qubit. This doubles the reached population until the block is filled. For every integer $b$,

```math
d_b\le2\lceil\log_2b\rceil,\qquad
G_b=2(b-1).
```

For $K$ blocks covering $N'=Kb$ active sensors, the total number of readout CNOT gates is exactly $2(N'-K)\le2N$. Majority and parity evaluation take linear classical work in the BSC case. This is an accounting of readout; preparing the GHZ groups is a separate operation.

## 6. Logarithmic blocks recover nearly all local information

On a full cubic grid, choose

```math
\ell=\left\lceil(A\log N)^{1/D}\right\rceil,\qquad
b=\ell^D,\qquad A>1/c_p.
```

For sufficiently large $N$, $\ell\le L$. Use the $K=\lfloor L/\ell\rfloor^D$ complete blocks, with $N'=Kb$ active sensors, in one GHZ group. Leave uncovered sensors in $Z$ eigenstates. Then

```math
\frac{N'}N\longrightarrow1,\qquad
K\epsilon_b\le\frac Nb\,N^{-Ac_p}\longrightarrow0.
```

Hence $v\to1$. The quadrature information and the uniformly randomized-phase information both equal $(1-o(1))N^2$. The required depth is $O((\log N)^{1/D})$.

With all-to-all connectivity, use $b=\lceil A\log N\rceil$ and $K=\lfloor N/b\rfloor$. Again $N'/N\to1$ and $v\to1$, now with depth $O(\log\log N)$. Together with the [converse](converse.md), this establishes the optimal threshold orders. The [frontier](frontier.md) treats every finite depth, including blocks too small to protect one global GHZ group.
