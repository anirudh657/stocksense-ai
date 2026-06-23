# StockSense AI — Portfolio Terminal

StockSense AI is a lightweight, low-latency financial portfolio tracking terminal built for active retail investors. Designed around a clean, minimalist, dark-themed UI, the terminal provides unified tracking of equity holdings alongside live market indices, real-time technical signals, core fundamental data, historical asset correlation tracking, and dynamic media reporting.

---

## 🚀 Key Features

* **Real-Time Index Analytics:** Live tracking of core Indian benchmarks (NIFTY 50 & SENSEX) with real-time percentage shift indications updated directly on the header status layer.
* **Modular Portfolio Framework:** Dynamic calculations of investment valuations, capital distributions, day P&L adjustments, and comprehensive net returns.
* **Smart Diversification Engine:** Algorithmic determination of current asset concentration safety margins to prevent heavy exposure risk.
* **Advanced Analytics & Statistics:**
  * **Portfolio Correlation Heatmap:** Dropdown analytics panel computing asset behavior patterns across a rolling 3-month historical timeline.
  * **Interactive Technical Engine:** Automatic calculation of running 20-day and 50-day Simple Moving Averages (SMA), Relative Strength Indicator (RSI), and MACD signal directions.
* **Live Financial Media Matrix:** Real-time collection and filtering of major publishing networks mapping localized press reports to your selected watchlists.
* **Data Portability:** Seamless local dataset exporting via instant CSV compilation hooks.

---

## 🏗️ Architecture Design

The system implements a decoupled, functional layout pattern engineered to separate UI layout rendering from complex technical processing pipelines and active memory stores:

```text
STOCKSENSE-AI/
├── app.py                # Main runtime orchestrator & layout configuration engine
├── market_data.py        # Core data ingestion pipeline, caching layers & math processors
├── portfolio.py          # Value accumulation, data storage, & diversification scoring
├── technicals.py         # Algorithmic calculation engines (RSI, SMA, MACD wrappers)
├── styles.py             # Global UI look-and-feel injection layer (CSS styles)
├── components.py         # Reusable presentation nodes (top bar indicators, currency formatters)
└── .gitignore            # Strict version control masking configuration
📈 Functional Block Model
Presentation Orchestrator (app.py): Acts as the centralized presentation environment managing dynamic context transitions based on user selections.

Telemetry Logic (market_data.py): Manages historical caching sequences (ttl=3600) to guarantee high calculation throughput across overlapping API execution loops.

Analytical Matrix (technicals.py): Processes underlying Pandas data slices into sequential technical signals.

🛠️ Technology Stack
Front-End Engine: Streamlit Architecture (Declarative UI Structure)

Visual Graph Rendering: Plotly Engine (Interactive Candlestick & Heatmap Matrices)

Data Pipelines & Math Arrays: Pandas Core Libraries & NumPy Vectors

Financial Data Access: yfinance Framework API

📦 Local Installation & Setup
Ensure you have Python 3.9+ installed on your local environment before proceeding.

1. Clone the Workspace
Bash
git clone [https://github.com/anirudh657/stocksense-ai.git](https://github.com/anirudh657/stocksense-ai.git)
cd stocksense-ai
2. Configure Your Virtual Isolation Space
On Windows:

Bash
python -m venv stocksense_env
stocksense_env\Scripts\activate
On macOS / Linux:

Bash
python3 -m venv stocksense_env
source stocksense_env/bin/activate
3. Install Required Framework Dependencies
Bash
pip install streamlit pandas yfinance plotly vectorbt
(Note: Adjust framework installations depending on your customized technical indicators)

4. Initialize the Application
Bash
streamlit run app.py
💾 Version Control Tracking Instructions
To log your localized system changes cleanly up to the active cloud repository, execute the following commands sequence within your isolated execution environment:

Bash
# Stage changes for index tracking
git add .

# Log architectural alterations safely
git commit -m "Feat: Add Market News, Correlation Matrix, and upgrade StockSense AI branding"

# Push branch snapshot updates to origin
git push origin main
📝 License
Distributed under the MIT License. See LICENSE for more information.


### Next Steps
1. Create a new file in your project directory named `README.md`.
2. Paste this text inside.
3. Use your terminal commands to sync it to GitHub:
   ```bash
   git add README.md
   git commit -m "Docs: Create professional repository documentation"
   git push origin main
