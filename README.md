# FX Converter

A lightweight desktop currency converter built with Python and Tkinter.

Fetches live exchange rates via Yahoo Finance and displays the converted amount, rate, and timestamp in a clean GUI window.

## Features

- Live FX rates pulled from Yahoo Finance
- Supports USD, SGD, EUR, GBP, JPY
- Displays converted amount, mid-market rate, and fetch timestamp
- Input validation for non-numeric amounts and same-currency conversion

## Requirements

- Python 3.x
- yfinance

Install dependencies:

```
pip install yfinance
```

## Usage

```
python app.py
```

Enter an amount, select From and To currencies, and click Convert.

## Notes

- Requires an active internet connection
- Rates are Yahoo Finance mid-market prices — not dealing rates
- Built for Windows
