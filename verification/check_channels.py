#!/usr/bin/env python3
"""Finite channel, gauge, and GHZ-decoder checks (seed 20261024).

Default: recompute and compare with expected_channels.json using tolerances.
--output PATH: write fresh results after all internal checks pass.
Requires NumPy. These finite checks do not prove an asymptotic theorem.
"""

import argparse
import json
import math
from pathlib import Path

import numpy as np

SEED = 20261024
HAD = np.array([[1, 1], [1, -1]], complex) / np.sqrt(2)
CNOT = np.array([[1, 0, 0, 0], [0, 1, 0, 0],
                 [0, 0, 0, 1], [0, 0, 1, 0]], complex)


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def gate(state, unitary, sites, n):
    """Apply a gate to a state vector or to every column of a matrix."""
    shape = state.shape
    columns = state.size // 2**n
    order = list(sites) + [i for i in range(n) if i not in sites] + [n]
    tensor = state.reshape([2] * n + [columns]).transpose(order)
    tensor = unitary @ tensor.reshape(2**len(sites), -1)
    return tensor.reshape([2] * n + [columns]).transpose(np.argsort(order)).reshape(shape)


def bsc(values, p, n):
    tensor = np.asarray(values).reshape([2] * n).copy()
    for axis in range(n):
        tensor = (1 - p) * tensor + p * np.flip(tensor, axis=axis)
    return tensor.reshape(-1)


def cfi(probabilities, derivative):
    require(np.min(probabilities) >= -1e-12, "Negative probability")
    mask = probabilities > 1e-14
    return float(np.sum(derivative[mask]**2 / probabilities[mask]))


def partial_trace(matrix, keep, n):
    keep = sorted(keep)
    traced = [i for i in range(n) if i not in keep]
    order = keep + traced + [i + n for i in keep] + [i + n for i in traced]
    a, b = 2**len(keep), 2**len(traced)
    tensor = matrix.reshape([2] * (2 * n)).transpose(order).reshape(a, b, a, b)
    return np.trace(tensor, axis1=1, axis2=3)


def qfi(state, derivative):
    eigenvalues, eigenvectors = np.linalg.eigh((state + state.conj().T) / 2)
    require(eigenvalues.min() > -1e-10, "Nonpositive density matrix")
    denominator = np.maximum(eigenvalues, 0)[:, None] + np.maximum(eigenvalues, 0)[None, :]
    transformed = eigenvectors.conj().T @ derivative @ eigenvectors
    mask = denominator > 1e-12
    return float(np.sum(2 * np.abs(transformed[mask])**2 / denominator[mask]))


def haar(rng, dimension):
    matrix = rng.normal(size=(dimension, dimension)) + 1j * rng.normal(size=(dimension, dimension))
    unitary, triangular = np.linalg.qr(matrix)
    phases = np.diag(triangular)
    return unitary @ np.diag(phases / np.abs(phases))


def random_readout(rng, layers, n=4):
    unitary = np.eye(2**n, dtype=complex)
    cones = [{i} for i in range(n)]
    for layer in [*layers, []]:
        for site in range(n):
            unitary = gate(unitary, haar(rng, 2), [site], n)
        for pair in layer:
            unitary = gate(unitary, haar(rng, 4), pair, n)
            pair = set(pair)
            cones = [cone | pair if cone & pair else cone for cone in cones]
    require(np.max(np.abs(unitary.conj().T @ unitary - np.eye(2**n))) < 2e-13,
            "Readout matrix is not unitary")
    return unitary, cones


