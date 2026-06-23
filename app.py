import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Import from our modularized files
from styles import apply_styles
from market_data import get_market_data, get_index_data, safe_get_history, get_stock_info, get_stock_news, get_correlation_matrix
from portfolio import get_portfolio_data, calculate_diversification_score
from technicals import compute_technicals
from components import format_money, format_large_number, render_top_bar

st.set_page_config(
    page_title="StockSense AI",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Apply CSS
apply_styles()

# ---------------- DATA INITIALIZATION ----------------
portfolio_data = get_portfolio_data()

watchlist = [
    "TCS.NS", "RELIANCE.NS", "INFY.NS", "HDFCBANK.NS", "ONGC.NS",
    "HINDUNILVR.NS", "ITC.NS", "SBIN.NS", "LT.NS", "ICICIBANK.NS",
    "AXISBANK.NS", "KOTAKBANK.NS", "BHARTIARTL.NS", "ASIANPAINT.NS",
    "MARUTI.NS", "WIPRO.NS", "TATAMOTORS.NS", "BAJFINANCE.NS"
]

nifty_data = get_index_data("^NSEI", "NIFTY 50")
sensex_data = get_index_data("^BSESN", "SENSEX")

if "selected_stock" not in st.session_state:
    st.session_state.selected_stock = watchlist[0]

holdings_df = pd.DataFrame(portfolio_data["stocks"]).copy()

if holdings_df.empty:
    st.error("Portfolio data not available.")
    st.stop()

holdings_df["NetChange"] = (
    (holdings_df["Profit"] / holdings_df["Invested"].replace(0, pd.NA)) * 100
).fillna(0).round(2)
holdings_df["DayChange"] = 0.00

total_investment = holdings_df["Invested"].sum()
current_value = holdings_df["Current"].sum()
total_pnl = holdings_df["Profit"].sum()
total_pnl_pct = (total_pnl / total_investment * 100) if total_investment else 0
day_pnl = 0.00
day_pnl_pct = 0.00
diversification_score = calculate_diversification_score(holdings_df)

# Render Custom Top Bar
render_top_bar(nifty_data, sensex_data)

# ---------------- LAYOUT ----------------
left, right = st.columns([1.02, 2.18], gap="small")

with left:
    st.markdown('<div class="panel"><div class="section-pad">', unsafe_allow_html=True)

    search_text = st.text_input("Search watchlist", value="", placeholder="Search symbol...")
    filtered_watchlist = [s for s in watchlist if search_text.lower() in s.lower()]

    if not filtered_watchlist:
        st.info("No matching stocks found.")
    else:
        if st.session_state.selected_stock not in filtered_watchlist:
            st.session_state.selected_stock = filtered_watchlist[0]

        selected_stock = st.radio(
            "Watchlist",
            filtered_watchlist,
            index=filtered_watchlist.index(st.session_state.selected_stock),
            label_visibility="collapsed"
        )
        st.session_state.selected_stock = selected_stock

        for s in filtered_watchlist:
            market = get_market_data(s)
            symbol = market["symbol"].replace(".NS", "")
            price = market["price"]
            chg_pct = market["change_percent"]
            color_class = "pos" if chg_pct >= 0 else "neg"

            st.markdown(
                f"""
                <div class="watch-card">
                    <div class="watch-row">
                        <div>
                            <span class="watch-symbol">{symbol}</span>
                            <span class="watch-ex">NSE</span>
                        </div>
                        <div class="watch-meta {color_class}">{chg_pct:+.2f}%</div>
                        <div class="watch-price">₹{price}</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown(
        """
        <div class="footer-pages">
            <div style="color:#f97316;">1</div>
            <div>2</div>
            <div>3</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("</div></div>", unsafe_allow_html=True)

with right:
    # --- HEADER & TABS ---
    st.markdown(
        """
        <div class="notice-box">
            StockSense AI portfolio terminal with holdings, candlestick chart, fundamentals, and technicals.
        </div>
        <div class="tab-row">
            <div class="tab">All</div>
            <div class="tab tab-active">Equity</div>
            <div class="tab">Mutual funds</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # --- ACTION BUTTONS & ANALYTICS TOGGLE ---
    h_title, h_search, h_analytics, h_download = st.columns([5, 1.5, 1.5, 1.5], gap="small")
    
    with h_title:
        st.markdown('<div class="holdings-title" style="padding-top: 6px;">Holdings</div>', unsafe_allow_html=True)
    with h_search:
        if st.button("🔍 Search", use_container_width=True):
            st.toast("Search feature coming soon!")
    with h_analytics:
        if st.button("📊 Analytics", use_container_width=True):
            st.session_state.show_analytics = not st.session_state.get("show_analytics", False)
    with h_download:
        csv_data = holdings_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="⬇️ Download",
            data=csv_data,
            file_name="stocksense_holdings.csv",
            mime="text/csv",
            use_container_width=True
        )

    # Show Correlation Matrix if Analytics is toggled ON
    if st.session_state.get("show_analytics", False):
        st.markdown('<div class="holdings-title" style="margin-top: 15px; font-size: 16px;">Portfolio Correlation Matrix (3M)</div>', unsafe_allow_html=True)
        portfolio_tickers = [stock["Stock"] + ".NS" for stock in portfolio_data["stocks"]]
        corr_fig = get_correlation_matrix(portfolio_tickers)
        if corr_fig:
            st.plotly_chart(corr_fig, use_container_width=True)
        else:
            st.info("Add more instruments to compute historical asset correlations.")

    # --- SUMMARY GRID ---
    pnl_class = "pos" if total_pnl >= 0 else "neg"

    st.markdown(
        f"""
        <div class="summary-grid">
            <div>
                <div class="summary-label">Total investment</div>
                <div class="summary-value">{format_money(total_investment)}</div>
            </div>
            <div>
                <div class="summary-label">Current value</div>
                <div class="summary-value">{format_money(current_value)}</div>
            </div>
            <div>
                <div class="summary-label">Day's P&amp;L</div>
                <div class="summary-value">{format_money(day_pnl)}<span class="summary-sub">{day_pnl_pct:.2f}%</span></div>
            </div>
            <div>
                <div class="summary-label">Total P&amp;L</div>
                <div class="summary-value {pnl_class}">{format_money(total_pnl)}<span class="summary-sub {pnl_class}">{total_pnl_pct:.2f}%</span></div>
            </div>
            <div>
                <div class="summary-label">Diversification</div>
                <div class="summary-value">{diversification_score}/100</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # --- TABLE DATA PREP ---
    display_df = holdings_df.copy().rename(
        columns={
            "Stock": "Instrument", "Qty": "Qty.", "AvgCost": "Avg. cost",
            "LTP": "LTP", "Invested": "Invested", "Current": "Cur. val",
            "Profit": "P&L", "NetChange": "Net chg.", "DayChange": "Day chg."
        }
    )

    for col in ["Avg. cost", "LTP", "Invested", "Cur. val", "P&L"]:
        display_df[col] = display_df[col].map(lambda x: f"{x:,.2f}")

    display_df["Net chg."] = display_df["Net chg."].map(lambda x: f"{x:+.2f}%")
    display_df["Day chg."] = display_df["Day chg."].map(lambda x: f"{x:+.2f}%")

    # --- TABLE COLOR STYLING ---
    def color_pnl(val):
        val_str = str(val)
        try:
            num = float(val_str.replace("₹", "").replace("%", "").replace(",", "").replace("+", ""))
            if num > 0:
                return "color: #22c55e; font-weight: 500;"
            elif num < 0:
                return "color: #ef4444; font-weight: 500;"
        except:
            pass
        return "color: #8b8b8b;"

    styled_df = display_df[
        ["Instrument", "Qty.", "Avg. cost", "LTP", "Invested", "Cur. val", "P&L", "Net chg.", "Day chg."]
    ].style.map(color_pnl, subset=["P&L", "Net chg.", "Day chg."])

    st.dataframe(
        styled_df,
        use_container_width=True,
        height=220
    )

    # --- PORTFOLIO BAR ---
    if len(holdings_df) >= 2 and current_value > 0:
        weights = (holdings_df["Current"] / current_value * 100).round(2).tolist()
        left_weight = weights[0]
        right_weight = max(0, 100 - left_weight)
    else:
        left_weight = 100; right_weight = 0

    st.markdown(
        f"""
        <div class="bar-wrap">
            <div class="bar-left" style="width:{left_weight}%;"></div>
            <div class="bar-right" style="width:{right_weight}%;"></div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # --- STOCK DETAILS & CHARTS ---
    selected_stock = st.session_state.selected_stock
    market = get_market_data(selected_stock)

    st.markdown(f'<div class="stock-head">{market["symbol"]} &nbsp;&nbsp; ₹{market["price"]}</div>', unsafe_allow_html=True)

    chart_data = safe_get_history(selected_stock, period="6mo", interval="1d")

    if chart_data.empty or not {"Open", "High", "Low", "Close", "Volume"}.issubset(chart_data.columns):
        st.warning("No chart data available for the selected stock.")
    else:
        tech_df, technical_summary = compute_technicals(chart_data)
        stock_info = get_stock_info(selected_stock)

        # Tabs updated to include "News"
        tab1, tab2, tab3, tab4 = st.tabs(["Fundamental", "Chart", "Technicals", "News"])

        with tab1:
            f1, f2, f3, f4 = st.columns(4)
            with f1:
                st.markdown(f'<div class="fund-box"><div class="fund-label">Sector</div><div class="fund-value">{stock_info["sector"]}</div></div>', unsafe_allow_html=True)
            with f2:
                st.markdown(f'<div class="fund-box"><div class="fund-label">Industry</div><div class="fund-value">{stock_info["industry"]}</div></div>', unsafe_allow_html=True)
            with f3:
                st.markdown(f'<div class="fund-box"><div class="fund-label">Market Cap</div><div class="fund-value">{format_large_number(stock_info["market_cap"])}</div></div>', unsafe_allow_html=True)
            with f4:
                st.markdown(f'<div class="fund-box"><div class="fund-label">P/E</div><div class="fund-value">{stock_info["pe"]}</div></div>', unsafe_allow_html=True)

            g1, g2, g3, g4 = st.columns(4)
            with g1: st.metric("P/B", stock_info["pb"])
            with g2: st.metric("Dividend Yield", stock_info["dividend_yield"])
            with g3: st.metric("52W High", stock_info["fifty_two_week_high"])
            with g4: st.metric("52W Low", stock_info["fifty_two_week_low"])

        with tab2:
            candle_fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.05, row_heights=[0.75, 0.25])
            candle_fig.add_trace(go.Candlestick(x=tech_df.index, open=tech_df["Open"], high=tech_df["High"], low=tech_df["Low"], close=tech_df["Close"], name="Candlestick"), row=1, col=1)
            candle_fig.add_trace(go.Bar(x=tech_df.index, y=tech_df["Volume"], name="Volume", marker_color="#3b82f6"), row=2, col=1)
            
            candle_fig.update_layout(height=480, margin=dict(l=10, r=10, t=20, b=10), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", xaxis_rangeslider_visible=False, font=dict(color="#d1d5db"))
            candle_fig.update_xaxes(showgrid=False)
            candle_fig.update_yaxes(showgrid=True, gridcolor="#2a2a2a")
            st.plotly_chart(candle_fig, use_container_width=True)

        with tab3:
            t1, t2, t3 = st.columns(3)
            with t1:
                st.metric("RSI (14)", technical_summary["RSI"])
                st.metric("RSI Signal", technical_summary["RSI Signal"])
            with t2:
                st.metric("Trend", technical_summary["Trend"])
                st.metric("MACD Signal", technical_summary["MACD Signal"])
            with t3:
                st.metric("SMA 20", technical_summary["SMA20"])
                st.metric("SMA 50", technical_summary["SMA50"])

            tech_line = go.Figure()
            tech_line.add_trace(go.Scatter(x=tech_df.index, y=tech_df["Close"], mode="lines", name="Close", line=dict(color="#60a5fa", width=2)))
            tech_line.add_trace(go.Scatter(x=tech_df.index, y=tech_df["SMA20"], mode="lines", name="SMA 20", line=dict(color="#f97316", width=1.5)))
            tech_line.add_trace(go.Scatter(x=tech_df.index, y=tech_df["SMA50"], mode="lines", name="SMA 50", line=dict(color="#22c55e", width=1.5)))

            tech_line.update_layout(height=320, margin=dict(l=10, r=10, t=20, b=10), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#d1d5db"))
            st.plotly_chart(tech_line, use_container_width=True)

        with tab4:
            st.markdown('<div class="fund-label" style="margin-bottom:12px; font-weight:600;">Ticker Live Coverage</div>', unsafe_allow_html=True)
            news_items = get_stock_news(selected_stock)
            
            if not news_items:
                st.info("No active media tracking found for this asset class.")
            else:
                for item in news_items:
                    st.markdown(
                        f"""
                        <div style="padding: 12px 0; border-bottom: 1px solid #222222;">
                            <a href="{item['link']}" target="_blank" style="color: #60a5fa; text-decoration: none; font-size: 13.5px; font-weight: 500; line-height:1.4;">
                                {item['title']}
                            </a>
                            <div style="color: #71717a; font-size: 11px; margin-top: 5px;">
                                Publisher: <span style="color: #a1a1aa;">{item['publisher']}</span>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )