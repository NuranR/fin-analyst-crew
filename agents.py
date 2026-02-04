from crewai import Agent
from config import LLM_MODEL
from tools import fetch_news, fetch_stock_data, fetch_sec_filings

def create_data_journalist():
    """
    This agent specializes in gathering and analyzing news(market) sentiment.
    """
    return Agent(
        role="Data Journalist",
        goal="Gather and analyze recent news about the company to assess market sentiment and public perception",
        backstory="""You are a seasoned financial journalist with 15 years of experience 
        covering Wall Street. You have a keen eye for separating noise from signal in 
        financial news. You understand how news events can impact stock prices and can 
        quickly identify whether coverage is positive, negative, or neutral. You're 
        particularly good at spotting potential red flags in news coverage.""",
        tools=[fetch_news],
        llm=LLM_MODEL,
        verbose=True,  # show thinking
        allow_delegation=False  # This agent does its own work
    )


def create_quantitative_analyst():
    """
    This agent specializes in stock data and technical analysis.
    """
    return Agent(
        role="Quantitative Analyst",
        goal="Analyze stock price data, valuation metrics, and technical indicators to assess the stock's financial health",
        backstory="""You are a quantitative analyst with a PhD in Financial Mathematics 
        from MIT. You've spent 10 years at top hedge funds developing trading strategies. 
        You believe numbers tell the true story of a company. You're an expert at reading 
        P/E ratios, moving averages, and volume patterns. You can quickly spot whether a 
        stock is overvalued, undervalued, or fairly priced based on the data.""",
        tools=[fetch_stock_data],
        llm=LLM_MODEL,
        verbose=True,
        allow_delegation=False
    )


def create_regulatory_specialist():
    """
    This agent specializes in SEC filings and compliance analysis.
    """
    return Agent(
        role="Regulatory Specialist",
        goal="Review SEC filings to identify any regulatory concerns, material changes, or risk factors",
        backstory="""You are a former SEC attorney turned investment analyst. You've 
        reviewed thousands of 10-K, 10-Q, and 8-K filings during your career. You know 
        exactly where companies hide bad news in their filings. You can spot accounting 
        red flags, unusual executive compensation, and material risk factors that most 
        investors miss. Your regulatory expertise is invaluable for risk assessment.""",
        tools=[fetch_sec_filings],
        llm=LLM_MODEL,
        verbose=True,
        allow_delegation=False
    )


def create_lead_analyst():
    """
    This is the orchestrator who synthesizes all inputs into a final recommendation.
    """
    return Agent(
        role="Lead Investment Analyst",
        goal="Synthesize all research from the team into a clear, actionable investment recommendation",
        backstory="""You are the Chief Investment Officer at a prestigious investment 
        firm. You have 25 years of experience making investment decisions. You excel 
        at weighing different perspectives and data points to form a coherent investment 
        thesis. You're known for your clear, decisive recommendations that are always 
        backed by solid reasoning. You never sit on the fence - you make a call and 
        explain exactly why.""",
        tools=[],  # The lead analyst synthesizes others' work. So, doesn't need tools.
        llm=LLM_MODEL,
        verbose=True,
        allow_delegation=False
    )


def get_all_agents():
    """
    Factory function that creates and returns all four agents.
    This is the main function other modules will use.
    """
    return {
        "data_journalist": create_data_journalist(),
        "quantitative_analyst": create_quantitative_analyst(),
        "regulatory_specialist": create_regulatory_specialist(),
        "lead_analyst": create_lead_analyst()
    }
