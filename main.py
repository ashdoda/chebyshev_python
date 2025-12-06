# main.py

import datetime
import matplotlib.pyplot as plt
from price_loader import fetch_bulk_close_prices, fetch_close_prices
from helper import analyze_ticker
from chebyshev import chebyshev_bound_for_k, compute_returns
from viz import plot_single_ticker_boxplot_horizontal, plot_sp500_top_boxplots_sorted


def prompt_date(msg: str) -> str:
    """
    Prompt the user for a date in MM-DD-YYYY format.
    Convert to YYYY-MM-DD for internal use (yfinance requirement).
    """
    while True:
        raw = input(msg).strip()

        try:
            # Parse MM-DD-YYYY
            dt = datetime.datetime.strptime(raw, "%m-%d-%Y")
            # Convert to YYYY-MM-DD
            return dt.strftime("%Y-%m-%d")

        except ValueError:
            print("Invalid date format. Please use MM-DD-YYYY (e.g. 10-05-2025).")


def load_sp500_tickers(path: str = "sp500_tickers.txt") -> list[str]:
    """
    Load S&P 500 tickers from a text file.
    Each line: one ticker. Blank lines and lines starting with '#' are ignored.
    """
    tickers: list[str] = []
    try:
        with open(path, "r") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                tickers.append(line.upper())
    except FileNotFoundError:
        print(f"Could not find {path}. Make sure it exists in the project folder.")
    return tickers


def prompt_k_value() -> int:
    """
    Ask the user for a k value (2, 3, 4, 5) and show what each choice represents.
    """
    print("\nChoose how wide you want the Chebyshev interval to be.\n")
    print("Chebyshev's theorem says: at least (1 - 1/k²) of values")
    print("should lie within ±k standard deviations of the mean.\n")

    k_options = [2, 3, 4, 5]
    for k in k_options:
        bound_pct = chebyshev_bound_for_k(k) * 100
        if k == 2:
            desc = "moderate band (at least ~75% of returns within ±2σ)"
        elif k == 3:
            desc = "wider band (at least ~88.89% of returns within ±3σ)"
        elif k == 4:
            desc = "very wide band (at least ~93.75% of returns within ±4σ)"
        else:  # k == 5
            desc = "extremely wide band (at least ~96% of returns within ±5σ)"

        print(f"{k}) k = {k}: {desc}")

    valid_k = set(k_options)

    while True:
        choice = input("\nEnter your choice for k (2, 3, 4, or 5): ").strip()
        if not choice.isdigit():
            print("Please enter a number: 2, 3, 4, or 5.")
            continue

        k = int(choice)
        if k in valid_k:
            return k
        else:
            print("Invalid choice. Please enter 2, 3, 4, or 5.")


def run_single_ticker_mode():
    """
    Option 1: Analyze a single stock ticker with Chebyshev's theorem.
    Output is formatted to match the Top 10 S&P table for consistency.
    """
    print("\n=== Single-Ticker Chebyshev Analysis ===")

    symbol = input("Enter stock ticker (e.g. AAPL): ").strip().upper()

    # Get start date in YYYY-MM-DD (user enters MM-DD-YYYY)
    start = prompt_date("Enter start date (MM-DD-YYYY): ")
    start_dt = datetime.datetime.strptime(start, "%Y-%m-%d")

    # Make sure end date is AFTER start date
    while True:
        end = prompt_date("Enter end date   (MM-DD-YYYY): ")
        end_dt = datetime.datetime.strptime(end, "%Y-%m-%d")
        if end_dt <= start_dt:
            print("End date must be AFTER start date. Please try again.")
        else:
            break

    k = prompt_k_value()

    try:
        prices = fetch_close_prices(symbol, start, end)
        if len(prices) < 2:
            print(f"Not enough price data for {symbol} in that date range.")
            return

        info = analyze_ticker(symbol, prices, k=k, verbose=False)

    except Exception as e:
        print(f"Error analyzing {symbol}: {e}")
        return

    # Convert back to MM-DD-YYYY for display
    start_disp = start_dt.strftime("%m-%d-%Y")
    end_disp = end_dt.strftime("%m-%d-%Y")

    print(f"\nChebyshev analysis for {symbol} (k = {k})")
    print(f"Date range: {start_disp} to {end_disp}\n")

    print(f"{'Rank':<5} {'Ticker':<8} {'Empirical%':<12} {'Cheby%':<12} "
          f"{'MeanRet':<10} {'StdDev':<10} {'Points':<8}")
    print("-" * 70)

    emp_pct = info["empirical_fraction_in_k"] * 100
    cheb_pct = info["chebyshev_bound"] * 100
    mean_ret = info["mean"]
    std_dev = info["std_dev"]
    points = info["data_points"]

    print(f"{1:<5} {info['ticker']:<8} {emp_pct:<12.2f} {cheb_pct:<12.2f} "
          f"{mean_ret:<10.4f} {std_dev:<10.4f} {points:<8}")

    print("\nInterval [±{}σ]: [{:.6f}, {:.6f}]".format(
        k, info["lower"], info["upper"]
    ))
    plot_choice = input("Would you like to see a box plot of returns? (y/n): ").strip().lower()
    if plot_choice == "y":
     plot_single_ticker_boxplot_horizontal(symbol, compute_returns(prices), k)




