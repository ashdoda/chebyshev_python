import matplotlib.pyplot as plt
import numpy as np
from chebyshev import compute_returns

def plot_single_ticker_boxplot(symbol: str, prices: list[float], info: dict):
    """
    Plot a box plot of daily returns for a single ticker and overlay
    Chebyshev bounds (μ ± kσ).
    """

    returns = compute_returns(prices)

    if len(returns) == 0:
        print("Not enough return data to plot.")
        return

    # Extract Chebyshev info
    mean_ret = info["mean"]
    std_dev = info["std_dev"]
    k = info["k"]
    lower = info["lower"]
    upper = info["upper"]

    plt.figure(figsize=(10, 6))

    # Box Plot
    bp = plt.boxplot(
        returns,
        vert=True,
        patch_artist=True,
        boxprops=dict(facecolor='lightblue'),
        medianprops=dict(color='red', linewidth=2),
        whiskerprops=dict(color='black'),
        capprops=dict(color='black'),
        flierprops=dict(marker='o', markerfacecolor='gray', markersize=6, alpha=0.5)
    )

    # Overlay Chebyshev interval
    plt.axhspan(lower, upper, color="yellow", alpha=0.25,
                label=f"Chebyshev Interval (±{k}σ)")

    # Mean line
    plt.axhline(mean_ret, color="black", linestyle="-", linewidth=2,
                label="Mean Return")

    # Labels
    plt.title(f"Box Plot of Daily Returns for {symbol}")
    plt.ylabel("Daily Return")
    plt.xticks([1], [symbol])
    plt.legend()

    plt.tight_layout()
    plt.show()

def plot_sp500_top_boxplots(
    top_symbols: list[str],
    prices_by_symbol: dict[str, list[float]],
    title_suffix: str = ""
):
    """
    Multi-ticker box plot for S&P 500 mode.

    top_symbols: list of ticker symbols to show (e.g., Top 5 or Top 10)
    prices_by_symbol: dict {symbol -> list of prices} from bulk download
    """
    data = []
    labels = []

    for sym in top_symbols:
        prices = prices_by_symbol.get(sym)
        if not prices or len(prices) < 2:
            continue
        returns = compute_returns(prices)
        if len(returns) < 2:
            continue
        data.append(returns)
        labels.append(sym)

    if not data:
        print("No sufficient price/return data available for box plot.")
        return

    plt.figure(figsize=(max(8, len(labels) * 0.7), 5))

    plt.boxplot(
        data,
        vert=True,
        patch_artist=True,
        boxprops=dict(facecolor="lightblue"),
        medianprops=dict(color="red", linewidth=1.5),
        whiskerprops=dict(color="black"),
        capprops=dict(color="black"),
        flierprops=dict(marker="o", markerfacecolor="gray",
                        markersize=4, alpha=0.5),
    )

    plt.xticks(range(1, len(labels) + 1), labels, rotation=45, ha="right")
    plt.ylabel("Daily return")
    plt.title("Box plots of daily returns for S&P 500 top tickers" + title_suffix)
    plt.tight_layout()
    plt.show()

def plot_sp500_top_boxplots_sorted(
    top_results: list[dict],
    prices_by_symbol: dict[str, list[float]],
    k: int,
):
    """
    Horizontal box plots of daily returns for S&P 500 top tickers,
    sorted by volatility (std dev of returns, low → high).

    top_results: list of result dicts (already filtered/sorted by your metric)
                 e.g., results_sorted from run_sp500_mode
    prices_by_symbol: {ticker -> price list} from fetch_bulk_close_prices
    k: Chebyshev k used in the analysis (for title only)
    """

    # First restrict to the tickers we want to plot (e.g., top 10)
    # The caller can pass in top_results[:top_n].
    # Now sort those by volatility (std_dev) ascending:
    sorted_by_vol = sorted(top_results, key=lambda r: r["std_dev"])

    tickers = []
    returns_data = []

    for r in sorted_by_vol:
        symbol = r["ticker"]
        prices = prices_by_symbol.get(symbol)
        if not prices or len(prices) < 2:
            continue

        rets = compute_returns(prices)
        if len(rets) < 2:
            continue

        tickers.append(symbol)
        returns_data.append(rets)

    if not returns_data:
        print("No sufficient data to plot S&P 500 box plots.")
        return

    # Horizontal box plot (vert=False)
    plt.figure(figsize=(10, max(5, len(tickers) * 0.4)))

    plt.boxplot(
        returns_data,
        vert=False,
        labels=tickers,
        patch_artist=True,
        boxprops=dict(facecolor="lightblue", alpha=0.7),
        medianprops=dict(color="red", linewidth=1.5),
        whiskerprops=dict(color="black"),
        capprops=dict(color="black"),
        flierprops=dict(marker="o", markerfacecolor="gray",
                        markersize=4, alpha=0.5),
    )

    plt.xlabel("Daily return")
    plt.ylabel("Ticker (sorted low → high volatility)")
    plt.title(f"S&P 500 top tickers: horizontal box plots (k={k})")

    # Light vertical grid for easier comparison
    plt.grid(axis="x", linestyle="--", alpha=0.4)

    plt.tight_layout()
    plt.show()

def plot_single_ticker_boxplot_horizontal(ticker: str, returns: list[float], k: int | None = None):
    """
    Creates a horizontal box plot of daily returns for a single ticker.
    Optional: draws vertical lines for ±kσ if k is provided.
    """

    if len(returns) < 2:
        print("Not enough return data to plot.")
        return

    # Convert to numpy for stats
    arr = np.array(returns)
    mean = arr.mean()
    std = arr.std(ddof=1)

    fig, ax = plt.subplots(figsize=(10, 4))

    # Horizontal box plot
    ax.boxplot(
        [arr],
        vert=False,
        patch_artist=True,
        boxprops=dict(facecolor="lightblue", alpha=0.5),
        medianprops=dict(color="red", linewidth=1.5),
    )

    ax.set_yticklabels([ticker])
    ax.set_xlabel("Daily Return")
    ax.set_title(f"Horizontal Box Plot of Daily Returns for {ticker}")

    # Optional: draw ±kσ lines
    if k is not None:
        lower = mean - k * std
        upper = mean + k * std
        ax.axvline(lower, color="green", linestyle="--", linewidth=1, label=f"-{k}σ")
        ax.axvline(upper, color="green", linestyle="--", linewidth=1, label=f"+{k}σ")
        ax.axvline(mean, color="black", linestyle="--", linewidth=1, label="Mean")

        ax.legend(loc="upper right")

    plt.tight_layout()
    plt.show()