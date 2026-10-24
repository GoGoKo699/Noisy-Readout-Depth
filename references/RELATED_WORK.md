# Related work and attribution

This project concerns a particular resource question: how the depth of an ideal coherent readout circuit limits the local Fisher information obtainable from arbitrary probes when every output is measured once through an independent imperfect detector. The sensing generator is $H=\frac12\sum_i Z_i$. Preparation depth, noise during sensing, and global phase identification are separate questions, as specified in the [model](../science/model.md).

The contribution combines a causal-support information bound with a block construction attaining its depth orders. The underlying metrological methods and the basic decoder are established. This page identifies those dependencies and distinguishes the closest results. Full bibliographic records are in [references.bib](references.bib).

## len2022

**Yink Loong Len, Tuvia Gefen, Alex Retzker, and Jan Kołodyński, “Quantum metrology with imperfect measurements,” Nature Communications 13, 6971 (2022).** [Published article](https://doi.org/10.1038/s41467-022-33563-8) · [Author manuscript](https://arxiv.org/html/2109.01160v2).

Sections II.3.1–II.3.2 establish the central distinction between local and global control under readout imperfections. Their local-control class consists of products of single-probe unitaries. Corollary 2 and Eq. (23) give an $O(N)$ optimized information ceiling for nontrivial detector noise in that class. Global controls recover ideal asymptotic sensitivity. Their Discussion explicitly raises the complexity of such control as a further question.

These endpoints are inherited here. The [converse](../science/converse.md) addresses the intervening class of overlapping, finite-depth circuits. A noisy product measurement generally cannot be commuted through an arbitrary entangling decoder and treated as independent encoding noise. The erasure comparison avoids that reduction. General detector overlap also appears in the earlier work; the added question is its interaction with readout depth.

## zhou2023

**Sisi Zhou, Spyridon Michalakis, and Tuvia Gefen, “Optimal Protocols for Quantum Metrology with Noisy Measurements,” PRX Quantum 4, 040305 (2023).** [Published article](https://doi.org/10.1103/PRXQuantum.4.040305) · [Author manuscript, v3](https://arxiv.org/pdf/2210.11393v3).

Section VII.C, Fig. 3(a), and Appendix H explicitly give GHZ compression to one leader, a Hadamard, and fanout before majority decoding. Appendix H.2 implements the operation with $O(N)$ two-qubit gates and $O(\log N)$ all-to-all depth. Their phase convention gives GHZ QFI $4N^2$; the generator used here gives $N^2$.

The [block construction](../science/construction.md) uses that inherited primitive independently within small blocks. Their logical outcomes retain the original sensing phase in a parity correlation. Protecting each block outcome to error inverse-polynomial in $N$ needs logarithmic block volume. This organization reduces all-to-all readout depth to $O(\log\log N)$ and yields the lattice construction. The associated arbitrary-probe converse and finite-depth frontier are separate from the older global decoder's optimality statement.

## zhou2021

**Sisi Zhou, Zi-Wen Liu, and Liang Jiang, “New perspectives on covariant quantum error correction,” Quantum 5, 521 (2021).** [Published article](https://doi.org/10.22331/q-2021-08-09-521) · [Author manuscript, v3](https://arxiv.org/pdf/2005.11918v3).

Appendix C, Eqs. (94)–(97), supplies the closest general variational formula behind the converse: branch-diagonal Kraus gauges for noise on subsets and commuting subset-supported Hamiltonian terms. The support-intersection bound here is an explicit specialization of that established machinery.

Let $E$ be an independent-erasure pattern of probability $w_E$, let $h_i=VZ_iV^\dagger/2$ have support $C_i$, and set

$$
A_E=\sum_i\frac{\mathbf1\{C_i\subseteq E\}}{\eta^{|C_i|}}h_i.
$$

Then $\sum_Ew_EA_E=H'=VHV^\dagger$. Choosing the older formula's branch Hamiltonian as $H_E=w_EA_E$ gives the gauge operator $\sum_Ew_EA_E^2-(H')^2$. Its explicit evaluation is

$$
\sum_{i,j}\bigl[\eta^{-|C_i\cap C_j|}-1\bigr]h_i h_j.
$$

Disjoint supports cancel. This evaluation, followed by circuit-causality bounds and the matching construction, produces the resource law. It does not constitute a new general purification framework. The [self-contained proof](../science/converse.md) retains the negative $(H')^2$ term; discarding it before evaluating the independent-erasure average would lose the useful cancellation.

## du2026

**Zhenyu Du, Siyuan Cheng, Han Ye, Junjie Chen, Xiao Yuan, and Xiongfeng Ma, “Complexity-driven transitions in quantum observation,” arXiv:2606.09765v1 (2026).** [Preprint](https://arxiv.org/abs/2606.09765v1) · [Full author upload](https://www.researchgate.net/publication/406464293_Complexity-driven_transitions_in_quantum_observation).

Theorem 1 establishes the same depth orders, $\Theta((\log N)^{1/D})$ on a $D$-dimensional architecture and $\Theta(\log\log N)$ with all-to-all connectivity. Its final computational-basis measurement is ideal. Below threshold there exists a smooth pure-state encoding with QFI one whose information is inaccessible to every allowed shallow readout. Above threshold a randomized readout extracts a constant QFI fraction for every smooth pure-state encoding.

The quantifiers differ here. For the fixed additive sensing generator and independent detector noise, the upper bound applies to **every probe state**. The construction optimizes sensitivity using a specific family of probes, rather than guaranteeing universal readout of every encoding. With ideal detectors, GHZ already yields $N^2$ FI using local Hadamards, so the older worst-case obstruction does not imply the noisy-detector ceiling. The shared exponents and the general relationship between readout and depth are therefore not claimed as new discoveries.

## Established proof methods

Purification and Kraus-representation bounds are developed by [Escher, de Matos Filho, and Davidovich (2011)](https://doi.org/10.1038/nphys1958), [Escher et al. (2012)](https://doi.org/10.1103/PhysRevLett.109.190404), and [Demkowicz-Dobrzański, Kołodyński, and Guţă (2012)](https://doi.org/10.1038/ncomms2067). They provide the general route from a noise model to state-independent precision limits.

[Faist et al. (2020)](https://doi.org/10.1103/PhysRevX.10.041018), Theorem 2 and Appendix A, allow overlapping charge terms supported on erasable subsets and construct a probability-reweighted environmental charge observable to bound code recovery fidelity. [Faist et al. (2023)](https://doi.org/10.1103/PRXQuantum.4.040336) further relate metrological information loss to complementary information accessible to the environment. These works establish the broader information-leakage interpretation. The calculation here uses that perspective for terminal detector noise and circuit-supported signal generators.

## General reviews

These reviews supply background rather than the detector-depth theorem. They are distinct from the primary-source dependencies above.

| Review | Useful sections in the linked version |
|---|---|
| [Tóth and Apellaniz (2014), arXiv:1405.4878v4](https://arxiv.org/pdf/1405.4878v4) | §2.2: GHZ sensing; §§4.1–4.3: FI, QFI, and optimal measurement; §5.1: entanglement; §6: noise. |
| [Paris (2009), arXiv:0804.2981v3](https://arxiv.org/pdf/0804.2981v3) | §§2–4: local estimation, estimability, pure states, and unitary families. |
| [Demkowicz-Dobrzański, Jarzyna, and Kołodyński (2015), arXiv:1405.7703v3](https://arxiv.org/pdf/1405.7703v3) | §IV.A–B: classical and quantum estimation; §V.A: ideal limits; §VI.B: QFI bounds under noise. |

## Scope of the comparison

This comparison uses the stated models and results of the identified sources. It supports distinguishing this detector-noise frontier from those specific results; it does not certify exhaustive publication priority. In particular, neither an established method used in a new calculation nor a familiar exponent alone establishes the significance of the complete theorem. The mathematical claims should be assessed through their assumptions, proofs, attainable protocols, and resource accounting in [science/](../science/README.md).
