# helper.py (or combine inside main.py)

from typing import List, Dict, Any
from chebyshev import compute_returns, chebyshev_summary

def analyze_ticker(ticker: str, prices: List[float], k: int, verbose: bool = True) -> Dict[str, Any]:
    """
    Reusable helper for both single-ticker mode and S&P batch mode.
    """
    returns = compute_returns(prices)

    if len(returns) < 2:
        raise ValueError(f"Not enough data for ticker {ticker}.")

    result = chebyshev_summary(returns, k)

    if verbose:
        print("\n=======================================")
        print(f"Chebyshev Analysis for {ticker.upper()} (k = {k})")
        print("=======================================\n")
        print(f"Total data points: {result.num_points}")
        print(f"Mean daily return: {result.mean:.6f}")
        print(f"Std deviation:     {result.std_dev:.6f}")
        print(f"Interval [{k}σ]:   [{result.lower_bound_value:.6f}, {result.upper_bound_value:.6f}]")
        print(f"Chebyshev bound:   {result.chebyshev_bound*100:.2f}% (minimum expectation)")
        print(f"Empirical % in kσ: {result.empirical_fraction_within_k*100:.2f}%")
        print("---------------------------------------\n")

    return {
        "ticker": ticker.upper(),
        "k": k,
        "mean": result.mean,
        "std_dev": result.std_dev,
        "chebyshev_bound": result.chebyshev_bound,
        "empirical_fraction_in_k": result.empirical_fraction_within_k,
        "data_points": result.num_points,
        "lower": result.lower_bound_value,
        "upper": result.upper_bound_value,
    }
