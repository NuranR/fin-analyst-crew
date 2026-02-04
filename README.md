# A-FIN (Autonomous Financial Information Nexus)

**A multi-agent AI system that analyzes stocks by combining news sentiment, financial metrics, and regulatory filings to generate comprehensive investment reports.**

A-FIN uses CrewAI and Gemini to build your personal investment team. Four AI specialists work together to analyze the news, numbers, and regulatory red flags, giving you a simple BUY, HOLD, or SELL verdict.

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER INPUT                               │
│                    (Company Ticker: ex: AAPL)                   │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    AGENT 1: Data Journalist                     │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  Tool: fetch_news()                                       │  │
│  │  • Fetches recent news articles                           │  │
│  │  • Analyzes sentiment (positive/negative/neutral)         │  │
│  │  • Identifies major events & market impact                │  │
│  │  • Flags concerning trends                                │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                 │
│  OUTPUT: News Sentiment Report                                  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                AGENT 2: Quantitative Analyst                    │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  Tool: fetch_stock_data()                                 │  │
│  │  • Pulls price data & technical indicators                │  │
│  │  • Calculates P/E ratios & valuation metrics              │  │
│  │  • Analyzes moving averages & trends                      │  │
│  │  • Reviews news context from Agent 1                      │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                 │
│  OUTPUT: Technical & Valuation Analysis                         │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│              AGENT 3: Regulatory Specialist                     │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  Tool: fetch_sec_filings()                                │  │
│  │  • Retrieves SEC filings (10-K, 10-Q, 8-K)                │  │
│  │  • Identifies regulatory risks & compliance issues        │  │
│  │  • Reviews financial disclosures                          │  │
│  │  • Considers previous agents' findings                    │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                 │
│  OUTPUT: Regulatory & Compliance Report                         │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    AGENT 4: Lead Analyst                        │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  Tool: None (synthesizes all previous reports)            │  │
│  │  • Combines insights from all three specialist agents     │  │
│  │  • Weighs sentiment, financials, and regulatory factors   │  │
│  │  • Generates final BUY/HOLD/SELL recommendation           │  │
│  │  • Provides confidence level and risk assessment          │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                 │
│  OUTPUT: Final Investment Report                                │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    FINAL INVESTMENT REPORT                      │
│  • Combined insights from all four agents                       │
│  • BUY/HOLD/SELL recommendation                                 │
│  • Risk assessment & key considerations                         │
│  • Confidence level & reasoning                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Getting Started

### 1. Create a Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Activate on macOS/Linux
source venv/bin/activate
```

### 2. Install Dependencies

```bash
# Install all required packages
pip install -r requirements.txt
```

### 3. Configure API Keys

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key_here
NEWS_API_KEY=your_newsapi_key_here
```

**Get your API keys:**

- **Gemini API**: https://ai.google.dev/
- **NewsAPI**: https://newsapi.org/

### 4. Run the Analysis

```bash
streamlit run app.py
```

Enter a stock ticker (e.g., `AAPL`) and watch the agents work sequentially!

## Agent Specializations

| Agent                     | Primary Focus              | Tool                  | Key Output                |
| ------------------------- | -------------------------- | --------------------- | ------------------------- |
| **Data Journalist**       | Market sentiment & news    | `fetch_news()`        | Sentiment analysis        |
| **Quantitative Analyst**  | Financial metrics          | `fetch_stock_data()`  | Valuation analysis        |
| **Regulatory Specialist** | Compliance & filings       | `fetch_sec_filings()` | Risk assessment           |
| **Lead Analyst**          | Final synthesis & decision | None                  | Investment recommendation |

## Technology Stack

- **Framework**: CrewAI (orchestrates agent collaboration)
- **LLM**: Google Gemini 2.5 Flash Lite (powers agent reasoning)
- **Data Sources**: NewsAPI, Yahoo Finance (yfinance), SEC EDGAR
- **Architecture**: Sequential crew with context sharing

---