def covariance_and_gauge(rng):
    cones, eta = [{0, 1}, {1, 2}, {3}, {0, 2, 3}], 0.37
    enumerated = np.zeros((4, 4))
    for mask in range(16):
        erased = {i for i in range(4) if mask >> i & 1}
        residual = 1 - np.array([float(cone <= erased) / eta**len(cone) for cone in cones])
        enumerated += eta**len(erased) * (1 - eta)**(4 - len(erased)) * np.outer(residual, residual)
    exact = np.array([[eta**(-len(a & b)) - 1 for b in cones] for a in cones])
    covariance_error = float(np.max(np.abs(enumerated - exact)))
    require(covariance_error < 1e-11, "Erasure covariance identity failed")
    # Nonuniform overlapping cones, including an isolated input generator.
    unitary, cones = random_readout(rng, [[(0, 1)], [(1, 2)]])
    eta = 0.46
    generators = []
    for site in range(4):
        diagonal = np.array([0.5 - ((x >> (3 - site)) & 1) for x in range(16)])
        generators.append((unitary * diagonal) @ unitary.conj().T)
    lhs, mean = np.zeros((16, 16), complex), np.zeros((16, 16), complex)
    for mask in range(16):
        erased = {i for i in range(4) if mask >> i & 1}
        weight = eta**len(erased) * (1 - eta)**(4 - len(erased))
        residual = sum((1 - float(cone <= erased) / eta**len(cone)) * generator
                       for cone, generator in zip(cones, generators))
        mean += weight * residual
        lhs += weight * residual @ residual
    coefficients = [[eta**(-len(a & b)) - 1 for b in cones] for a in cones]
    rhs = sum(coefficients[i][j] * generators[i] @ generators[j]
              for i in range(4) for j in range(4))
    gauge_error, mean_error = float(np.max(np.abs(lhs - rhs))), float(np.max(np.abs(mean)))
    norm_error = abs(4 * np.linalg.eigvalsh(lhs).max() - np.sum(coefficients))
    require(max(gauge_error, mean_error, norm_error) < 1e-10, "Matrix gauge identity failed")
    return {"covariance_max_error": covariance_error, "gauge_max_error": gauge_error,
            "mean_residual_max_error": mean_error, "norm_identity_error": float(norm_error),
            "gauge_cones": [sorted(cone) for cone in cones], "gauge_eta": eta}


def random_channel_checks(rng):
    n, theta, step = 4, 0.271, 1e-6
    hz = np.array([(n - 2 * x.bit_count()) / 2 for x in range(2**n)])
    results = []
    for depth in (0, 1, 2):
        layers = [[(0, 1), (2, 3)], [(0, 2), (1, 3)]][:depth]
        unitary, cones = random_readout(rng, layers)
        for kind in ("pure", "mixed"):
            matrix = rng.normal(size=(16, 1 if kind == "pure" else 16))
            matrix = matrix + 1j * rng.normal(size=matrix.shape)
            initial = matrix @ matrix.conj().T
            initial /= np.trace(initial)
            def encoded(angle):
                phases = np.exp(-1j * angle * hz)
                return phases[:, None] * initial * phases.conj()[None, :]
            input_state = encoded(theta)
            input_derivative = -1j * (hz[:, None] - hz[None, :]) * input_state
            state = unitary @ input_state @ unitary.conj().T
            derivative = unitary @ input_derivative @ unitary.conj().T
            input_qfi = qfi(input_state, input_derivative)
            require(abs(input_qfi - qfi(state, derivative)) < 1e-9, "Unitary QFI changed")
            shifted = [np.real(np.diag(unitary @ encoded(theta + sign * step) @ unitary.conj().T))
                       for sign in (-1, 1)]
            for p in (0.1, 0.3, 0.45):
                probabilities = bsc(np.real(np.diag(state)), p, n)
                dp = bsc(np.real(np.diag(derivative)), p, n)
                finite_difference = (bsc(shifted[1], p, n) - bsc(shifted[0], p, n)) / (2 * step)
                derivative_error = float(np.max(np.abs(finite_difference - dp)))
                require(derivative_error < 2e-9, "Analytic probability derivative failed")
                fi, erasure_qfi, eta = cfi(probabilities, dp), 0.0, 2 * p
                for mask in range(16):
                    erased = {i for i in range(n) if mask >> i & 1}
                    keep = set(range(n)) - erased
                    weight = eta**len(erased) * (1 - eta)**len(keep)
                    erasure_qfi += weight * qfi(partial_trace(state, keep, n),
                                               partial_trace(derivative, keep, n))
                support_bound = sum(eta**(-len(a & b)) - 1 for a in cones for b in cones)
                require(fi <= erasure_qfi + 1e-9, "Erasure domination failed")
                require(erasure_qfi <= min(support_bound, input_qfi) + 1e-9,
                        "Erasure QFI violates a universal upper bound")
                results.append({"n": n, "depth": depth, "input": kind, "p": p,
                                "classical_fi": fi, "erasure_qfi": erasure_qfi,
                                "support_bound": support_bound, "input_qfi": input_qfi,
                                "finite_difference_max_error": derivative_error})
    return results


