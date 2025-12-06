Chebyshev Stock Analyzer

A Python command-line application for analyzing stock return distributions using Chebyshev’s Inequality.
This tool allows users to evaluate how frequently returns fall within ±k standard deviations of the mean, without assuming a normal distribution.

Overview

The Chebyshev Stock Analyzer provides:

Analysis of a single stock ticker over a user-defined time period

Batch analysis of all S&P 500 tickers (Top 10 ranked by empirical stability)

Automated S&P 500 ticker list generation

Bulk stock price downloading through yfinance

Consistent, professional table-style output

Clean and modular architecture suitable for extension

The purpose of the project is to compare empirical stock volatility with Chebyshev’s theoretical minimum bound:

𝑃
(
∣
𝑋
−
𝜇
∣
≤
𝑘
𝜎
)
≥
1
−
1
𝑘
2
P(∣X−μ∣≤kσ)≥1−
k
2
1
	​

Features
For each stock analyzed, the tool calculates:

Mean daily return

Standard deviation

Chebyshev lower bound

Empirical percentage of returns within ±kσ

Return interval values

Number of data points

Ranked results for S&P 500 batch mode

Installation

Clone the repository:

git clone https://github.com/ashdoda/chebyshev_python.git
cd chebyshev_python


Install required packages:

pip install -r requirements.txt


Dependencies:

yfinance

pandas

requests

Usage

Run the program:

python main.py


Menu:

==============================
 Chebyshev Stock Analyzer
==============================
1) Analyze a single stock ticker
2) Analyze all S&P 500 stocks (Top 10)
0) Exit

Single-Ticker Analysis

Example input:

Enter stock ticker: AAPL
Enter start date (MM-DD-YYYY): 10-01-2025
Enter end date   (MM-DD-YYYY): 10-31-2025
Enter your choice for k: 2


Sample output:

Rank  Ticker   Empirical%   Cheby%      MeanRet    StdDev     Points
----------------------------------------------------------------------
1     AAPL     90.48        75.00       0.0021      0.0150      21

Interval [±2σ]: [-0.027047, 0.033838]

S&P 500 Mode

The tool downloads price data for all S&P 500 tickers in a single bulk operation.

Example:

Fetching bulk price data for 503 tickers...
Running Chebyshev analysis...

Top 10 tickers by empirical fraction within ±2σ:


Sample output:

Rank  Ticker   Empirical%   Cheby%      MeanRet    StdDev     Points
----------------------------------------------------------------------
1     APD      100.00       75.00     -0.0044      0.0110      21
2     ALLE     100.00       75.00     -0.0031      0.0127      21
...

Generating the S&P 500 Ticker List

Run:

python build_sp500_list.py


This will:

Scrape the S&P 500 constituents from Wikipedia

Normalize ticker formats (e.g., BRK.B → BRK-B)

Write them to sp500_tickers.txt

Project Structure
chebyshev_python/
│
├── main.py                # CLI and program flow
├── chebyshev.py           # Core math functions
├── helper.py              # Wrapper utilities
├── price_loader.py        # Price fetching (bulk + single)
├── build_sp500_list.py    # Downloads S&P 500 ticker list
├── sp500_tickers.txt      # Cached tickers
├── requirements.txt
└── README.md

Example Interpretation

If empirical percentage > Chebyshev bound:

The stock is more stable than the theorem guarantees.

If empirical percentage is close to the bound:

The stock’s return distribution is high variance or irregular.

This tool helps highlight which stocks behave more consistently over the selected period.

Troubleshooting
"No data returned for ticker"

Occurs when:

The date range is in the future

The ticker is invalid or delisted

The market was closed during the range

All tickers fail in S&P 500 mode

Common causes:

Future date ranges

Internet or firewall blocking Yahoo Finance

Temporary rate limiting

License

This project is open-source.
If you'd like, I can generate a full MIT License file.

Contributing

Pull requests and feature suggestions are welcome.
