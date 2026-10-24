"""Deterministic finite checks of the classical-detector extension.

Checks the common-overlap erasure decomposition, exact equal-prior repetition
errors, independent-complement symmetrization, even-block fair ties, and the
parity formula for correlated logical inputs. Finite likelihoods are enumerated
using exact rational arithmetic; reported results are floating-point numbers.
These checks do not establish the asymptotic theorem, experimental performance,
or novelty. Only Python's standard library is required.

By default, recompute and compare with expected_detectors.json without writing
files. --output PATH additionally saves the recomputed report after comparison.
"""

import argparse
import itertools
import json
import math
from fractions import Fraction
from pathlib import Path


ABS_TOL = 1e-12
REL_TOL = 1e-10
EXPECTED_PATH = Path(__file__).with_name("expected_detectors.json")


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def require_close(actual, expected, context):
    require(math.isfinite(actual) and math.isfinite(expected),
            f"{context}: nonfinite value {actual!r} or {expected!r}")
    require(math.isclose(actual, expected, rel_tol=REL_TOL, abs_tol=ABS_TOL),
            f"{context}: got {actual:.17g}, expected {expected:.17g}")


def repetitions(p0, p1, block_size, fair_tie=False):
    """Return exact-enumeration errors and tie mass as floats.

    Inputs in the finite benchmarks are decimal rational probabilities. Using
    their exact fractions makes an equal-likelihood tie unambiguous.
    """
    probabilities = [[Fraction(str(p)) for p in vector] for vector in (p0, p1)]
    alpha = beta = overlap = tie_mass = Fraction(0)
    for word in itertools.product(range(len(p0)), repeat=block_size):
        likelihoods = [math.prod(vector[y] for y in word)
                       for vector in probabilities]
        a, c = likelihoods
        if a == c:
            decide_one = Fraction(1, 2) if fair_tie else Fraction(0)
            tie_mass += a
        else:
            decide_one = Fraction(int(c > a))
        alpha += a * decide_one
        beta += c * (1 - decide_one)
        overlap += min(a, c)
    return tuple(float(value) for value in (alpha, beta, overlap / 2, tie_mass))


def symmetrized_transition(alpha, beta):
    """Q[reported logical bit][true logical bit], averaged over both masks."""
    base = [[1 - alpha, beta], [alpha, 1 - beta]]
    return [[sum(base[out ^ mask][bit ^ mask] for mask in (0, 1)) / 2
             for bit in (0, 1)] for out in (0, 1)]


def propagate(channels, input_distribution):
    words = tuple(input_distribution)
    return {
        reported: sum(weight * math.prod(channels[j][reported[j]][true[j]]
                                        for j in range(len(channels)))
                      for true, weight in input_distribution.items())
        for reported in words
    }


def propagate_with_explicit_masks(raw_channels, input_distribution):
    """Enumerate raw decisions and recorded masks before the classical undo."""
    count = len(raw_channels)
    words = tuple(input_distribution)
    result = dict.fromkeys(words, 0.0)
    for true, weight in input_distribution.items():
        for mask in words:
            physical = tuple(bit ^ r for bit, r in zip(true, mask))
            for estimate in words:
                probability = math.prod(raw_channels[j][estimate[j]][physical[j]]
                                        for j in range(count))
                report = tuple(bit ^ r for bit, r in zip(estimate, mask))
                result[report] += weight * probability / 2 ** count
    return result


def parity_expectation(distribution):
    return sum(weight * (-1) ** sum(word) for word, weight in distribution.items())


