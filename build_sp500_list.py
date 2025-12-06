# build_sp500_list.py

import requests
import pandas as pd


def fetch_sp500():
    """
    Scrapes the S&P 500 ticker list from Wikipedia.
    Returns a clean list of ticker symbols.
    """
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

    print("Downloading S&P 500 company list from Wikipedia...")

    # Use a browser-like User-Agent so we don't get 403 Forbidden
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/122.0.0.0 Safari/537.36"
        )
    }

    resp = requests.get(url, headers=headers)
    resp.raise_for_status()  # will raise HTTPError if not 200

    # Parse tables from the downloaded HTML
    tables = pd.read_html(resp.text)
    df = tables[0]  # first table is the index components

    # Wikipedia column is usually named "Symbol"
    if "Symbol" not in df.columns:
        raise RuntimeError(f"'Symbol' column not found. Columns are: {df.columns}")

    tickers = df["Symbol"].tolist()

    cleaned = []
    for t in tickers:
        t = t.upper().strip()
        # Wikipedia uses BRK.B, BF.B, etc.; yfinance expects BRK-B, BF-B
        t = t.replace(".", "-")
        cleaned.append(t)

    return cleaned


def save_to_file(tickers, path: str = "sp500_tickers.txt"):
    """
    Saves the ticker list to a text file, one ticker per line.
    """
    with open(path, "w") as f:
        for t in tickers:
            f.write(t + "\n")

    print(f"Saved {len(tickers)} tickers to {path}")


if __name__ == "__main__":
    tickers = fetch_sp500()
    save_to_file(tickers)
