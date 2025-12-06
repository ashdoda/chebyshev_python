# chebyshev.py

from __future__ import annotations
from dataclasses import dataclass
from typing import List
import math

# ------------------------------
# Dataclass to hold results
# ------------------------------
@dataclass
class ChebyshevResult:
    k: float
    mean: float
    std_dev: float
    lower_bound_value: float
    upper_bound_value: float
    chebyshev_bound: float
    empirical_fraction_within_k: float
    num_points: int


# ------------------------------
# Core math utilities
# ------------------------------
def compute_returns(prices: List[float]) -> List[float]:
    """
    Convert price list → daily returns.
    """
    returns: List[float] = []
    if len(prices) < 2:
        return returns

    for i in range(1, len(prices)):
        p_prev = prices[i - 1]
        p_curr = prices[i]
        if p_prev == 0:
            continue
        r = (p_curr - p_prev) / p_prev
        returns.append(r)

    return returns


def mean(values: List[float]) -> float:
    if not values:
        raise ValueError("mean() requires at least one value")
    return sum(values) / len(values)


def std_dev(values: List[float], sample: bool = True) -> float:
    n = len(values)
    if n < 2:
        raise ValueError("std_dev() requires at least two values")

    m = mean(values)
    var_sum = sum((x - m)**2 for x in values)
    denom = n - 1 if sample else n
    variance = var_sum / denom
    return math.sqrt(variance)


# ------------------------------
# Chebyshev Theorem
# ------------------------------
def chebyshev_bound_for_k(k: float) -> float:
    """
    Chebyshev lower bound: 1 - 1/k^2
    """
    if k <= 1:
        raise ValueError("k must be > 1 for Chebyshev’s inequality")
    return 1.0 - 1.0 / (k * k)


def chebyshev_summary(values: List[float], k: float) -> ChebyshevResult:
    """
    Compute Chebyshev interval + empirical comparison.
    """
    if len(values) < 2:
        raise ValueError("chebyshev_summary() requires ≥ 2 points")

    mu = mean(values)
    sigma = std_dev(values)

    lower_val = mu - k * sigma
    upper_val = mu + k * sigma

    count_in_range = sum(1 for x in values if lower_val <= x <= upper_val)
    n = len(values)
    empirical_fraction = count_in_range / n

    bound = chebyshev_bound_for_k(k)

    return ChebyshevResult(
        k=k,
        mean=mu,
        std_dev=sigma,
        lower_bound_value=lower_val,
        upper_bound_value=upper_val,
        chebyshev_bound=bound,
        empirical_fraction_within_k=empirical_fraction,
        num_points=n
    )
