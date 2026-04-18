import yfinance as yf
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox
import os
import sys

# When running as a .exe (PyInstaller), use the folder the exe lives in.
# When running as a .py script, use the folder the script lives in.
if getattr(sys, "frozen", False):
    _app_dir = os.path.dirname(sys.executable)
else:
    _app_dir = os.path.dirname(os.path.abspath(__file__))

_log_path = os.path.join(_app_dir, "fx_converter_log.txt")

# Appends a single plain-English line to the log file, with the current date and time.
def write_log(message):
    timestamp = datetime.now().strftime("%d %b %Y, %I:%M %p")
    with open(_log_path, "a", encoding="utf-8") as f:
        f.write(f"{timestamp} — {message}\n")

# Fetches the live exchange rate between two currencies using Yahoo Finance.
# Returns a dict with the rate, the currency pair ticker, and a timestamp.
def get_fx_rate(from_currency, to_currency):
    ticker_symbol = f"{from_currency}{to_currency}=X"
    ticker = yf.Ticker(ticker_symbol)
    data = ticker.history(period="1d", interval="1m")

    if data.empty:
        raise ValueError(f"No data returned for {ticker_symbol}. Check the currency codes.")

    rate = data["Close"].iloc[-1]
    fetched_at = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    return {
        "ticker": ticker_symbol,
        "rate": rate,
        "fetched_at": fetched_at
    }


# Reads the inputs, calls get_fx_rate, and updates the result labels in the window.
# This function is called every time the Convert button is clicked.
def on_convert(amount_var, from_var, to_var, result_label, rate_label, time_label):
    # Read current values from the input widgets.
    from_currency = from_var.get()
    to_currency = to_var.get()

    # Validate the amount field before making a network call.
    try:
        amount = float(amount_var.get().replace(",", ""))
    except ValueError:
        write_log(f"Invalid amount entered: '{amount_var.get()}' is not a number.")
        messagebox.showerror("Invalid input", "Please enter a valid number in the Amount field.")
        return

    # Guard against converting a currency to itself.
    if from_currency == to_currency:
        write_log(f"Conversion skipped: From and To currencies are both {from_currency}.")
        messagebox.showwarning("Same currency", "From and To currencies are the same.")
        return

    # Disable the button and show a status message while fetching.
    result_label.config(text="Fetching rate...")
    rate_label.config(text="")
    time_label.config(text="")
    result_label.update()  # Force the label to redraw immediately.

    # Fetch the live rate and update all three display labels.
    try:
        fx = get_fx_rate(from_currency, to_currency)
        converted = amount * fx["rate"]

        # Format large numbers with commas for readability (e.g. 13,420.50).
        amount_fmt = f"{amount:,.2f}"
        converted_fmt = f"{converted:,.2f}"

        result_label.config(text=f"{amount_fmt} {from_currency} = {converted_fmt} {to_currency}")
        rate_label.config(text=f"Rate: 1 {from_currency} = {fx['rate']:.6f} {to_currency}")
        time_label.config(text=f"Fetched at: {fx['fetched_at']}")

        write_log(
            f"Converted {amount_fmt} {from_currency} to {converted_fmt} {to_currency} "
            f"(rate: 1 {from_currency} = {fx['rate']:.6f} {to_currency})."
        )

    except Exception as e:
        write_log(f"Failed to fetch rate for {from_currency} to {to_currency}. Reason: {e}")
        messagebox.showerror("Fetch failed", str(e))
        result_label.config(text="Result will appear here")


# Builds and launches the main application window.
def build_gui():
    currencies = ["USD", "SGD", "EUR", "GBP", "JPY", "AUD", "CHF"]

    root = tk.Tk()
    root.title("FX Converter")
    root.resizable(False, False)

    main_frame = ttk.Frame(root, padding=20)
    main_frame.grid(row=0, column=0)

    # --- Amount input ---
    ttk.Label(main_frame, text="Amount:").grid(row=0, column=0, sticky="w", pady=4)

    amount_var = tk.StringVar(value="10000")
    ttk.Entry(main_frame, textvariable=amount_var, width=18).grid(
        row=0, column=1, columnspan=2, sticky="w", pady=4
    )

    # --- From currency dropdown ---
    ttk.Label(main_frame, text="From:").grid(row=1, column=0, sticky="w", pady=4)

    from_var = tk.StringVar(value="USD")
    ttk.Combobox(
        main_frame, textvariable=from_var,
        values=currencies, state="readonly", width=8
    ).grid(row=1, column=1, sticky="w", pady=4)

    # --- To currency dropdown ---
    ttk.Label(main_frame, text="To:").grid(row=2, column=0, sticky="w", pady=4)

    to_var = tk.StringVar(value="SGD")
    ttk.Combobox(
        main_frame, textvariable=to_var,
        values=currencies, state="readonly", width=8
    ).grid(row=2, column=1, sticky="w", pady=4)

    # --- Result labels ---
    result_label = ttk.Label(main_frame, text="Result will appear here", font=("Helvetica", 11, "bold"))
    result_label.grid(row=4, column=0, columnspan=3, pady=(12, 2))

    rate_label = ttk.Label(main_frame, text="", foreground="grey")
    rate_label.grid(row=5, column=0, columnspan=3)

    time_label = ttk.Label(main_frame, text="", foreground="grey")
    time_label.grid(row=6, column=0, columnspan=3)

    # --- Convert button — wired to on_convert via lambda ---
    # lambda is used so we can pass arguments to on_convert when the button is clicked.
    ttk.Button(
        main_frame,
        text="Convert",
        command=lambda: on_convert(amount_var, from_var, to_var, result_label, rate_label, time_label)
    ).grid(row=3, column=0, columnspan=3, pady=12)

    root.mainloop()


# --- Entry point ---
if __name__ == "__main__":
    build_gui()
