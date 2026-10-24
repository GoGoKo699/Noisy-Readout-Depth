# Thirty milestones for Noisy Readout Depth

This map follows one scientific question: how much coherent readout is needed to turn an entangled sensor's phase sensitivity into a reliable classical record? It specifies understanding targets for any reader. The exact definitions, proofs and constructions remain in the linked [scientific account](../science/README.md).

The single educational anchor is Géza Tóth and Iagoba Apellaniz, *Quantum metrology from a quantum information science perspective*, Journal of Physics A **47**, 424006 (2014), [arXiv:1405.4878v4](https://arxiv.org/abs/1405.4878v4). Section and equation numbers below refer to that version; the [anchor guide](ANCHOR.md) gives the reading selection and notation translation. “Anchor” identifies supporting foundations; it does not attribute this project's detector-depth theorem to the review. The [source bridge](BRIDGE.md) supplies the additional circuit, probability and environmental-gauge steps.

## Organization

| Phase | Milestones | Scientific progression |
|---|---|---|
| Background and preliminaries | [M01–M12](#m01) | One qubit and one outcome distribution; local information and entanglement; noise, classical reliability and circuit causality; the complete resource question. |
| Narrative and innovation | [M13–M30](#m13) | Local ingredients of the converse and decoder; their assembly into finite bounds and depth laws; detector generality, resource boundaries and the full contribution. |

The **12/18 allocation** reflects the project's three prerequisites: local quantum estimation, the causal reach of a circuit, and the reliability of repeated classical outcomes. The second phase develops both proof and construction components before combining them into architecture-dependent results. Its final milestones integrate the detector class, physical limitations and attribution. The map covers the project's conceptual structure without requiring every technical lemma or neighboring subject.

Dependencies refer only to earlier milestones. A dependency identifies an idea used by the target; it does not replace the explanation in the scientific source.

## Phase I: Background and preliminaries

### M01

**A phase carried by one qubit**

- **Central question:** What does the unknown parameter change before any measurement is made?
- **Understanding target:** Explain how the generator $Z/2$ changes the relative phase of a qubit superposition, and why a computational-basis probability can remain unchanged until a suitable readout rotation is applied.
- **Dependencies and story role:** None. Establish the individual sensor, the dimensionless phase and the separation between encoding and readout.
- **Conceptual connection:** A parameter can be present in a quantum state without being visible in a particular outcome distribution.
- **Source pointers:** Anchor §2, Eqs. (3), (5)–(8), and §4.2, Eq. (54); [sensors, circuit and detector](../science/model.md#sensors-circuit-and-detector).

### M02

**A probability distribution as a measuring instrument**

- **Central question:** How does a detector record reveal a small change in phase?
- **Understanding target:** Read a phase-dependent binary likelihood and distinguish outcome randomness from the change in its probabilities. Explain why visibility and the operating phase both affect local sensitivity.
- **Dependencies and story role:** M01. Move from a state carrying phase to the statistics available to an observer.
- **Conceptual connection:** A steep, reproducible change in probabilities is useful; a phase stored in an inaccessible part of the state is insufficient.
- **Source pointers:** Anchor §2, Eq. (7), and §4.1, Eqs. (51)–(53); [information being bounded](../science/model.md#the-information-being-bounded), [parity likelihood](../science/construction.md#3-exact-parity-likelihood-and-information).

### M03

**Classical Fisher information and independent records**

- **Central question:** What does Fisher information quantify, and why do independent sensing groups contribute additively?
- **Understanding target:** Interpret $F_C$ as local sensitivity of the entire likelihood. Explain additivity for independent records and the role of repetitions in a local Cramér–Rao bound, including its regularity conditions.
- **Dependencies and story role:** M02. Introduce the quantity that will be bounded and assembled across groups.
- **Conceptual connection:** Summing information from independent experiments differs from adding their phase amplitudes coherently.
- **Source pointers:** Anchor §4.1, Eqs. (51)–(53); [information being bounded](../science/model.md#the-information-being-bounded), [finite grouping lemma](../science/frontier.md#a-finite-grouping-lemma).

### M04

**Quantum sensitivity and a chosen measurement**

- **Central question:** Why can the state possess more information than the actual detector record reveals?
- **Understanding target:** Distinguish QFI from the classical information obtained by a specified measurement. Use $F_Q=4\operatorname{Var}(H)$ for pure unitary families, and explain why parameter-independent processing cannot improve QFI.
- **Dependencies and story role:** M01–M03. Add the measurement-independent benchmark needed to judge a readout.
- **Conceptual connection:** An optimal-measurement statement does not provide an implementation within a restricted noisy circuit architecture.
- **Source pointers:** Anchor §4.2, Eqs. (55), (59)–(61), (77), and §4.3, Eqs. (83)–(87); [information being bounded](../science/model.md#the-information-being-bounded).

### M05

**The collective phase of an entangled probe**

- **Central question:** Why does a GHZ state have an $N^2$ information benchmark while independent equatorial sensors have an $N$ benchmark?
- **Understanding target:** Connect the additive generator's spectral width to its variance and to the relative phase $N\theta$ of a GHZ state. Distinguish this collective phase from $N$ independent single-sensor records.
- **Dependencies and story role:** M03–M04. Extend the single-qubit picture to the many-sensor sensitivity that motivates the project.
- **Conceptual connection:** Entanglement provides a potential metrological advantage; readable measurement statistics determine how much of it is attained.
- **Source pointers:** Anchor §2.2, Eqs. (25)–(30), and §5.1, Eqs. (99)–(101); [information being bounded](../science/model.md#the-information-being-bounded), [sensing state and readable record](../science/interpretation.md#a-sensing-state-and-a-readable-record-are-different-resources).

### M06

**Where an imperfection acts**

- **Central question:** Why does noise during sensing differ from an assignment error after coherent readout?
- **Understanding target:** Locate preparation, encoding, coherent readout and terminal detection in the experiment. Explain why already-lost state coherence limits every later measurement, whereas detector noise may be mitigated by reorganizing the information beforehand.
- **Dependencies and story role:** M04–M05. Introduce the physical boundary that makes the project a readout-resource problem.
- **Conceptual connection:** The location of a channel in the experiment matters because an entangling readout generally does not commute with it.
- **Source pointers:** Anchor §6, especially Eq. (132), as a comparison with state noise; [sensors, circuit and detector](../science/model.md#sensors-circuit-and-detector), [gate and sensing noise](../science/interpretation.md#gate-and-sensing-noise-are-not-corrected-by-this-result).

### M07

**Processing records and retaining settings**

- **Central question:** What changes when a random measurement setting is recorded or forgotten?
- **Understanding target:** Explain classical data processing and why a parameter-independent, labeled mixture has the average of its conditional Fisher informations. Distinguish that record from an unlabeled mixture of likelihoods.
- **Dependencies and story role:** M02–M04. Identify which classical information survives after measurement choices and decoding.
- **Conceptual connection:** A setting can be random without being unknown to the observer. Discarding its label can destroy a phase signal.
- **Source pointers:** Anchor §4.1 supplies the likelihood/FI definition; [sensors, circuit and detector](../science/model.md#sensors-circuit-and-detector), [ancillas and classical settings](../science/converse.md#ancillas-and-classical-settings), [uniformly random phase](../science/construction.md#uniformly-random-phase).

### M08

**Reliability from repeated classical evidence**

- **Central question:** How can several noisy observations make one binary decision reliable?
- **Understanding target:** Explain majority decoding for independent symmetric errors and likelihood comparison for general classical detector outputs. Distinguish independence of detector errors from possible correlations among the ideal encoded bits.
- **Dependencies and story role:** M02, M06–M07. Supply the classical mechanism used by the constructive readout.
- **Conceptual connection:** Redundancy protects an encoded basis label, while a parity statistic combines the resulting logical decisions.
- **Source pointers:** Anchor §6 motivates the importance of a specified noise model; the decoding derivations are supplied in [majority decoding](../science/construction.md#2-majority-decoding-for-every-block-size) and [repetition with asymmetric errors](../science/detectors.md#repetition-decoding-with-asymmetric-errors), rather than assumed from the review.

### M09

**Circuit depth and the reach of a local generator**

- **Central question:** What can one additional layer of two-qubit gates make physically accessible?
- **Understanding target:** Define disjoint two-qubit layers, forward causal supports and their intersections. Explain how nearest-neighbor geometry constrains spatial reach and how bounded fan-in constrains all-to-all growth.
- **Dependencies and story role:** M01, M04, M06. Introduce the resource that constrains the readout implementation.
- **Conceptual connection:** The conjugated generator $V(Z_i/2)V^\dagger$ records where one sensor's phase can influence the terminal outputs.
- **Source pointers:** Anchor §4.3 supplies the unrestricted-measurement comparison; circuit restrictions are defined in [architectures](../science/model.md#architectures) and [circuit causality](../science/converse.md#4-circuit-causality).

### M10

**Purification and information in an environment**

- **Central question:** How can a hypothetical larger quantum system help bound the observed information?
- **Understanding target:** Distinguish a mathematical purification from an accessible physical ancilla. Explain why tracing out an environment cannot increase QFI and why changing only that environment can change a purification without changing the receiver's state.
- **Dependencies and story role:** M04, M06, M09. Supply the logical basis for the universal converse.
- **Conceptual connection:** A more informative receiver can upper-bound the actual detector; environmental freedom then makes that upper bound calculable.
- **Source pointers:** Anchor §4.2, Eqs. (62), (77), and §6's channel-bound discussion; [informative comparison channel](../science/converse.md#1-an-informative-channel-above-the-noisy-detector), [legitimate environmental gauge](../science/converse.md#2-a-legitimate-environmental-gauge).

### M11

**Local sensitivity and global ambiguity**

- **Central question:** Can a sharply varying likelihood still leave several phases indistinguishable?
- **Understanding target:** Explain the difference between local Fisher information and global phase risk. Identify the repeated fringes of a GHZ likelihood and why a uniform local-information guarantee does not remove them.
- **Dependencies and story role:** M02–M05, M07. Integrate statistical sensitivity with the physical meaning of the phase record.
- **Conceptual connection:** A good local ruler does not identify which repeated interval contains the unknown phase.
- **Source pointers:** Anchor §2's local-estimation discussion and §4.1; [information being bounded](../science/model.md#the-information-being-bounded), [local sensitivity and aliases](../science/interpretation.md#local-sensitivity-does-not-remove-phase-aliases).

### M12

**The complete resource question**

- **Central question:** What exactly is optimized, and what must an upper bound and a construction each establish?
- **Understanding target:** State the experiment with an arbitrary supplied probe, fixed independent terminal detectors, ideal readout gates and one detector round. Interpret the supremum over allowed protocols and infimum over phase in $\mathcal F(N,d)$; distinguish a pointwise all-probe ceiling from one attained protocol.
- **Dependencies and story role:** M01–M11. Synthesize the background into the full scientific problem.
- **Conceptual connection:** The central issue is how a bounded readout resource converts available quantum sensitivity into recorded local information.
- **Source pointers:** Anchor §§2.2, 4.1–4.3 and 6; [complete model and principal statements](../science/model.md), [resource accounting](../science/interpretation.md#resource-accounting).

## Phase II: Narrative and innovation

### M13

**A stronger receiver that simulates one noisy detector**

- **Central question:** Why is quantum erasure a valid upper-bound comparison for a bit-flip detector?
- **Understanding target:** Reconstruct the erasure-and-fair-bit simulation with $\eta=2p$. Explain the direction of the information inequality, the role of the retained erasure flag, and why the simulation remains valid for entangled inputs.
- **Dependencies and story role:** M06–M07, M10, M12. Begin the converse with a single-output channel identity.
- **Conceptual connection:** Enlarging the receiver's access permits an upper bound without moving detector noise through the entangling circuit.
- **Source pointers:** Anchor §4.2's QFI/partial-trace foundations; [informative comparison channel](../science/converse.md#1-an-informative-channel-above-the-noisy-detector).

### M14

**An unbiased generator carried by erased supports**

- **Central question:** What can the environment represent when it receives an entire causal support?
- **Understanding target:** Explain the indicator and inverse-probability weight in $a_i(E)$, why $\mathbb E[a_i]=1$, and why $A_E$ acts only on erased qubits. Distinguish the phase-local gauge used in a proof from an unknown-parameter-dependent experimental operation.
- **Dependencies and story role:** M09–M10, M13. Build the local operator ingredient of the converse.
- **Conceptual connection:** Probability weighting converts occasional access to a whole support into an unbiased environmental representation of its generator.
- **Source pointers:** Anchor §4.2 supplies QFI foundations; [environmental gauge](../science/converse.md#2-a-legitimate-environmental-gauge) supplies the derivation, with its research-level provenance in [Zhou–Liu–Jiang](../references/RELATED_WORK.md#zhou2021).

### M15

**Why only intersecting supports contribute**

- **Central question:** Which correlations survive after subtracting the environmental representation?
- **Understanding target:** Explain how independent erasures give $\mathbb E[(1-a_i)(1-a_j)]=\eta^{-\lvert C_i\cap C_j\rvert}-1$. Identify the exact cancellation for disjoint supports and why omitting it would lose the useful shallow-circuit bound.
- **Dependencies and story role:** M09, M13–M14. Move from a single support to the pairwise quantity controlling the converse.
- **Conceptual connection:** The covariance depends on shared physical outputs, while arbitrary input-state correlations remain allowed.
- **Source pointers:** Anchor §4.2 supplies the information framework; [covariance evaluation](../science/converse.md#3-evaluate-the-covariance), [what the converse measures](../science/interpretation.md#what-the-converse-measures).

### M16

**Compression without shrinking the sensing phase**

- **Central question:** Why can small readout blocks retain a phase accumulated by a much larger GHZ group?
- **Understanding target:** Distinguish group size $M$ from block size $b$. Explain how inverse fanout moves the GHZ correlation to block leaders while retaining $M\theta$, and how the other sensors return to the zero state for reuse.
- **Dependencies and story role:** M05, M08–M09, M12. Begin the constructive branch with one block operation.
- **Conceptual connection:** Compression changes where the signal is stored, not how much phase the earlier sensing evolution accumulated.
- **Source pointers:** Anchor §2.2, Eqs. (25)–(30); [block compression](../science/construction.md#1-compress-each-block-without-losing-the-group-phase), [inherited global primitive](../references/RELATED_WORK.md#zhou2023).

### M17

**Turning leader phases into repeated basis labels**

- **Central question:** What information is made redundant by the Hadamard-and-fanout step?
- **Understanding target:** Connect the leader Hadamards to a parity-dependent distribution of logical bits, then explain why fanout repeats computational-basis labels without cloning an arbitrary unknown quantum state.
- **Dependencies and story role:** M01–M02, M08, M16. Complete the local quantum operation that prepares each block for noisy detection.
- **Conceptual connection:** The phase survives as a correlation among several logical bits, each of which can be protected by classical redundancy.
- **Source pointers:** Anchor §2.2 supplies GHZ parity foundations; [compression, leader distribution and fanout](../science/construction.md#1-compress-each-block-without-losing-the-group-phase).

### M18

**The logical error of a noisy repetition block**

- **Central question:** How does block volume determine the probability of one wrong logical decision?
- **Understanding target:** Explain the majority tail and fair-tie term for even block size, the bound $\epsilon_b\le p$, and the exponential error bound controlled by $c_p$. Identify why the resulting error channel is independent of the ideal logical bit.
- **Dependencies and story role:** M08, M16–M17. Quantify the reliability supplied by one readout block.
- **Conceptual connection:** Exponentially improving one block decision will compete with the number of decisions entering a larger parity.
- **Source pointers:** Anchor §6 supplies noise-model context; [majority error and exponential bound](../science/construction.md#2-majority-decoding-for-every-block-size) provides the required probability argument.

### M19

**From reliable blocks to a measurable group phase**

- **Central question:** How do independent logical errors change a GHZ group's parity likelihood?
- **Understanding target:** Explain the product visibility $v=\prod_j(1-2\epsilon_{b_j})$ and its effect on the exact parity FI. Distinguish the attained information of this decoded statistic from the potentially larger information in the complete raw record.
- **Dependencies and story role:** M02–M03, M07, M16–M18. Assemble the block outputs into a group-level sensing statistic.
- **Conceptual connection:** Protecting each bit is useful only through its accumulated effect on the parity carrying $M\theta$.
- **Source pointers:** Anchor §§2.2 and 4.1; [exact parity likelihood and information](../science/construction.md#3-exact-parity-likelihood-and-information).

### M20

**A fixed protocol that works at every phase**

- **Central question:** How can the protocol avoid phases at which one parity setting has zero slope?
- **Understanding target:** Explain the constant-fraction guarantee from two recorded quadratures and the phase-independent FI from a recorded uniform offset. Distinguish their asymptotic information fractions and explain why discarding a uniformly random offset label removes the signal while retaining it still leaves global aliases.
- **Dependencies and story role:** M07, M11, M19. Convert an operating-point construction into the phase-uniform local objective.
- **Conceptual connection:** Controlled measurement diversity improves local coverage without resolving the repeated fringes of the encoding.
- **Source pointers:** Anchor §4.1 supplies the FI definition; [phase-uniform experiment](../science/construction.md#4-a-fixed-experiment-with-sensitivity-at-every-phase), [phase aliases](../science/interpretation.md#local-sensitivity-does-not-remove-phase-aliases).

### M21

**An architecture-dependent ceiling for every probe**

- **Central question:** How do the local covariance ingredients become a bound on all sensing protocols at a given depth?
- **Understanding target:** Assemble the purification bound, operator norms and support intersections into T1. Explain the roles of the maximum support size $s$ and overlap count $\Delta$, and derive the fixed-depth $O(N)$ conclusion for both architectures without assuming a product input.
- **Dependencies and story role:** M04, M09–M10, M12–M15. Turn the converse ingredients into a global resource constraint.
- **Conceptual connection:** Limited circuit reach, rather than a lack of input entanglement, imposes the noisy-readout ceiling.
- **Source pointers:** Anchor §4.2 supplies pure-state QFI and monotonicity; [covariance bound](../science/converse.md#3-evaluate-the-covariance), [circuit causality](../science/converse.md#4-circuit-causality), [T1](../science/model.md#t1-the-support-intersection-converse).

### M22

**An executable readout within the depth budget**

- **Central question:** What gates actually realize the protected block on each architecture?
- **Understanding target:** Explain nearest-neighbor coordinate fanout and all-to-all doubling, including their reversed compression passes. Account for disjoint layers, the $2(b-1)$ CNOT count per block, parallel execution and reuse of sensing qubits.
- **Dependencies and story role:** M09, M16–M18. Translate the constructive mechanism into the same resource units used by the converse.
- **Conceptual connection:** A reliable block is available only if its required gate schedule fits the allowed readout depth.
- **Source pointers:** Anchor §4.3 motivates implementation of a measurement but does not supply these schedules; [depth and gate count](../science/construction.md#5-depth-and-gate-count), [resource accounting](../science/interpretation.md#resource-accounting).

### M23

**Choosing a sensing group small enough to read reliably**

- **Central question:** What should be done when the available blocks cannot protect one global GHZ parity?
- **Understanding target:** Explain the choice of at most order $1/\epsilon_b$ blocks per GHZ group, the uniform visibility lower bound, and how independent groups' FI adds. Account for a final smaller group instead of assuming divisibility.
- **Dependencies and story role:** M03, M18–M20, M22. Assemble many blocks into a finite-size protocol at any available block volume.
- **Conceptual connection:** The construction trades coherent group size against accumulated logical errors, then uses repetition across groups to exploit the full sensor budget.
- **Source pointers:** Anchor §4.1 supplies classical FI and §4.2, Eq. (72), its quantum additivity counterpart; [finite grouping lemma](../science/frontier.md#a-finite-grouping-lemma).

### M24

**Fitting complete blocks into a finite lattice**

- **Central question:** How can a constructive depth bound remain valid for nondivisible grid sizes and zero depth?
- **Understanding target:** Explain the integer block-side choice, complete-cube tiling, active count $N'$ and use of inactive $Z$ eigenstates. Distinguish the finite constant active fraction from the asymptotic fraction approaching one, and identify the product-probe endpoint at $d=0$.
- **Dependencies and story role:** M09, M12, M22–M23. Put the abstract grouping construction into the specified physical geometry.
- **Conceptual connection:** Rounding and unused sites affect constants and must be controlled before claiming a bound uniform in depth and system size.
- **Source pointers:** Anchor §5.1 supplies the separable benchmark; [full cubic lattices](../science/frontier.md#full-cubic-lattices), [architectures](../science/model.md#architectures).

### M25

**The matched logarithmic lattice frontier**

- **Central question:** In what precise sense do the lattice upper and lower bounds match?
- **Understanding target:** Combine the causal ceiling and packed-block lower bound to interpret $\log(1+\mathcal F/N)$ as order $\min\lbrace(d+1)^D,\log(1+N)\rbrace$. Explain fixed-depth extensivity, the intermediate enhancement and saturation, while distinguishing a logarithmic-order theorem from matched exponential constants.
- **Dependencies and story role:** M12, M21–M24. Synthesize the two arguments into the principal geometric frontier.
- **Conceptual connection:** Accessible causal volume limits information from above and protects logical decisions from below.
- **Source pointers:** Anchor §§4.1–4.2 supplies the performance framework; [logarithmic-order derivation](../science/frontier.md#deriving-the-logarithmic-order-statement), [T2](../science/model.md#t2-geometric-precision-frontier).

### M26

**The all-to-all threshold and its unresolved coefficient**

- **Central question:** Why is the all-to-all threshold order determined even though its finite-depth frontier is not matched?
- **Understanding target:** Compare support growth $2^d$ with the constructed block size $2^{\lfloor d/2\rfloor}$. Explain why both imply a $\log\log N$ depth order, while the separate compression and expansion passes leave a leading factor-two gap.
- **Dependencies and story role:** M21–M23, M25. Compare architectures without overstating the precision of the matching result.
- **Conceptual connection:** A shared asymptotic order can coexist with a consequential gap in the optimal circuit's constant factor.
- **Source pointers:** Anchor §4.3 supplies measurement context; [all-to-all bounds](../science/frontier.md#all-to-all-connectivity), [threshold consequences](../science/frontier.md#threshold-consequences), [T3](../science/model.md#t3-all-to-all-depth-threshold).

### M27

**Logarithmic blocks recover nearly all ideal local information**

- **Central question:** How can a small readout volume preserve the phase of almost the entire sensor array?
- **Understanding target:** Connect exponential block reliability to vanishing accumulated parity error for blocks of order $\log N$. Explain why $N'/N\to1$ matters and why the recorded uniform-phase protocol, rather than merely the two-setting lower bound, establishes $F_C/N^2\to1$ uniformly over phase.
- **Dependencies and story role:** M18–M20, M22, M24–M26. Integrate asymptotic attainment with the necessary depth orders.
- **Conceptual connection:** The construction approaches the ideal information ceiling while paying only for protecting logical measurement bits, with probe preparation accounted separately.
- **Source pointers:** Anchor §§2.2, 4.1–4.2; [logarithmic-block attainment](../science/construction.md#6-logarithmic-blocks-recover-nearly-all-local-information), [threshold consequences](../science/frontier.md#threshold-consequences).

### M28

**Which classical detectors share the law?**

- **Central question:** Which parts of the proof and construction survive when the detector is asymmetric or has more than two outputs?
- **Understanding target:** Reassemble the argument using common overlap $\eta$ for the erasure converse and exponent $\chi$ for repetition discrimination. Explain independent block complements, their use and marginalization, and the distinction between a decoded parity record and the richer mask-labeled record. Identify the informative-overlapping regime and its endpoints.
- **Dependencies and story role:** M07–M08, M13, M18–M27. Integrate the results across the established detector class.
- **Conceptual connection:** The resource law needs a nonzero common detector component and exponential distinguishability; symmetric bit flips are one instance.
- **Source pointers:** Anchor §6 supplies noise-model context; [general classical detectors](../science/detectors.md), especially [logical symmetrization](../science/detectors.md#symmetrize-the-logical-channel) and [excluded measurement classes](../science/detectors.md#endpoints-and-excluded-measurement-classes).

### M29

**The boundaries that give the theorem its physical meaning**

- **Central question:** Which changes to the experiment remove the obstruction or require a different theorem?
- **Understanding target:** Explain the counterexamples from parity-preserving correlated errors and repeated QND measurements. Distinguish terminal readout depth from preparation depth, pre-readout coherence loss, physical density, gate fan-in and global estimation resources; retain fixed detector parameters in the asymptotic claim.
- **Dependencies and story role:** M06, M09–M12, M21–M28. Test the integrated result against changes to its load-bearing assumptions.
- **Conceptual connection:** A resource law is meaningful only when all channels and operations capable of avoiding its bottleneck are accounted for.
- **Source pointers:** Anchor §6 supplies the broader noisy-metrology comparison; [resource accounting](../science/interpretation.md#resource-accounting), [concrete failure modes](../science/interpretation.md#assumptions-with-concrete-failure-modes).

### M30

**The complete scientific contribution**

- **Central question:** What has been established, how do its two arguments fit together, and how does it relate to previous work?
- **Understanding target:** Explain the arbitrary-probe support-intersection ceiling, matched lattice logarithmic frontier and optimal threshold orders together with their scope. Identify inherited purification machinery and the global decoder, distinguish the ideal-detector depth result with the same exponents, and separate analytical proof from finite verification and publication-priority judgments.
- **Dependencies and story role:** M12–M29. Synthesize the narrative, assumptions, proof dependencies, attainable protocols and open quantitative gap.
- **Conceptual connection:** Input entanglement supplies phase sensitivity; sufficient coherent readout makes that sensitivity accessible through independent imperfect detectors.
- **Source pointers:** Anchor §§2.2, 4.1–4.3, 5.1 and 6 supplies the foundational context; [principal results](../science/model.md#principal-results), [what is and is not sharp](../science/frontier.md#what-is-and-is-not-sharp), [related work](../references/RELATED_WORK.md), [verification and its limits](../verification/README.md).