def majority_error(size, p):
    total = math.fsum(math.comb(size, k) * p**k * (1 - p)**(size - k)
                      for k in range(size // 2 + 1, size + 1))
    return total + (0.5 * math.comb(size, size // 2) * (p * (1 - p))**(size // 2)
                    if size % 2 == 0 else 0)


def decoder_checks():
    results = []
    layouts = [(3,), (2,), (2, 2), (3, 3), (3, 3, 3), (2, 3, 4), (1, 2, 3)]
    for sizes in layouts:
        n, cursor, blocks = sum(sizes), 0, []
        for size in sizes:
            blocks.append(list(range(cursor, cursor + size)))
            cursor += size
        bits = (np.arange(2**n)[:, None] >> np.arange(n - 1, -1, -1)) & 1
        # A tie contributes zero expected parity: fair tie coins are integrated
        # exactly, giving a stochastic classical map instead of a sampled vote.
        parity_mean = np.prod([np.sign(len(block) - 2 * bits[:, block].sum(axis=1))
                               for block in blocks], axis=0)
        kernel = np.array([(1 + parity_mean) / 2, (1 - parity_mean) / 2])
        for phase in (0.37, 1.11, math.pi / 2):
            state = np.zeros(2**n, complex)
            state[0], state[-1] = 1 / np.sqrt(2), np.exp(1j * phase) / np.sqrt(2)
            derivative = np.zeros_like(state)
            derivative[-1] = 1j * n * state[-1]
            for block in blocks:
                pairs = list(zip(block[:-1], block[1:]))
                operations = [(CNOT, pair) for pair in reversed(pairs)]
                operations += [(HAD, [block[0]])] + [(CNOT, pair) for pair in pairs]
                for operation, sites in operations:
                    state = gate(state, operation, sites, n)
                    derivative = gate(derivative, operation, sites, n)
            for p in (0.1, 0.25, 0.4):
                raw = bsc(np.abs(state)**2, p, n)
                draw = bsc(2 * np.real(state.conj() * derivative), p, n)
                parity, dparity = kernel @ raw, kernel @ draw
                visibility = math.prod(1 - 2 * majority_error(size, p) for size in sizes)
                prediction = np.array([1 + visibility * math.cos(phase),
                                       1 - visibility * math.cos(phase)]) / 2
                dprediction = np.array([-1, 1]) * n * visibility * math.sin(phase) / 2
                error = float(max(np.max(np.abs(parity - prediction)),
                                  np.max(np.abs(dparity - dprediction))))
                require(error < 2e-11, "Decoder likelihood or derivative formula failed")
                actual, predicted = cfi(parity, dparity), cfi(prediction, dprediction)
                raw_fi = cfi(raw, draw)
                require(abs(actual - predicted) < 2e-9, "Decoder FI formula failed")
                require(actual <= raw_fi + 2e-9 and raw_fi <= n**2 + 2e-9,
                        "Decoder violates data processing or the ideal QFI bound")
                results.append({"n": n, "block_sizes": list(sizes), "p": p,
                                "logical_phase": phase, "visibility": visibility,
                                "parity_fi": actual, "formula_fi": predicted,
                                "raw_record_fi": raw_fi, "likelihood_max_error": error})
    return results


def compare(actual, expected, location="root"):
    if isinstance(expected, dict):
        require(isinstance(actual, dict) and actual.keys() == expected.keys(), location)
        for key in expected:
            compare(actual[key], expected[key], f"{location}.{key}")
    elif isinstance(expected, list):
        require(isinstance(actual, list) and len(actual) == len(expected), location)
        for index, (got, want) in enumerate(zip(actual, expected)):
            compare(got, want, f"{location}[{index}]")
    elif isinstance(expected, float):
        require(math.isfinite(actual) and math.isclose(actual, expected, rel_tol=3e-8, abs_tol=1e-10),
                f"{location}: {actual!r} differs from {expected!r}")
    else:
        require(type(actual) is type(expected) and actual == expected, location)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    rng = np.random.default_rng(SEED)
    result = {"schema_version": 1, "seed": SEED,
              "scope": "Finite algebra and channel checks; proof and novelty are separate.",
              "gauge": covariance_and_gauge(rng),
              "random_channels": random_channel_checks(rng), "decoders": decoder_checks()}
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2, allow_nan=False) + "\n", encoding="utf-8")
        action = f"wrote {args.output}"
    else:
        baseline = Path(__file__).with_name("expected_channels.json")
        compare(result, json.loads(baseline.read_text(encoding="utf-8")))
        action = "matched expected_channels.json"
    print(json.dumps({"status": "pass", "result": action, "seed": SEED,
                      "random_channel_cases": len(result["random_channels"]),
                      "decoder_cases": len(result["decoders"]), "gauge": result["gauge"],
                      "max_decoder_fi_error": max(abs(row["parity_fi"] - row["formula_fi"])
                                                   for row in result["decoders"]),
                      "max_finite_difference_error": max(row["finite_difference_max_error"]
                                                         for row in result["random_channels"])}, indent=2))


if __name__ == "__main__":
    main()
