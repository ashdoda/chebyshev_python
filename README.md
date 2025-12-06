# Chebyshev Stock Analyzer

A Python console application that applies **Chebyshev’s Theorem** to historical stock returns.

The tool lets you:

1. Analyze a **single stock ticker** over a chosen date range.
2. Analyze **all S&P 500 tickers** over a chosen date range and list the **Top 10** stocks with the highest empirical fraction of returns within ±k standard deviations of the mean.

Data is pulled live from Yahoo Finance via the `yfinance` library.

---

## Features

- Fetches daily price data from Yahoo Finance.
- Converts prices to **daily returns**.
- Computes:
  - Mean daily return
  - Sample standard deviation
  - Chebyshev interval \([ \mu \pm k\sigma ]\)
  - Theoretical Chebyshev bound: \(1 - 1/k^2\)
  - **Empirical fraction** of returns inside the interval.
- Supports \(k \in \{2, 3, 4, 5\}\) with explanation of what each k means.
- S&P 500 mode:
  - Loads tickers from `sp500_tickers.txt`
  - Runs Chebyshev analysis for each ticker
  - Displays a **Top 10** table sorted by empirical fraction.

---

## Project Structure

```text
.
├── main.py               # Console menu + single-ticker & S&P 500 modes
├── helper.py             # Ticker-level analysis helpers
├── chebyshev.py          # Core math: returns, mean, std dev, Chebyshev summary
├── price_loader.py       # yfinance price-fetching utilities (single & bulk)
├── build_sp500_list.py   # Script to scrape S&P 500 tickers from Wikipedia
├── sp500_tickers.txt     # Cached list of S&P 500 tickers (one per line)
└── README.md             # This file
