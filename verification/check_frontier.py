#!/usr/bin/env python3
"""Finite, reproducible checks of the readout-depth constructions.

Run from any working directory:
    python verification/check_frontier.py
    python verification/check_frontier.py --output /tmp/frontier-results.json

The default command recomputes and compares with expected_frontier.json.  The
--output command writes fresh results after all internal checks pass.  These
checks validate explicit small schedules, finite detector distributions,
rounding/grouping examples, and a phase integral; they do not prove the
asymptotic frontier or establish originality.  SciPy is needed for quadrature.
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
from pathlib import Path
from typing import Any

from scipy.integrate import quad


REL_TOL = 2e-9
ABS_TOL = 2e-11


def require(condition: bool, message: str) -> None:
    """Keep checks active even if Python is invoked with -O."""
    if not condition:
        raise AssertionError(message)


def lattice_fanout(dimension: int, side: int) -> tuple[list, list]:
    """Fill successive coordinate directions from the origin.

    Each layer is a list of (control, target) coordinate pairs.  Coordinates in
    directions not reached yet stay zero; already filled directions label
    disjoint parallel lines.
    """
    sites = list(itertools.product(range(side), repeat=dimension))
    layers = []
    for axis in range(dimension):
        for step in range(side - 1):
            layer = []
            for prefix in itertools.product(range(side), repeat=axis):
                control = prefix + (step,) + (0,) * (dimension - axis - 1)
                target = prefix + (step + 1,) + (0,) * (dimension - axis - 1)
                layer.append((control, target))
            layers.append(layer)
    return sites, layers


def complete_fanout(size: int) -> tuple[list, list]:
    """Double the active set each layer, including non-power-of-two sizes."""
    active = [0]
    next_site = 1
    layers = []
    while next_site < size:
        layer = []
        new_sites = []
        for control in active:
            if next_site == size:
                break
            layer.append((control, next_site))
            new_sites.append(next_site)
            next_site += 1
        layers.append(layer)
        active += new_sites
    return list(range(size)), layers


def inspect_schedule(sites: list, layers: list, nearest_neighbor: bool) -> dict:
    """Inspect the actual gates, then simulate both logical basis states."""
    known = set(sites)
    root = sites[0]
    bits = {site: int(site == root) for site in sites}
    zero_bits = {site: 0 for site in sites}
    gate_count = 0
    for layer_index, layer in enumerate(layers):
        touched = set()
        for control, target in layer:
            require(control in known and target in known, "Gate leaves block")
            require(control != target, "Self gate")
            require(control not in touched and target not in touched,
                    f"Overlapping gates in layer {layer_index}")
            touched.update((control, target))
            if nearest_neighbor:
                distance = sum(abs(a - b) for a, b in zip(control, target))
                require(distance == 1, "Non-nearest-neighbor lattice gate")
            require(bits[control] == 1 and bits[target] == 0,
                    "Fanout does not reach a fresh target from an active site")
            bits[target] ^= bits[control]
            zero_bits[target] ^= zero_bits[control]
            gate_count += 1
    require(all(bit == 1 for bit in bits.values()), "Fanout misses sites")
    require(not any(zero_bits.values()), "Zero state was changed")
    require(gate_count == len(sites) - 1, "Incorrect fanout gate count")
    # Reverse the actual gate schedule, rather than merely recounting gates.
    for layer in reversed(layers):
        for control, target in reversed(layer):
            bits[target] ^= bits[control]
    require(bits == {site: int(site == root) for site in sites},
            "Reverse schedule fails to compress the all-ones string")
    return {"size": len(sites), "depth": len(layers), "gates": gate_count}


def check_schedules() -> dict:
    lattice = []
    for dimension in (1, 2, 3):
        for side in (1, 2, 3, 4):
            sites, layers = lattice_fanout(dimension, side)
            result = inspect_schedule(sites, layers, nearest_neighbor=True)
            require(result["depth"] == dimension * (side - 1),
                    "Lattice schedule depth differs from claimed construction")
            lattice.append({"dimension": dimension, "side": side, **result})
    complete = []
    for size in (1, 2, 3, 4, 5, 7, 8, 9, 15, 16, 17, 31):
        sites, layers = complete_fanout(size)
        result = inspect_schedule(sites, layers, nearest_neighbor=False)
        require(result["depth"] == (size - 1).bit_length(),
                "All-to-all schedule does not attain ceiling(log2(size))")
        complete.append(result)
    return {"lattice": lattice, "all_to_all": complete}


def majority_error(size: int, error: float) -> float:
    """Exact finite binomial expression, with fair ties for even size."""
    terms = [math.comb(size, ones) * error**ones * (1 - error)**(size - ones)
             for ones in range(size // 2 + 1, size + 1)]
    if size % 2 == 0:
        terms.append(0.5 * math.comb(size, size // 2)
                     * error**(size // 2) * (1 - error)**(size // 2))
    return math.fsum(terms)


def enumerate_majority_error(size: int, error: float, input_bit: int) -> float:
    """Sum over physical detector strings, independently of the binomial sum."""
    contributions = []
    for output in itertools.product((0, 1), repeat=size):
        probability = math.prod(error if bit != input_bit else 1 - error
                                for bit in output)
        ones = sum(output)
        decoded_one = 1.0 if 2 * ones > size else 0.0
        if 2 * ones == size:
            decoded_one = 0.5
        wrong = decoded_one if input_bit == 0 else 1 - decoded_one
        contributions.append(probability * wrong)
    return math.fsum(contributions)


def check_majority() -> dict:
    cases = []
    largest_error = 0.0
    for error in (0.05, 0.2, 0.49):
        for size in range(1, 7):
            epsilon = majority_error(size, error)
            conditional = [enumerate_majority_error(size, error, bit)
                           for bit in (0, 1)]
            discrepancy = max(abs(value - epsilon) for value in conditional)
            largest_error = max(largest_error, discrepancy)
            require(discrepancy < 2e-14, "Majority distribution or symmetry failed")
            cases.append({"p": error, "block_size": size, "epsilon": epsilon})
    return {"cases": cases, "max_enumeration_error": largest_error}


def group_plan(blocks: int, epsilon: float) -> tuple[int, int, int]:
    """Return maximum group size, full group count, and remainder.

    Cap before taking a reciprocal so tiny logical errors cannot create a
    needlessly huge intermediate integer.
    """
    if 8 * blocks * epsilon <= 1:
        group_size = blocks
    else:
        group_size = max(1, math.floor(1 / (8 * epsilon)))
    group_size = min(blocks, group_size)
    full, leftover = divmod(blocks, group_size)
    return group_size, full, leftover


def finite_cap(sensors: int, block_size: int, exponent: float) -> float:
    """min(sensors, block_size * exp(exponent)), without large exponentials."""
    log_value = math.log(block_size) + exponent
    return float(sensors) if log_value >= math.log(sensors) else math.exp(log_value)


def parity_fi(sensors: int, log_visibility: float, phase: float) -> float:
    """Stable parity FI, including visibility extremely close to one."""
    one_minus_v_squared = -math.expm1(2 * log_visibility)
    sin_squared = math.sin(phase)**2
    cos_squared = math.cos(phase)**2
    denominator = sin_squared + one_minus_v_squared * cos_squared
    # In these tests 0<p<1/2 and finite block size imply a positive denominator.
    require(denominator > 0, "Unexpected singular detector likelihood")
    return (sensors**2 * (1 - one_minus_v_squared)
            * sin_squared / denominator)


def check_grouping() -> dict:
    cases = []
    incomplete_cases = 0
    zero_depth_cases = 0
    smallest_margin = math.inf
    phases = (0.0, 0.013, 0.17, 0.71, 1.0)
    for error in (0.001, 0.05, 0.2, 0.4, 0.49):
        exponent = -math.log(2 * math.sqrt(error * (1 - error)))
        visibility_floor = min(0.75, 1 - 2 * error)
        for size in (1, 2, 3, 4, 7, 10, 31):
            epsilon = majority_error(size, error)
            require(0 < epsilon <= error + 1e-14,
                    "Repetition is worse than ignoring extra bits")
            require(epsilon <= math.exp(-exponent * size) + 1e-14,
                    "Finite Chernoff bound failed")
            log_single_visibility = math.log1p(-2 * epsilon)
            for blocks in (1, 2, 3, 7, 30, 1000):
                group_size, full, leftover = group_plan(blocks, epsilon)
                multiplicities = [(group_size, full)]
                if leftover:
                    multiplicities.append((leftover, 1))
                    incomplete_cases += 1
                if size == 1:
                    zero_depth_cases += 1
                sensors = size * blocks
                guarantee = 0.5 * math.fsum(
                    count * (size * group)**2
                    * math.exp(2 * group * log_single_visibility)
                    for group, count in multiplicities)
                lower_bound = (visibility_floor**2 / 64 * sensors
                               * finite_cap(sensors, size, exponent * size))
                require(guarantee >= lower_bound * (1 - 2e-13),
                        "Finite grouping lemma failed")
                sampled_values = []
                for theta in phases:
                    total = 0.0
                    for group, count in multiplicities:
                        group_sensors = size * group
                        lv = group * log_single_visibility
                        phase = group_sensors * theta
                        total += count * 0.5 * (
                            parity_fi(group_sensors, lv, phase)
                            + parity_fi(group_sensors, lv, phase + math.pi / 2))
                    sampled_values.append(total)
                require(min(sampled_values) >= guarantee * (1 - 3e-13),
                        "Two labeled settings fail the finite uniform bound")
                margin = guarantee / lower_bound
                smallest_margin = min(smallest_margin, margin)
                cases.append({
                    "p": error, "block_size": size, "blocks": blocks,
                    "group_size": group_size, "full_groups": full,
                    "leftover_blocks": leftover,
                    "epsilon": epsilon,
                    "guarantee_over_N_squared": guarantee / sensors**2,
                    "bound_over_N_squared": lower_bound / sensors**2,
                })
    require(incomplete_cases > 0 and zero_depth_cases > 0,
            "Missing required remainder or zero-depth coverage")
    return {"cases": cases, "incomplete_group_cases": incomplete_cases,
            "zero_entangling_depth_cases": zero_depth_cases,
            "minimum_guarantee_to_bound_ratio": smallest_margin}


def check_lattice_tiling() -> list:
    """Enumerate retained sites, rather than only evaluating the floor formula."""
    cases = []
    for dimension in (1, 2, 3):
        for side in (1, 5, 8):
            depths = sorted({0, 1, 2 * dimension,
                             2 * dimension * (side - 1),
                             2 * dimension * max(0, side // 2 - 1)})
            for depth in depths:
                block_side = min(side, 1 + depth // (2 * dimension))
                retained = set()
                block_count = 0
                for tile in itertools.product(range(side // block_side),
                                              repeat=dimension):
                    block = {tuple(tile[axis] * block_side + offset[axis]
                                   for axis in range(dimension))
                             for offset in itertools.product(range(block_side),
                                                             repeat=dimension)}
                    require(not retained.intersection(block), "Overlapping tiles")
                    require(all(0 <= value < side for site in block for value in site),
                            "Tile extends beyond the physical lattice")
                    retained.update(block)
                    block_count += 1
                sensors = side**dimension
                require(len(retained) == block_side**dimension * block_count,
                        "Tiling has an incorrect active sensor count")
                require(len(retained) * 2**dimension >= sensors,
                        "Tiling loses more than the stated constant fraction")
                require(2 * dimension * (block_side - 1) <= depth,
                        "Selected block decoder exceeds the depth budget")
                cases.append({"dimension": dimension, "side": side, "depth": depth,
                              "block_side": block_side, "blocks": block_count,
                              "active_sensors": len(retained), "sensors": sensors})
    return cases


def check_phase_average() -> dict:
    cases = []
    largest_error = 0.0
    for visibility in (0.01, 0.2, 0.8, 0.99, 0.9999):
        # One dimensionless logical sensor is enough: the full formula is M^2
        # times this integral.  Nonzero shifts check phase independence too.
        log_visibility = math.log(visibility)
        target = -math.expm1(0.5 * math.log1p(-visibility**2))
        for offset in (0.0, 0.137, 1.1):
            integral, reported_error = quad(
                lambda phase: parity_fi(1, log_visibility, phase + offset),
                0, 2 * math.pi, epsabs=2e-11, epsrel=2e-11, limit=300)
            numerical = integral / (2 * math.pi)
            discrepancy = abs(numerical - target)
            largest_error = max(largest_error, discrepancy)
            require(discrepancy < 2e-10, "Uniform-phase integral identity failed")
            require(reported_error / (2 * math.pi) < 2e-9,
                    "Quadrature did not resolve the requested accuracy")
            cases.append({"visibility": visibility, "offset": offset,
                          "numerical_average": numerical, "formula": target})
    return {"cases": cases, "max_absolute_error": largest_error}


def compare(actual: Any, expected: Any, location: str = "root") -> None:
    """Compare structure exactly and floating values with portable tolerances."""
    if isinstance(expected, dict):
        require(isinstance(actual, dict) and actual.keys() == expected.keys(),
                f"Dictionary keys differ at {location}")
        for key in expected:
            compare(actual[key], expected[key], f"{location}.{key}")
    elif isinstance(expected, list):
        require(isinstance(actual, list) and len(actual) == len(expected),
                f"List length differs at {location}")
        for index, (got, want) in enumerate(zip(actual, expected)):
            compare(got, want, f"{location}[{index}]")
    elif isinstance(expected, float):
        require(isinstance(actual, (float, int)) and math.isfinite(actual)
                and math.isclose(actual, expected, rel_tol=REL_TOL, abs_tol=ABS_TOL),
                f"Floating value differs at {location}: {actual!r} versus {expected!r}")
    else:
        require(type(actual) is type(expected) and actual == expected,
                f"Value differs at {location}: {actual!r} versus {expected!r}")


def run_checks() -> dict:
    return {"schema_version": 1,
            "scope": "Finite construction and phase-integral checks; not an asymptotic proof.",
            "schedules": check_schedules(), "majority": check_majority(),
            "grouping": check_grouping(), "tiling": check_lattice_tiling(),
            "phase_average": check_phase_average()}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path,
                        help="Write recomputed JSON instead of comparing the committed baseline")
    args = parser.parse_args()
    result = run_checks()
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2, allow_nan=False) + "\n",
                               encoding="utf-8")
        action = f"wrote {args.output}"
    else:
        baseline = Path(__file__).with_name("expected_frontier.json")
        require(baseline.is_file(), f"Missing committed baseline: {baseline}")
        compare(result, json.loads(baseline.read_text(encoding="utf-8")))
        action = "matched expected_frontier.json"
    print(json.dumps({
        "status": "pass", "result": action,
        "lattice_schedules": len(result["schedules"]["lattice"]),
        "all_to_all_schedules": len(result["schedules"]["all_to_all"]),
        "majority_cases": len(result["majority"]["cases"]),
        "grouping_cases": len(result["grouping"]["cases"]),
        "incomplete_group_cases": result["grouping"]["incomplete_group_cases"],
        "zero_entangling_depth_cases": result["grouping"]["zero_entangling_depth_cases"],
        "tiling_cases": len(result["tiling"]),
        "phase_integrals": len(result["phase_average"]["cases"]),
        "max_phase_integral_error": result["phase_average"]["max_absolute_error"],
    }, indent=2))


if __name__ == "__main__":
    main()
