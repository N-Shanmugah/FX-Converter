# FX Converter — Project Instructions for Claude Code

## What This App Does

A lightweight desktop currency converter for Windows.

- Fetches live FX rates from Yahoo Finance via the `yfinance` library
- User enters an amount, selects a From and To currency, and clicks Convert
- Displays: converted amount, mid-market rate (6 decimal places), and fetch timestamp
- Input validation covers: non-numeric amounts, same-currency selection
- No database, no config files, no local state — stateless on every conversion

Supported currencies: USD, SGD, EUR, GBP, JPY, AUD, CHF

## Tech Stack

| Component | Library | Notes |
|---|---|---|
| GUI framework | `tkinter` + `ttk` | Python stdlib — no install required |
| FX data | `yfinance` 1.2.1 | Yahoo Finance mid-market rates |
| Packaging | PyInstaller | Spec file: `FX Converter.spec` |
| Environment | Python 3, `venv` | Windows; deps pinned in `requirements.txt` |

`yfinance` is the only non-stdlib dependency used by the app itself. The rest of `requirements.txt` is its transitive dependency tree.

## Code Structure

Everything lives in a single file: `app.py` (129 lines, 3 functions).

```
app.py
├── get_fx_rate(from_currency, to_currency)   # Data layer
├── on_convert(amount_var, from_var, to_var,  # Event handler
│              result_label, rate_label,
│              time_label)
├── build_gui()                                # GUI construction + mainloop
└── if __name__ == "__main__": build_gui()    # Entry point
```

### Function responsibilities

**`get_fx_rate`** — pure data function. Constructs a Yahoo Finance ticker symbol (e.g. `USDSGD=X`), fetches 1-day 1-minute history, returns the last close price as a dict: `{ticker, rate, fetched_at}`. Raises `ValueError` if no data is returned.

**`on_convert`** — UI event handler wired to the Convert button via `lambda`. Reads widget variables, validates input, calls `get_fx_rate`, formats numbers with commas, and updates the three result labels. Shows `messagebox` dialogs on errors.

**`build_gui`** — builds the entire window using `ttk` widgets on a grid layout. Defines the currency list. Creates all widget variables and labels, then calls `root.mainloop()`.

## Running and Packaging

**Run from source (VS Code terminal, bash):**
```bash
python app.py
```

**Rebuild the .exe after any code change:**
```bash
pyinstaller "FX Converter.spec"
```
Output lands in `dist/`. The spec is already configured: no console window, UPX compression, single-file bundle.

**Install dependencies into the venv:**
```bash
pip install -r requirements.txt
```

## Development Rules

1. **Single-file discipline.** Keep all logic in `app.py`. Only split into multiple files if the file exceeds ~300 lines or a genuinely separate concern emerges (e.g. a separate data module). Do not create helper files speculatively.

2. **Currency list lives in `build_gui`.** The `currencies` list at the top of `build_gui()` is the single place to add or remove currencies. Do not hardcode currency values elsewhere.

3. **Always use a venv.** Never install packages globally. The venv is at `venv/` and is excluded from git.

4. **Rebuild the exe after source changes.** The `dist/` folder is not auto-updated. If you change `app.py`, remind the user to run `pyinstaller "FX Converter.spec"`.

5. **yfinance is the sole data source.** Do not add a fallback API (e.g. Open Exchange Rates, Fixer) without explicit user confirmation. Rate-source changes have operational implications.

6. **Comment every function.** A plain-English comment block above each function is the established pattern in this project. Maintain it for any new functions.

7. **No external data files.** The app is intentionally self-contained. Do not introduce config files, JSON assets, or SQLite databases unless the user explicitly asks for persistent state.

8. **This is a Windows app.** File paths, shell commands, and packaging all target Windows. Do not introduce platform-specific code that breaks on Windows.

## What Does NOT Exist (Do Not Assume)

- No test suite
- No logging
- No settings/preferences persistence
- No rate caching or offline fallback
- No multi-window navigation
- No async/threading (the UI freezes briefly on fetch — this is acceptable for the current scope)
