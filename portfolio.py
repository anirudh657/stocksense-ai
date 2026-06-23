import pandas as pd
from market_data import safe_get_current_price

def get_portfolio_data():
    portfolio = {
        "TCS.NS": {"qty": 10, "avg_price": 3500},
        "INFY.NS": {"qty": 12, "avg_price": 1500},
        "RELIANCE.NS": {"qty": 8, "avg_price": 2800},
        "HDFCBANK.NS": {"qty": 15, "avg_price": 1600},
        "ITC.NS": {"qty": 20, "avg_price": 430},
        "SBIN.NS": {"qty": 18, "avg_price": 780}
    }

    stocks_data = []

    for stock, details in portfolio.items():
        qty = details["qty"]
        avg_price = details["avg_price"]

        current_price = safe_get_current_price(stock)
        if current_price is None:
            current_price = avg_price

        invested = qty * avg_price
        current = qty * current_price
        profit = current - invested

        stocks_data.append({
            "Stock": stock.replace(".NS", ""),
            "Qty": qty,
            "AvgCost": round(avg_price, 2),
            "LTP": round(current_price, 2),
            "Invested": round(invested, 2),
            "Current": round(current, 2),
            "Profit": round(profit, 2),
        })

    return {"stocks": stocks_data}

def calculate_diversification_score(df):
    if df.empty or df["Current"].sum() == 0:
        return 0
    weights = df["Current"] / df["Current"].sum()
    hhi = (weights ** 2).sum()
    score = int((1 - hhi) * 100)
    return max(0, min(score, 100))