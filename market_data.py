import pandas as pd
import yfinance as yf

def safe_get_history(symbol, period="6mo", interval="1d"):
    try:
        df = yf.download(
            symbol,
            period=period,
            interval=interval,
            progress=False,
            auto_adjust=False
        )

        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        if df.empty:
            return pd.DataFrame()

        return df.dropna(how="all")
    except Exception:
        return pd.DataFrame()

def safe_get_current_price(symbol):
    hist = safe_get_history(symbol, period="5d", interval="1d")

    if hist.empty or "Close" not in hist.columns:
        return None

    close_series = hist["Close"].dropna()
    if close_series.empty:
        return None

    return float(close_series.iloc[-1])

def get_market_data(symbol):
    hist = safe_get_history(symbol, period="5d", interval="1d")

    if hist.empty or "Close" not in hist.columns:
        return {"symbol": symbol, "price": 0.0, "change_percent": 0.0}

    close_series = hist["Close"].dropna()
    if close_series.empty:
        return {"symbol": symbol, "price": 0.0, "change_percent": 0.0}

    last_price = float(close_series.iloc[-1])

    if len(close_series) >= 2:
        prev_price = float(close_series.iloc[-2])
        change_percent = ((last_price - prev_price) / prev_price) * 100 if prev_price else 0.0
    else:
        change_percent = 0.0

    return {
        "symbol": symbol,
        "price": round(last_price, 2),
        "change_percent": round(change_percent, 2)
    }

def get_index_data(symbol, label):
    hist = safe_get_history(symbol, period="5d", interval="1d")

    if hist.empty or "Close" not in hist.columns:
        return {
            "label": label,
            "price": 0.0,
            "change": 0.0,
            "change_percent": 0.0
        }

    close_series = hist["Close"].dropna()

    if close_series.empty:
        return {
            "label": label,
            "price": 0.0,
            "change": 0.0,
            "change_percent": 0.0
        }

    last_price = float(close_series.iloc[-1])

    if len(close_series) >= 2:
        prev_price = float(close_series.iloc[-2])
        change = last_price - prev_price
        change_percent = (change / prev_price) * 100 if prev_price else 0.0
    else:
        change = 0.0
        change_percent = 0.0

    return {
        "label": label,
        "price": round(last_price, 2),
        "change": round(change, 2),
        "change_percent": round(change_percent, 2)
    }

def get_stock_info(symbol):
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        return {
            "sector": info.get("sector", "N/A"),
            "industry": info.get("industry", "N/A"),
            "market_cap": info.get("marketCap", "N/A"),
            "pe": info.get("trailingPE", "N/A"),
            "pb": info.get("priceToBook", "N/A"),
            "dividend_yield": info.get("dividendYield", "N/A"),
            "beta": info.get("beta", "N/A"),
            "fifty_two_week_high": info.get("fiftyTwoWeekHigh", "N/A"),
            "fifty_two_week_low": info.get("fiftyTwoWeekLow", "N/A"),
            "book_value": info.get("bookValue", "N/A"),
            "eps": info.get("trailingEps", "N/A")
        }
    except Exception:
        return {
            "sector": "N/A", "industry": "N/A", "market_cap": "N/A",
            "pe": "N/A", "pb": "N/A", "dividend_yield": "N/A",
            "beta": "N/A", "fifty_two_week_high": "N/A",
            "fifty_two_week_low": "N/A", "book_value": "N/A", "eps": "N/A"
        }