import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import streamlit as st

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

def get_stock_news(symbol, limit=4):
    """Fetches compact market news for a specific stock."""
    try:
        ticker = yf.Ticker(symbol)
        news = ticker.news
        if not news:
            return []
        
        formatted_news = []
        for n in news[:limit]:
            formatted_news.append({
                "title": n.get("title", "No Title"),
                "publisher": n.get("publisher", "Unknown"),
                "link": n.get("link", "#")
            })
        return formatted_news
    except Exception:
        return []

@st.cache_data(ttl=3600)
def get_correlation_matrix(tickers):
    """Generates a Plotly heatmap of stock correlations based on 3 months of data."""
    if not tickers or len(tickers) < 2:
        return None
    try:
        # Download 3 months of daily close price data
        df = yf.download(tickers, period="3mo", interval="1d", progress=False)["Close"]
        
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
            
        corr = df.corr().round(2)
        
        # Create an interactive heatmap
        fig = go.Figure(data=go.Heatmap(
            z=corr.values,
            x=corr.columns,
            y=corr.index,
            colorscale='RdBu',
            zmin=-1, zmax=1,
            text=corr.values,
            texttemplate="%{text}",
            showscale=False,
            hoverinfo="x+y+z"
        ))
        
        fig.update_layout(
            height=350,
            margin=dict(l=20, r=20, t=20, b=20),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#d1d5db", size=10)
        )
        return fig
    except Exception:
        return None