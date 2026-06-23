import streamlit as st

def format_money(x):
    return f"₹{x:,.2f}"

def format_large_number(x):
    if x in [None, "N/A"]:
        return "N/A"
    try:
        x = float(x)
        if x >= 1e12:
            return f"₹{x / 1e12:.2f}T"
        if x >= 1e9:
            return f"₹{x / 1e9:.2f}B"
        if x >= 1e7:
            return f"₹{x / 1e7:.2f}Cr"
        if x >= 1e5:
            return f"₹{x / 1e5:.2f}L"
        return f"₹{x:,.2f}"
    except Exception:
        return str(x)

def render_top_bar(nifty_data, sensex_data):
    # Determine colors based on positive/negative change
    nifty_name_class = "index-name-up" if nifty_data["change"] >= 0 else "index-name-down"
    nifty_change_class = "index-change-up" if nifty_data["change"] >= 0 else "index-change-down"

    sensex_name_class = "index-name-up" if sensex_data["change"] >= 0 else "index-name-down"
    sensex_change_class = "index-change-up" if sensex_data["change"] >= 0 else "index-change-down"

    st.markdown(
        f"""
        <div class="topbar">
            <div class="topbar-inner">
                <div class="top-left">
                    <div class="index-chip">
                        <span class="{nifty_name_class}"><b>{nifty_data['label']}</b></span>
                        <span class="index-val">{nifty_data['price']:,.2f}</span>
                        <span class="{nifty_change_class}">{nifty_data['change']:+.2f} ({nifty_data['change_percent']:+.2f}%)</span>
                    </div>
                    <div class="index-chip">
                        <span class="{sensex_name_class}"><b>{sensex_data['label']}</b></span>
                        <span class="index-val">{sensex_data['price']:,.2f}</span>
                        <span class="{sensex_change_class}">{sensex_data['change']:+.2f} ({sensex_data['change_percent']:+.2f}%)</span>
                    </div>
                </div>
                <div class="top-center">
                    <div class="brand-box">◀</div>
                    <div class="nav-item">Dashboard</div>
                    <div class="nav-item">Orders</div>
                    <div class="nav-item nav-active">Holdings</div>
                    <div class="nav-item">Positions</div>
                    <div class="nav-item">Funds</div>
                </div>
                <div class="top-right">
                    <div class="brand-logo">STOCKSENSE AI</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )