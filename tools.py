"""
tools.py 

- Data Journalist gets a news fetching tool
- Quantitative Analyst gets a stock data tool  
- Regulatory Specialist gets an SEC filings tool

"""

import requests
import yfinance as yf
from crewai.tools import tool
from config import NEWS_API_KEY


@tool("Fetch Company News") # CrewAI's decorator to make the functions available to agents
def fetch_news(company_name: str) -> str:
    """
    Fetches recent news articles about a company using NewsAPI.
    
    Args:
        company_name: The name of the company to search for (e.g., "Apple" or "AAPL")
    
    Returns:
        A formatted string with recent news headlines and descriptions
    """
    # NewsAPI endpoint - search for everything
    url = "https://newsapi.org/v2/everything"
    
    params = {
        "q": company_name,
        "apiKey": NEWS_API_KEY,
        "language": "en",
        "sortBy": "publishedAt",  # Most recent first
        "pageSize": 5  # Grab 5 articles - enough for analysis without overwhelming
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # If no articles found, let the agent know
        if data.get("totalResults", 0) == 0:
            return f"No recent news found for {company_name}"
        
        # Format the news nicely for our agent to analyze
        articles = data.get("articles", [])
        news_summary = f"Recent News for {company_name}:\n\n"
        
        for i, article in enumerate(articles, 1):
            title = article.get("title", "No title")
            description = article.get("description", "No description")
            published = article.get("publishedAt", "Unknown date")[:10]  # Just the date part
            source = article.get("source", {}).get("name", "Unknown source")
            
            news_summary += f"{i}. [{published}] {title}\n"
            news_summary += f"   Source: {source}\n"
            news_summary += f"   Summary: {description}\n\n"
        
        return news_summary
        
    except requests.RequestException as e:
        return f"Error fetching news: {str(e)}"


@tool("Fetch Stock Data")
def fetch_stock_data(ticker: str) -> str:
    """
    Fetches stock market data for a given ticker using yfinance.
    
    Args:
        ticker: The stock ticker symbol (e.g., "AAPL", "GOOGL", "MSFT")
    
    Returns:
        A formatted string with key stock metrics and technical indicators
    """
    try:
        # Create a ticker object
        stock = yf.Ticker(ticker)
        
        # Get the stock info
        info = stock.info
        
        # Sometimes yfinance returns empty data for invalid tickers
        if not info or "regularMarketPrice" not in info:
            return f"Could not find stock data for ticker: {ticker}"
        
        # Extract the data Quantitative Analyst needs
        current_price = info.get("regularMarketPrice", "N/A")
        previous_close = info.get("previousClose", "N/A")
        market_cap = info.get("marketCap", "N/A")
        pe_ratio = info.get("trailingPE", "N/A")
        forward_pe = info.get("forwardPE", "N/A")
        dividend_yield = info.get("dividendYield", "N/A")
        fifty_two_week_high = info.get("fiftyTwoWeekHigh", "N/A")
        fifty_two_week_low = info.get("fiftyTwoWeekLow", "N/A")
        fifty_day_avg = info.get("fiftyDayAverage", "N/A")
        two_hundred_day_avg = info.get("twoHundredDayAverage", "N/A")
        volume = info.get("regularMarketVolume", "N/A")
        avg_volume = info.get("averageVolume", "N/A")
        
        # Format market cap (billions/millions)
        if isinstance(market_cap, (int, float)):
            if market_cap >= 1e12:
                market_cap_str = f"${market_cap/1e12:.2f}T"
            elif market_cap >= 1e9:
                market_cap_str = f"${market_cap/1e9:.2f}B"
            else:
                market_cap_str = f"${market_cap/1e6:.2f}M"
        else:
            market_cap_str = "N/A"
        
        # Format dividend yield as percentage
        if isinstance(dividend_yield, (int, float)):
            dividend_yield_str = f"{dividend_yield*100:.2f}%"
        else:
            dividend_yield_str = "N/A"
        
        # Build the comprehensive stock report
        stock_report = f"""
Stock Data for {ticker.upper()}:
================================

PRICE INFORMATION:
- Current Price: ${current_price}
- Previous Close: ${previous_close}
- 52-Week High: ${fifty_two_week_high}
- 52-Week Low: ${fifty_two_week_low}

VALUATION METRICS:
- Market Cap: {market_cap_str}
- P/E Ratio (Trailing): {pe_ratio}
- P/E Ratio (Forward): {forward_pe}
- Dividend Yield: {dividend_yield_str}

TECHNICAL INDICATORS:
- 50-Day Moving Average: ${fifty_day_avg}
- 200-Day Moving Average: ${two_hundred_day_avg}
- Current Volume: {volume:,} shares
- Average Volume: {avg_volume:,} shares

QUICK ANALYSIS:
- Trading {"ABOVE" if isinstance(current_price, (int, float)) and isinstance(fifty_day_avg, (int, float)) and current_price > fifty_day_avg else "BELOW"} 50-day average
- Trading {"ABOVE" if isinstance(current_price, (int, float)) and isinstance(two_hundred_day_avg, (int, float)) and current_price > two_hundred_day_avg else "BELOW"} 200-day average
"""
        return stock_report
        
    except Exception as e:
        return f"Error fetching stock data for {ticker}: {str(e)}"


@tool("Fetch SEC Filings")
def fetch_sec_filings(ticker: str) -> str:
    """
    Fetches recent SEC filings for a company using the SEC EDGAR API.
    
    Args:
        ticker: The stock ticker symbol (e.g., "AAPL", "GOOGL", "MSFT")
    
    Returns:
        A formatted string with recent SEC filings (10-K, 10-Q, 8-K)
    """
    try:
        # The SEC uses CIK(Central Index Key), not ticker symbols, so we need to do a lookup        
        # SEC requires a proper User-Agent header
        headers = {
            "User-Agent": "A-FIN Investment Research Bot (educational purposes)"
        }
        
        # Get the CIK lookup table from SEC
        cik_lookup_url = "https://www.sec.gov/files/company_tickers.json"
        response = requests.get(cik_lookup_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        companies = response.json()
        
        # Find our company's CIK
        cik = None
        company_name = None
        ticker_upper = ticker.upper()
        
        for entry in companies.values():
            if entry.get("ticker") == ticker_upper:
                cik = str(entry.get("cik_str")).zfill(10)  # CIK must be 10 digits
                company_name = entry.get("title")
                break
        
        if not cik:
            return f"Could not find SEC filings for ticker: {ticker}"
        
        # Now fetch the company's recent filings
        filings_url = f"https://data.sec.gov/submissions/CIK{cik}.json"
        response = requests.get(filings_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        filings_data = response.json()
        recent_filings = filings_data.get("filings", {}).get("recent", {})
        
        # Extract the filing details
        forms = recent_filings.get("form", [])
        dates = recent_filings.get("filingDate", [])
        descriptions = recent_filings.get("primaryDocument", [])
        accession_numbers = recent_filings.get("accessionNumber", [])
        
        # major filings: 10-K (annual), 10-Q (quarterly), 8-K (current events)
        important_forms = ["10-K", "10-Q", "8-K"]
        
        filings_report = f"""
SEC Filings for {company_name} ({ticker.upper()}):
{'=' * 50}

"""
        filing_count = 0
        max_filings = 10  # Limit to avoid overwhelming the agent
        
        for i, form in enumerate(forms):
            if form in important_forms and filing_count < max_filings:
                filing_date = dates[i] if i < len(dates) else "Unknown"
                accession = accession_numbers[i] if i < len(accession_numbers) else "Unknown"
                
                # Add a brief explanation of what each form type means
                form_explanation = {
                    "10-K": "Annual Report - comprehensive yearly financial overview",
                    "10-Q": "Quarterly Report - financial update every 3 months", 
                    "8-K": "Current Report - significant events or changes"
                }
                
                filings_report += f"""
{form} Filing - {filing_date}
  Type: {form_explanation.get(form, 'SEC Filing')}
  Accession Number: {accession}
  Link: https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={cik}&type={form}
"""
                filing_count += 1
        
        if filing_count == 0:
            filings_report += "No recent 10-K, 10-Q, or 8-K filings found.\n"
        
        filings_report += f"""
SUMMARY:
- Total major filings shown: {filing_count}
- For detailed analysis, review the 10-K (annual) and most recent 10-Q (quarterly) reports
"""
        
        return filings_report
        
    except requests.RequestException as e:
        return f"Error fetching SEC filings: {str(e)}"
    except Exception as e:
        return f"Unexpected error fetching SEC filings for {ticker}: {str(e)}"
