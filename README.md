Chebyshev Stock Analyzer
==============================

A Python command-line application for analyzing stock return distributions using Chebyshev’s Inequality.
This tool evaluates how often stock returns fall within ±k standard deviations of the mean, without assuming a normal distribution.

Overview

The Chebyshev Stock Analyzer provides:

- Analysis of a single stock ticker over a specified date range
- Batch processing of all S&P 500 tickers with ranking of the top ten
- Automated scraping of S&P 500 tickers from Wikipedia
- Bulk historical price downloading via yfinance
- Consistent tabular output for both single and batch analysis

The system compares empirical volatility to Chebyshev’s theoretical lower bound:

P(|X − μ| ≤ kσ) ≥ 1 − 1/k²

Installation

Clone the repository:

git clone https://github.com/ashdoda/chebyshev_python.git
cd chebyshev_python

Install dependencies:

pip install -r requirements.txt

Required packages:
- yfinance
- pandas
- requests

Usage

Run the application:

python main.py

Main menu:

<img width="363" height="150" alt="image" src="https://github.com/user-attachments/assets/dcde8b76-e534-4a88-b911-faf47a8b79b0" />

Once either mode is selected:

<img width="721" height="309" alt="image" src="https://github.com/user-attachments/assets/3949cdad-cdc5-4f2d-8048-4d31f1f1b5d8" />

Single-Ticker Analysis Example Output:

<img width="647" height="156" alt="image" src="https://github.com/user-attachments/assets/3975248b-827d-4a18-aa52-ac05878a15f9" />


S&P 500 Batch Mode Example Output:

<img width="649" height="332" alt="image" src="https://github.com/user-attachments/assets/54700fe7-e1ca-4ece-a8ab-cb1c7fe010f5" />

Interpretation of Results:

- Empirical % > Chebyshev bound → more stable than theoretical minimum
- Empirical % near Chebyshev bound → higher volatility

Troubleshooting:

- No data returned: invalid date range, delisted ticker, Yahoo API limit
- Batch returns zero: future dates, network issue, rate limiting

License: MIT License (see LICENSE file)

Contributing:

Pull requests and improvements welcome.