def run_sp500_mode():
    """
    Option 2: Chebyshev analysis on all S&P 500 tickers (Top 10).
    Uses a single bulk yfinance download instead of our own threads.
    Dates are entered as MM-DD-YYYY but converted to YYYY-MM-DD internally.
    """
    print("\n=== S&P 500 Chebyshev Analysis (Top 10) ===")

    tickers = load_sp500_tickers()
    if not tickers:
        print("No tickers loaded. Check sp500_tickers.txt.")
        return

    print(f"Loaded {len(tickers)} tickers from sp500_tickers.txt.")

    # Get start date in YYYY-MM-DD (user enters MM-DD-YYYY)
    start = prompt_date("Enter start date (MM-DD-YYYY): ")
    start_dt = datetime.datetime.strptime(start, "%Y-%m-%d")

    # Ensure end date is AFTER start date
    while True:
        end = prompt_date("Enter end date   (MM-DD-YYYY): ")
        end_dt = datetime.datetime.strptime(end, "%Y-%m-%d")
        if end_dt <= start_dt:
            print("End date must be AFTER start date. Please try again.")
        else:
            break

    k = prompt_k_value()

    # For display, convert back to MM-DD-YYYY
    start_disp = start_dt.strftime("%m-%d-%Y")
    end_disp = end_dt.strftime("%m-%d-%Y")

    print(f"\nDate range: {start_disp} to {end_disp}")
    print(f"Fetching bulk price data for {len(tickers)} tickers...")

    try:
        prices_by_symbol = fetch_bulk_close_prices(tickers, start, end)
    except Exception as e:
        print(f"Error during bulk download: {e}")
        return

    if not prices_by_symbol:
        print("No price data fetched successfully.")
        return

    print("Running Chebyshev analysis...\n")

    results: list[dict] = []
    failures: list[str] = []

    for idx, symbol in enumerate(tickers, start=1):
        prices = prices_by_symbol.get(symbol)
        if not prices or len(prices) < 2:
            failures.append(symbol)
            continue

        try:
            info = analyze_ticker(symbol, prices, k=k, verbose=False)
            results.append(dict(info))
        except Exception:
            failures.append(symbol)

        if idx % 25 == 0 or idx == len(tickers):
            print(f"Progress: {idx}/{len(tickers)} tickers processed")

    if not results:
        print("No successful analyses completed.")
        return

    results_sorted = sorted(
        results,
        key=lambda r: r["empirical_fraction_in_k"],
        reverse=True,
    )

    top_n = min(10, len(results_sorted))
    print(f"\nTop {top_n} tickers by empirical fraction within ±{k}σ:\n")
    print(f"{'Rank':<5} {'Ticker':<8} {'Empirical%':<12} {'Cheby%':<12} "
          f"{'MeanRet':<10} {'StdDev':<10} {'Points':<8}")
    print("-" * 70)

    for i, r in enumerate(results_sorted[:top_n], start=1):
        emp_pct = r["empirical_fraction_in_k"] * 100
        cheb_pct = r["chebyshev_bound"] * 100
        mean_ret = r["mean"]
        std_dev = r["std_dev"]
        points = r["data_points"]
        print(f"{i:<5} {r['ticker']:<8} {emp_pct:<12.2f} {cheb_pct:<12.2f} "
              f"{mean_ret:<10.4f} {std_dev:<10.4f} {points:<8}")

    if failures:
        print(f"\nTickers with errors or insufficient data: {len(failures)}")
    
    choice = input("\nWould you like to see a bar chart of the Top 10 (sorted by volatility)? (y/n): ").strip().lower()
    if choice == "y":
       top_n = min(10, len(results_sorted))
       top_slice = results_sorted[:top_n]
       plot_sp500_top_boxplots_sorted(top_slice, prices_by_symbol, k)


def main_menu():
    while True:
        print("\n==============================")
        print(" Chebyshev Stock Analyzer")
        print("==============================")
        print("1) Analyze a single stock ticker")
        print("2) Analyze all S&P 500 stocks (Top 10)")
        print("0) Exit")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            run_single_ticker_mode()
        elif choice == "2":
            run_sp500_mode()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 0.")


if __name__ == "__main__":
    main_menu()
