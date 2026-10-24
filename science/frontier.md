# The finite-size precision–depth frontier

Small readout blocks cannot preserve the parity of an arbitrarily large GHZ probe. They can preserve the parity of a smaller GHZ group, and many such groups contribute information additively. Optimizing that group size gives the precision available between zero-depth local readout and a readout large enough to retain Heisenberg-scale information.

The [construction](construction.md) supplies the exact error and likelihood formulas. The [converse](converse.md) supplies the all-probe upper bounds. This page connects them with explicit integer choices.

## A finite grouping lemma

Suppose $K\ge1$ disjoint readout blocks of size $b\ge1$ are available, covering $N'=Kb$ sensors. Define

```math
q=1-2p,\qquad
c_p=-\log(2\sqrt{p(1-p)}),\qquad
v_*=\min\{3/4,q\}.
```

For the majority error $\epsilon_b$, set

```math
k_b=\max\left\{1,\left\lfloor\frac1{8\epsilon_b}\right\rfloor\right\},
\qquad
r=\min\{K,k_b\}.
```

Partition the $K$ blocks into groups of $r$ blocks and, if needed, a final smaller group. Each group is an independent GHZ probe. No readout gate connects different blocks.

Every group has visibility at least $v_*$. If $\epsilon_b\le1/8$, then $r\epsilon_b\le1/8$, so

```math
(1-2\epsilon_b)^r\ge1-2r\epsilon_b\ge3/4.
```

If $\epsilon_b>1/8$, then $r=1$ and $1-2\epsilon_b\ge q$. The same reasoning applies to the smaller final group.

Since $\epsilon_b\le e^{-c_pb}$ and $\lfloor x\rfloor\ge x/2$ for $x\ge1$,

```math
k_b\ge\frac1{16}e^{c_pb},
\qquad
r\ge\frac1{16}\min\{K,e^{c_pb}\}.
```

For the first inequality when $1/(8\epsilon_b)<1$, use $k_b=1$ and $e^{c_pb}\le1/\epsilon_b<8$. Thus it also covers the short-block regime.

Ignoring only the nonnegative contribution from the smaller final group,

```math
\sum_{\text{groups}}M_g^2
\ge\left\lfloor\frac Kr\right\rfloor(rb)^2
\ge\frac12Krb^2.
```

The two-setting protocol therefore proves the following finite lower bound, for every phase:

```math
\boxed{\quad
F_C(\theta)\ge
\frac{v_*^2}{64}\,
N'\min\{N',b e^{c_pb}\}.
\quad}
```

This is a deliberately conservative bound. It uses neither a divisibility assumption about group size nor an odd-block assumption.

## Full cubic lattices

Let $N=L^D$. For $1\le\ell\le L$, tile the grid with
$K=\lfloor L/\ell\rfloor^D$ complete cubes of side $\ell$. Put $b=\ell^D$ and $N'=Kb$. The uncovered sites are prepared in $Z$ eigenstates and their records are ignored. The active fraction obeys

```math
N'=\ell^D\lfloor L/\ell\rfloor^D\ge2^{-D}N.
```

The readout remains inside each cube. Sensing groups may contain any collection of those cubes, because the input state is supplied before the depth-limited readout.

For an available depth $d$, choose

```math
\ell_d=\min\{L,1+\lfloor d/(2D)\rfloor\},
\qquad b_d=\ell_d^D.
```

The construction uses at most $2D(\ell_d-1)\le d$ two-qubit layers. Applying the grouping lemma and the active-fraction bound twice yields

```math
\mathcal F(N,d)\ge
A_{p,D}N\min\{N,b_d e^{c_pb_d}\},
\qquad
A_{p,D}=\frac{v_*^2}{64\,4^D}.
```

The upper bound is

```math
\mathcal F(N,d)\le
\min\left\{N^2,\,
N(4d+1)^D
\left[(2p)^{-(2d+1)^D}-1\right]\right\}.
```

### Deriving the logarithmic-order statement

Set $\eta=2p$. The upper bound implies

```math
\log(1+\mathcal F/N)
\le\log2+D\log(4d+1)
+\lvert\log\eta\rvert(2d+1)^D
\le B_{p,D}(d+1)^D
```

for a constant $B_{p,D}$, while the ideal ceiling gives
$\log(1+\mathcal F/N)\le\log(1+N)$.

For the lower bound, $0<A_{p,D}\le1$, and concavity gives
$\log(1+Ax)\ge A\log(1+x)$ for $x\ge0$. Consequently,

