
import yfinance as yf
import pandas as pd
from typing import List, Dict

def fetch_close_prices(ticker: str, start: str, end: str) -> List[float]:
    """
    Fetch daily close or adjusted close prices for a ticker between start and end dates (YYYY-MM-DD).
    Handles both older and newer yfinance column formats.
    Returns a list of floats.
    """
    data = yf.download(ticker, start=start, end=end, progress=False)

    if data.empty:
        raise ValueError(
            f"No data returned for ticker '{ticker}'. "
            "Check the ticker symbol and date range."
        )

    # If it's a MultiIndex (more common with multiple tickers), try to simplify
    if isinstance(data.columns, pd.MultiIndex):
        # Try to pick the first level that looks like 'Adj Close' or 'Close'
        level0 = data.columns.get_level_values(0)
        if "Adj Close" in level0:
            series = data["Adj Close"].iloc[:, 0]
        elif "Close" in level0:
            series = data["Close"].iloc[:, 0]
        else:
            raise RuntimeError(
                f"Expected 'Adj Close' or 'Close' in MultiIndex columns, got: {list(set(level0))}"
            )
    else:
        # Regular single-level columns
        if "Adj Close" in data.columns:
            series = data["Adj Close"]
        elif "Close" in data.columns:
            series = data["Close"]
        else:
            raise RuntimeError(
                f"Expected 'Adj Close' or 'Close' in columns, got: {list(data.columns)}"
            )

    closes = series.dropna().tolist()
    return closes

def fetch_bulk_close_prices(
    tickers: List[str], start: str, end: str
) -> Dict[str, List[float]]:
    """
    Fetch daily close/adjusted-close prices for MANY tickers at once.
    Uses yfinance's internal threading instead of our own.
    Returns dict[ticker] -> list of floats.
    """
    data = yf.download(
        tickers,
        start=start,
        end=end,
        progress=False,
        group_by="ticker",   # yfinance groups columns by ticker/field
        threads=True,        # let yfinance manage concurrency
    )

    if data.empty:
        raise ValueError("No data returned for bulk download.")

    result: Dict[str, List[float]] = {}

    # Handle MultiIndex vs single columns
    if isinstance(data.columns, pd.MultiIndex):
        lvl0 = data.columns.get_level_values(0)
        lvl1 = data.columns.get_level_values(1)

        # Two common layouts:
        # 1) ('Adj Close', 'AAPL'), ('Adj Close', 'MSFT'), ...
        # 2) ('AAPL', 'Adj Close'), ('MSFT', 'Adj Close'), ...
        for ticker in tickers:
            series = None

            # layout 1: price-field first
            if ("Adj Close", ticker) in data.columns:
                series = data[("Adj Close", ticker)]
            elif ("Close", ticker) in data.columns:
                series = data[("Close", ticker)]

            # layout 2: ticker first
            elif (ticker, "Adj Close") in data.columns:
                series = data[(ticker, "Adj Close")]
            elif (ticker, "Close") in data.columns:
                series = data[(ticker, "Close")]

            if series is not None:
                result[ticker] = series.dropna().tolist()
            # if not found, we just skip that ticker

    else:
        # Single-level columns (rare in bulk mode, but keep it robust)
        for ticker in tickers:
            col_adj = f"{ticker} Adj Close"
            col_close = f"{ticker} Close"

            if col_adj in data.columns:
                series = data[col_adj]
            elif col_close in data.columns:
                series = data[col_close]
            else:
                continue

            result[ticker] = series.dropna().tolist()

    return result


import pandas as pd

def fetch_price_dataframe(ticker: str, start: str, end: str) -> pd.DataFrame:
    """
    Fetch daily close/adjusted-close prices for a ticker between start and end
    dates (YYYY-MM-DD) and return a DataFrame with columns:
        Date, Price, Ticker
    This is for debugging / CSV export.
    """
    data = yf.download(ticker, start=start, end=end, progress=False)

    if data.empty:
        raise ValueError(
            f"No data returned for ticker '{ticker}'. "
            "Check the ticker symbol and date range."
        )

    # Handle MultiIndex (common with yfinance)
    if isinstance(data.columns, pd.MultiIndex):
        # Look for Adjusted Close first
        if ("Adj Close" in data.columns.get_level_values(0)):
            series = data["Adj Close"].iloc[:, 0]
        elif ("Close" in data.columns.get_level_values(0)):
            series = data["Close"].iloc[:, 0]
        else:
            raise RuntimeError(
                f"Expected 'Adj Close' or 'Close' in MultiIndex columns, got: {data.columns}"
            )
    else:
        # Single-level columns
        if "Adj Close" in data.columns:
            series = data["Adj Close"]
        elif "Close" in data.columns:
            series = data["Close"]
        else:
            raise RuntimeError(
                f"Expected 'Adj Close' or 'Close', got: {list(data.columns)}"
            )

    df = series.to_frame(name="Price").reset_index()
    df["Ticker"] = ticker.upper()
    return df


# Debug block
if __name__ == "__main__":
    print("Names in price_loader containing 'fetch':")
    print([name for name in globals() if "fetch" in name.lower()])