def compare_expected(actual, expected, path="report"):
    """Compare all fixture fields, with tolerances only for numeric values."""
    if isinstance(expected, dict):
        require(isinstance(actual, dict), f"{path}: expected an object")
        require(set(actual) == set(expected), f"{path}: object keys changed")
        for key in sorted(expected):
            compare_expected(actual[key], expected[key], f"{path}.{key}")
    elif isinstance(expected, list):
        require(isinstance(actual, list), f"{path}: expected a list")
        require(len(actual) == len(expected), f"{path}: list length changed")
        for index, (a, e) in enumerate(zip(actual, expected)):
            compare_expected(a, e, f"{path}[{index}]")
    elif isinstance(expected, (int, float)) and not isinstance(expected, bool):
        require(isinstance(actual, (int, float)) and not isinstance(actual, bool),
                f"{path}: expected a numeric value")
        require_close(actual, expected, path)
    else:
        require(actual == expected, f"{path}: got {actual!r}, expected {expected!r}")


def run():
    detectors = [
        ("asymmetric_ternary", [0.85, 0.10, 0.05], [0.20, 0.65, 0.15]),
        ("one_sided", [1.0, 0.0], [0.3, 0.7]),
        ("bsc", [0.8, 0.2], [0.2, 0.8]),
    ]
    repetition_records = []
    parity_records = []
    correlated_records = []
    fair_tie_records = []
    identity_errors = []
    words = tuple(itertools.product((0, 1), repeat=3))
    for name, p0, p1 in detectors:
        for bit, vector in enumerate((p0, p1)):
            require_close(sum(vector), 1, f"{name}: input-{bit} normalization")
        eta = sum(min(a, b) for a, b in zip(p0, p1))
        common = [min(a, b) / eta for a, b in zip(p0, p1)]
        residuals = [[(p[y] - eta * common[y]) / (1 - eta)
                      for y in range(len(p))] for p in (p0, p1)]
        require_close(sum(common), 1, f"{name}: common distribution normalization")
        for bit, vector in enumerate(residuals):
            require(min(vector) >= -ABS_TOL, f"{name}: negative residual probability")
            require_close(sum(vector), 1, f"{name}: residual-{bit} normalization")
        reconstruction_error = max(abs(p[y] - eta * common[y] -
                                       (1 - eta) * residuals[x][y])
                                   for x, p in enumerate((p0, p1))
                                   for y in range(len(p)))
        require_close(reconstruction_error, 0, f"{name}: erasure reconstruction")
        coefficient = sum(math.sqrt(a * b) for a, b in zip(p0, p1))
        require(0 < eta < 1 and 0 < coefficient < 1,
                f"{name}: benchmark detector must have nontrivial overlap")
        channels, raw_channels, epsilons = [], [], []
        for block_size in (1, 2, 5):
            alpha, beta, epsilon, tie_mass = repetitions(p0, p1, block_size)
            context = f"{name}, b={block_size}"
            channel = symmetrized_transition(alpha, beta)
            bayes_error = abs(epsilon - (alpha + beta) / 2)
            sym_error = max(abs(channel[out][bit] -
                                (epsilon if out != bit else 1 - epsilon))
                            for out in (0, 1) for bit in (0, 1))
            require_close(bayes_error, 0, f"{context}: equal-prior error identity")
            require_close(sym_error, 0, f"{context}: mask symmetrization")
            upper_bound = coefficient ** block_size / 2
            require(epsilon <= upper_bound + ABS_TOL,
                    f"{context}: error {epsilon} exceeds bound {upper_bound}")
            identity_errors.extend((bayes_error, sym_error, reconstruction_error))
            channels.append(channel)
            raw_channels.append([[1 - alpha, beta], [alpha, 1 - beta]])
            epsilons.append(epsilon)
            repetition_records.append({
                "detector": name, "block_size": block_size, "eta": eta,
                "bhattacharyya_coefficient": coefficient,
                "alpha": alpha, "beta": beta, "epsilon": epsilon,
                "tie_mass": tie_mass, "bhattacharyya_bound": upper_bound,
                "bayes_identity_error": bayes_error,
                "symmetrization_error": sym_error,
                "erasure_reconstruction_error": reconstruction_error,
            })
        visibility = math.prod(1 - 2 * e for e in epsilons)
        for phase in (0.2, 0.7, 1.8):
            source = {word: (1 + (-1) ** sum(word) * math.cos(phase)) / 8
                      for word in words}
            got = parity_expectation(propagate(channels, source))
            predicted = visibility * math.cos(phase)
            require_close(got, predicted, f"{name}, phase={phase}: GHZ parity")
            error = abs(got - predicted)
            identity_errors.append(error)
            parity_records.append({"detector": name, "phase": phase,
                                   "observed_bias": got, "predicted_bias": predicted,
                                   "absolute_error": error})

        # A biased joint distribution with correlations beyond uniform marginals.
        source = dict.fromkeys(words, 0.0)
        source.update({(0, 0, 0): 0.40, (0, 1, 1): 0.10, (1, 0, 1): 0.15,
                       (1, 1, 0): 0.05, (1, 1, 1): 0.30})
        direct = propagate_with_explicit_masks(raw_channels, source)
        reduced = propagate(channels, source)
        distribution_error = max(abs(direct[word] - reduced[word]) for word in words)
        require_close(distribution_error, 0, f"{name}: correlated-input distribution")
        require_close(sum(direct.values()), 1, f"{name}: output normalization")
        predicted = parity_expectation(source) * visibility
        measured = parity_expectation(direct)
        require_close(measured, predicted, f"{name}: biased-input parity")
        identity_errors.extend((distribution_error, abs(measured - predicted)))
        correlated_records.append({
            "detector": name, "input_probabilities_lexicographic": list(source.values()),
            "output_probabilities_lexicographic": list(direct.values()),
            "distribution_max_absolute_error": distribution_error,
            "observed_bias": measured, "predicted_bias": predicted,
        })

    for block_size in (2, 4):
        p = 0.2
        alpha, beta, epsilon, tie_mass = repetitions([1 - p, p], [p, 1 - p],
                                                     block_size, fair_tie=True)
        majority_error = sum(math.comb(block_size, k) * p ** k * (1 - p) ** (block_size - k)
                             for k in range(block_size // 2 + 1, block_size + 1))
        majority_error += 0.5 * math.comb(block_size, block_size // 2) * (p * (1 - p)) ** (block_size // 2)
        require(tie_mass > 0, f"fair tie, b={block_size}: missing actual tied outcomes")
        for label, actual in (("alpha", alpha), ("beta", beta), ("epsilon", epsilon)):
            require_close(actual, majority_error, f"fair tie, b={block_size}: {label}")
            identity_errors.append(abs(actual - majority_error))
        fair_tie_records.append({"block_size": block_size, "p": p, "alpha": alpha,
                                 "beta": beta, "epsilon": epsilon, "tie_mass": tie_mass,
                                 "majority_formula": majority_error})

    require(max(identity_errors) < ABS_TOL, "finite identities exceed absolute tolerance")
    return {
        "schema_version": 1,
        "scope": "Finite classical-detector identities; no asymptotic or experimental claim.",
        "repetition_case_count": len(repetition_records),
        "fair_tie_case_count": len(fair_tie_records),
        "ghz_parity_case_count": len(parity_records),
        "biased_correlated_input_case_count": len(correlated_records),
        "max_absolute_identity_error": max(identity_errors),
        "repetition_cases": repetition_records,
        "fair_tie_cases": fair_tie_records,
        "ghz_parity_cases": parity_records,
        "biased_correlated_input_cases": correlated_records,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="also save the recomputed JSON report here")
    args = parser.parse_args()
    actual = run()
    expected = json.loads(EXPECTED_PATH.read_text(encoding="utf-8"))
    compare_expected(actual, expected)
    if args.output is not None:
        args.output.write_text(json.dumps(actual, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("PASS: detector identities and expected results; "
          f"9 repetition, 2 fair-tie, 9 GHZ parity, 3 biased correlated-input cases; "
          f"max absolute error {actual['max_absolute_identity_error']:.3g}")


if __name__ == "__main__":
    main()
