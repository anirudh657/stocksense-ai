import pandas as pd

def compute_technicals(chart_data):
    df = chart_data.copy()

    if df.empty or "Close" not in df.columns:
        return df, {
            "RSI": "N/A", "RSI Signal": "N/A", "Trend": "N/A",
            "MACD Signal": "N/A", "SMA20": "N/A", "SMA50": "N/A"
        }

    df["SMA20"] = df["Close"].rolling(20).mean()
    df["SMA50"] = df["Close"].rolling(50).mean()

    delta = df["Close"].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(14).mean()
    avg_loss = loss.rolling(14).mean()
    rs = avg_gain / avg_loss
    df["RSI"] = 100 - (100 / (1 + rs))

    ema12 = df["Close"].ewm(span=12, adjust=False).mean()
    ema26 = df["Close"].ewm(span=26, adjust=False).mean()
    df["MACD"] = ema12 - ema26
    df["Signal"] = df["MACD"].ewm(span=9, adjust=False).mean()

    latest = df.iloc[-1]

    latest_rsi = latest["RSI"] if pd.notna(latest["RSI"]) else None
    latest_sma20 = latest["SMA20"] if pd.notna(latest["SMA20"]) else None
    latest_sma50 = latest["SMA50"] if pd.notna(latest["SMA50"]) else None
    latest_macd = latest["MACD"] if pd.notna(latest["MACD"]) else None
    latest_signal = latest["Signal"] if pd.notna(latest["Signal"]) else None

    if latest_rsi is None:
        rsi_signal = "N/A"
    elif latest_rsi > 70:
        rsi_signal = "Overbought"
    elif latest_rsi < 30:
        rsi_signal = "Oversold"
    else:
        rsi_signal = "Neutral"

    if latest_sma20 is None or latest_sma50 is None:
        trend_signal = "N/A"
    else:
        trend_signal = "Bullish" if latest_sma20 > latest_sma50 else "Bearish"

    if latest_macd is None or latest_signal is None:
        macd_signal = "N/A"
    else:
        macd_signal = "Bullish" if latest_macd > latest_signal else "Bearish"

    return df, {
        "RSI": round(latest_rsi, 2) if latest_rsi is not None else "N/A",
        "RSI Signal": rsi_signal,
        "Trend": trend_signal,
        "MACD Signal": macd_signal,
        "SMA20": round(latest_sma20, 2) if latest_sma20 is not None else "N/A",
        "SMA50": round(latest_sma50, 2) if latest_sma50 is not None else "N/A"
    }