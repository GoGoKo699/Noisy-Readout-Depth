# Independent classical detectors beyond symmetric bit flips

The resource law depends on detector overlap and on the possibility of distinguishing repeated outputs. Neither mechanism requires symmetric assignment errors. This page proves the extension for a fixed classical binary-input detector with a finite output alphabet. The use of general detector distributions in metrology is established in [Len et al.](../references/RELATED_WORK.md#len2022); the conclusion here concerns their interaction with circuit depth.

## Detector model and two constants

Write $q_x(y)=P(y\mid x)$ for $x\in\lbrace0,1\rbrace$ and $y$ in a finite alphabet $\mathcal Y$. The corresponding qubit measurement is diagonal:

```math
M_y=q_0(y)\lvert0\rangle\langle0\rvert
+q_1(y)\lvert1\rangle\langle1\rvert.
```

The same detector acts independently on every physical output. The distributions are fixed as $N$ varies. Define

```math
\eta=\sum_y\min\{q_0(y),q_1(y)\},
\qquad
B=\sum_y\sqrt{q_0(y)q_1(y)},
\qquad
\chi=-\log B.
```

Assume $0<\eta<1$. The detector has both a nonzero common part and some ability to distinguish the two bits. Then $0<B<1$ and $\chi>0$: nonzero overlap makes $B>0$, while equality in Cauchy–Schwarz would give $B=1$ only for identical distributions.

For a BSC, $\eta=2p$ and $B=2\sqrt{p(1-p)}$. The converse uses $\eta$ and the constructive rate uses $\chi$. Equal overlap does not imply equal sharp performance for different detectors.

## Exact erasure simulation

Set $r(y)=\min\lbrace q_0(y),q_1(y)\rbrace$ and define normalized distributions

```math
q_{\rm c}(y)=\frac{r(y)}{\eta},
\qquad
\widetilde q_x(y)=\frac{q_x(y)-r(y)}{1-\eta}.
```

Then

```math
q_x(y)=\eta q_{\rm c}(y)+(1-\eta)\widetilde q_x(y).
```

Apply a quantum erasure channel with erasure probability $\eta$. If erased, sample $q_{\rm c}$; if retained, measure the computational bit $x$ and sample $\widetilde q_x$. This parameter-independent classical processing exactly gives the original detector. It is a channel identity, so it holds on entangled inputs as well as basis states.

Apply the simulation independently on all outputs. The entire [support-intersection proof](converse.md) then applies without alteration:

```math
F_C(\theta)\le
\min\left\{N^2,\sum_{i,j}
\left[\eta^{-\lvert C_i\cap C_j\rvert}-1\right]\right\}.
```

This retains the same geometric and all-to-all causal-cone bounds, with $2p$ replaced by $\eta$.

## Repetition decoding with asymmetric errors

Encode a logical bit into the repetition string $x^b$. Given the $b$ detector outputs, compare the likelihoods $q_0^{\otimes b}$ and $q_1^{\otimes b}$ with equal priors. Any fixed tie rule gives equal-prior error

```math
\varepsilon_b=
\frac12\sum_{\mathbf y}
\min\{q_0^{\otimes b}(\mathbf y),
q_1^{\otimes b}(\mathbf y)\}.
```

The conditional errors
$\alpha_b=P(\widehat x=1\mid x=0)$ and
$\beta_b=P(\widehat x=0\mid x=1)$ need not be equal, but
$\varepsilon_b=(\alpha_b+\beta_b)/2$.

Pointwise comparison with the geometric mean proves the finite bound

```math
0<\varepsilon_b\le\frac12 B^b
=\frac12e^{-\chi b}.
```

Also, an optimal test can ignore all but one observation, so
$\varepsilon_b\le\varepsilon_1=\eta/2<1/2$.
For completeness, $\varepsilon_b\ge\eta^b/2>0$, since the minimum of the two product likelihoods is at least the product of their pointwise minima.

### Symmetrize the logical channel

For each block, draw an independent uniform bit $R$, and use one leader $X$ gate before fanout to encode $x=z\oplus R$ instead of the intended bit $z$. Apply the likelihood test to the detector record and report

```math
\widehat z=\widehat x\oplus R.
```

For either value of $z$, averaging over $R$ gives error
$(\alpha_b+\beta_b)/2=\varepsilon_b$. Thus the marginal channel
$z\mapsto\widehat z$ is exactly a BSC. Independent masks and detectors make these logical channels independent across blocks, for **any correlated distribution of the ideal block bits**. That is the condition needed for GHZ parity.

The masks are recorded so they can be undone. After that operation, the parity statistic may omit their labels. Its distribution has the exact BSC form. If the final data also retain the mask labels, that richer record can have more Fisher information; it need not have exactly the same Fisher information as the marginal BSC statistic. The construction uses the latter as a lower bound.

The mask acts after the leader Hadamard and before fanout. Its only function is to relabel the computational-basis bit that the detector sees. The terminal POVM is diagonal, so the argument applies to the coherent block state through its joint basis-outcome distribution.

## The same attained depth orders

For a GHZ group of $M=\sum_j b_j$ sensors, the decoded parity has visibility

```math
v=\prod_j(1-2\varepsilon_{b_j})
```

and exactly the likelihood and Fisher information derived in [the construction](construction.md#3-exact-parity-likelihood-and-information). The recorded two-setting experiment attains $F_C(\theta)\ge M^2v^2/2$ at every phase. A sufficient finite condition is

```math
\sum_j\varepsilon_{b_j}\le\frac18,
```

which gives $v\ge3/4$ and $F_C\ge9M^2/32$. For blocks of size at least $b$ and at most $N$ blocks, $b\ge\log(4N)/\chi$ is one simple sufficient choice when it fits the layout.

The complete [grouping lemma](frontier.md#a-finite-grouping-lemma) applies with

```math
c_p\ \longrightarrow\ \chi,
\qquad
q=1-2p\ \longrightarrow\ 1-\eta,
\qquad
v_*=\min\{3/4,1-\eta\}.
```

Its proof uses only $\varepsilon_b\le e^{-\chi b}$ and
$1-2\varepsilon_b\ge1-\eta$, both established above. Hence the finite lattice lower bound, the logarithmic lattice frontier, and the all-to-all threshold orders all hold, with constants depending on the fixed detector. Logarithmic blocks and the recorded uniform-phase setting again attain $(1-o(1))N^2$ local Fisher information on the layouts specified in the model.

For a fixed finite alphabet, a likelihood decision can be implemented by adding log-likelihood contributions, with direct treatment of zero probabilities. No exponential enumeration of all possible detector strings is required by the construction; enumeration is only used in small verification examples.

## Endpoints and excluded measurement classes

If $\eta=0$, the supports of $q_0,q_1$ are disjoint and the bit can be identified perfectly from one detector output. The positive-noise depth obstruction disappears. If $\eta=1$, the distributions coincide and all terminal records are independent of the input; the accessible information is zero.

The extension proves a statement about diagonal binary-input classical detectors. It does not establish the same law for arbitrary noncommuting qubit POVMs, correlated detectors or collective measurements. Nor are its constants uniform as the detector approaches either endpoint.

[Finite checks](../verification/README.md) enumerate asymmetric ternary and one-sided binary examples, even-block ties, and correlated logical input distributions. They check the exact channel and parity identities rather than replacing the general proof.
