import streamlit as st

def apply_styles():
    st.markdown(
        """
        <style>
        .stApp { background: #171717; color: #e5e7eb; }
        header[data-testid="stHeader"] { background: #171717; height: 0rem; }
        .main .block-container { max-width: 100%; padding-top: 0.01rem !important; padding-bottom: 0.45rem; padding-left: 0.5rem; padding-right: 0.5rem; }
        section.stMain .block-container { padding-top: 0.01rem !important; }
        div[data-testid="stToolbar"] { top: 0.1rem; right: 0.35rem; }
        [data-testid="collapsedControl"] { display: none; }
        .topbar { background: #1b1b1b; border: 1px solid #252525; margin-top: 0rem; margin-bottom: 0.3rem; }
        .topbar-inner { display: flex; align-items: center; justify-content: space-between; gap: 12px; padding: 7px 14px; }
        .top-left, .top-center, .top-right { display: flex; align-items: center; gap: 18px; flex-wrap: wrap; }
        .index-chip { font-size: 12px; color: #d1d5db; padding: 4px 8px; border-radius: 6px; background: #202020; border: 1px solid #2c2c2c; }
        .index-name-up { color: #22c55e; font-weight: 700; }
        .index-name-down { color: #ef4444; font-weight: 700; }
        .index-val { color: #f3f4f6; font-weight: 600; }
        .index-change-up { color: #22c55e; font-weight: 600; }
        .index-change-down { color: #ef4444; font-weight: 600; }
        .brand-box { color: #f97316; font-weight: 700; font-size: 16px; }
        .nav-item { color: #b3b3b3; font-size: 13px; }
        .nav-active { color: #f97316; border-bottom: 2px solid #f97316; padding-bottom: 7px; }
        .panel { background: #171717; border: 1px solid #252525; height: 100%; }
        .section-pad { padding: 8px 10px 0 10px; }
        .notice-box { background: #222222; border: 1px solid #2f2f2f; color: #d1d5db; padding: 10px 14px; font-size: 13px; margin-bottom: 7px; }
        .tab-row { display: flex; gap: 20px; padding: 0 6px 8px 6px; border-bottom: 1px solid #252525; margin-bottom: 7px; }
        .tab { color: #a3a3a3; font-size: 13px; }
        .tab-active { color: #f97316; border-bottom: 2px solid #f97316; padding-bottom: 8px; }
        .holdings-top { display: flex; align-items: center; justify-content: space-between; padding: 5px 2px 8px 2px; border-bottom: 1px solid #252525; margin-bottom: 8px; }
        .holdings-title { font-size: 17px; color: #e5e7eb; font-weight: 500; }
        .mini-actions { color: #60a5fa; font-size: 12px; display: flex; gap: 12px; align-items: center; }
        .summary-grid { display: grid; grid-template-columns: repeat(5, minmax(120px, 1fr)); gap: 10px; padding: 7px 2px 12px 2px; border-bottom: 1px solid #252525; margin-bottom: 6px; }
        .summary-label { color: #8b8b8b; font-size: 11px; margin-bottom: 3px; }
        .summary-value { color: #e5e7eb; font-size: 16px; font-weight: 600; }
        .summary-sub { color: #bfbfbf; font-size: 11px; margin-left: 5px; }
        .pos { color: #58b26b; }
        .neg { color: #e26d5a; }
        .bar-wrap { width: 100%; height: 34px; background: #202020; margin-top: 8px; display: flex; overflow: hidden; border: 1px solid #252525; }
        .bar-left { height: 100%; background: #4f6fe8; }
        .bar-right { height: 100%; background: #1da1e2; }
        .watch-card { padding: 8px 0; border-bottom: 1px solid #252525; }
        .watch-row { display: flex; justify-content: space-between; align-items: center; gap: 8px; }
        .watch-symbol { color: #e5e7eb; font-size: 13px; font-weight: 500; }
        .watch-ex { color: #7b7b7b; font-size: 10px; margin-left: 5px; }
        .watch-meta { color: #a3a3a3; font-size: 12px; }
        .watch-price { color: #d4d4d4; font-size: 13px; }
        .footer-pages { display: flex; gap: 18px; color: #8d8d8d; font-size: 13px; padding: 8px 0 10px 0; border-top: 1px solid #252525; margin-top: 6px; }
        .stock-head { padding-top: 10px; padding-bottom: 4px; color: #d4d4d4; font-size: 16px; }
        .stTextInput > div > div > input { background: #1a1a1a; color: #e5e7eb; border: 1px solid #2a2a2a; border-radius: 0; padding: 9px 12px; font-size: 13px; }
        .stTextInput > label { color: #888 !important; font-size: 11px !important; }
        .stRadio { margin-bottom: 0.35rem; }
        .stRadio > div { gap: 0.05rem; }
        .stRadio label { width: 100%; font-size: 12px; }
        div[data-testid="stDataFrame"] { border: 1px solid #252525 !important; }
        [data-testid="stMetric"] { background: transparent; border: none; padding: 0; }
        [data-testid="stMetricLabel"] { color: #8b8b8b; font-size: 11px; }
        [data-testid="stMetricValue"] { color: #e5e7eb; font-size: 16px; }
        .fund-box { background: #1b1b1b; border: 1px solid #262626; padding: 12px; margin-bottom: 10px; }
        .fund-label { color: #8e8e8e; font-size: 11px; margin-bottom: 4px; }
        .fund-value { color: #e5e7eb; font-size: 14px; font-weight: 600; }
        
        /* NEW: Custom branding logo styling */
        .brand-logo {
            background: linear-gradient(to right, #f97316, #fcd34d);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 20px;
            font-weight: 900;
            letter-spacing: 1px;
            text-transform: uppercase;
        }
        </style>
        """,
        unsafe_allow_html=True
    )