```math
\log(1+\mathcal F/N)
\ge A_{p,D}
\min\{\log(1+N),c_pb_d\}.
```

The elementary inequalities
$1+\lfloor d/(2D)\rfloor\ge(d+1)/(2D)$ and
$\log(1+N)\le N$ give

```math
\min\{\log(1+N),b_d\}
\ge(2D)^{-D}
\min\{\log(1+N),(d+1)^D\}.
```

Thus, uniformly for every integer $L\ge1,d\ge0$,

```math
a_{p,D}\min\{(d+1)^D,\log(1+N)\}
\le\log(1+\mathcal F/N)
\le B'_{p,D}\min\{(d+1)^D,\log(1+N)\},
```

where, for example,
$a_{p,D}=A_{p,D}\min\lbrace1,c_p\rbrace(2D)^{-D}>0$ suffices. This proves T2.

The constants inside the exponential enhancement are not matched. The sharp statement is the order of its logarithm. At $d=0$, product equatorial probes and two local phase settings give the simpler explicit bound $\mathcal F\ge N(1-2p)^2/2$. At large depth the formula saturates at order $N^2$.

## All-to-all connectivity

For all-to-all two-qubit layers, choose

```math
b_d=\min\{N,2^{\lfloor d/2\rfloor}\},
\qquad
K=\lfloor N/b_d\rfloor,\qquad
N'=Kb_d\ge N/2.
```

Each block requires $2\lceil\log_2b_d\rceil\le d$ two-qubit layers. The grouping lemma and the converse give

```math
\boxed{
A_pN\min\{N,b_d e^{c_pb_d}\}
\le\mathcal F(N,d)
\le\min\{N^2,N4^d[(2p)^{-2^d}-1]\},
\quad A_p=\frac{v_*^2}{256}.
}
```

Consequently, for positive constants depending only on $p$,

```math
a_p\min\{2^{\lfloor d/2\rfloor},\log(1+N)\}
\le\log(1+\mathcal F/N)
\le B_p\min\{2^d,\log(1+N)\}.
```

These bounds determine the order of the Heisenberg-depth threshold. They leave a gap in the leading depth coefficient: a forward causal cone can grow in every layer, while this construction spends separate passes on compression and re-expansion. An exact all-to-all precision frontier at each $d$ is not established.

## Threshold consequences

If a protocol attains $F_C\ge c_0N^2$ for a fixed $c_0>0$, the lattice converse implies
$d=\Omega_{p,D}((\log N)^{1/D})$. The all-to-all converse implies
$d=\Omega_p(\log\log N)$. More explicitly, for fixed $c_0$,

```math
d\ge\log_2\log N-O_{p,c_0}(1)
```

is necessary all-to-all. Indeed, the upper bound forces
$\log N+O(1)\le2d\log2+\lvert\log(2p)\rvert\thinspace2^d$, and the right side is bounded by a $p$-dependent constant times $2^d$.

The [logarithmic-block construction](construction.md#6-logarithmic-blocks-recover-nearly-all-local-information) gives the matching depth orders, and all-to-all uses

```math
d\le2\log_2\log N+O_p(1)
```

to approach the full ideal fraction with the recorded uniform-phase variant. No claim closes this factor-two leading gap.

Two other useful consequences follow directly from the converse:

- At any fixed depth, every probe has $F_C=O(N)$.
- If $d^D=o(\log N)$ on the lattice, or $d=o(\log\log N)$ all-to-all, every probe has $F_C\le N^{1+o(1)}$.

The constructive side identifies why logarithmic block size is enough: a block decision has error exponentially small in its volume, so the accumulated parity error over order $N/b$ blocks stays small. The converse explains why arbitrary input entanglement cannot eliminate that readout requirement.

## What is and is not sharp

| Statement | Status |
|---|---|
| Arbitrary-probe finite support-intersection upper bound | Proved; not asserted optimal for each circuit or detector |
| Lattice order of $\log(1+\mathcal F/N)$ | Matched above and below for full cubic grids |
| Depth order for $\Theta(N^2)$ local information | Matched for full cubic grids and all-to-all connectivity |
| Exact constants, optimal finite-depth circuits, all-to-all leading threshold coefficient | Not fixed by these bounds |
| Preparation cost, gate-noise tolerance, global phase-estimation risk | Separate resource questions |

The finite computations in [verification](../verification/README.md) check circuit schedules, grouping arithmetic and the phase-average formula. The inequalities above are analytical arguments and do not rely on extrapolating those computations.
