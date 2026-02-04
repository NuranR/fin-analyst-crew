from crewai import Task


def create_news_analysis_task(agent, ticker: str, company_name: str):

    return Task(
        description=f"""
        Analyze recent news coverage for {company_name} (ticker: {ticker}).
        
        Your job is to:
        1. Use your news fetching tool to gather recent articles about {company_name}
        2. Analyze the overall sentiment (positive, negative, neutral)
        3. Identify any major news events that could impact the stock
        4. Note any concerning trends or red flags in media coverage
        5. Assess how the market might react to this news
        
        Focus on news from the past week for the most relevant insights.
        """,
        expected_output="""
        A concise news sentiment report including:
        - Overall sentiment assessment (Positive/Negative/Neutral with score 1-10)
        - Key news highlights (top 3-5 stories)
        - Potential market impact analysis
        - Any red flags or concerns noted
        """,
        agent=agent
    )


def create_stock_analysis_task(agent, ticker: str, company_name: str):
    
    return Task(
        description=f"""
        Perform a quantitative analysis of {company_name} (ticker: {ticker}).
        
        Your job is to:
        1. Use your stock data tool to fetch current market data for {ticker}
        2. Analyze the valuation metrics (P/E ratio, market cap, etc.)
        3. Review technical indicators (moving averages, volume trends)
        4. Compare current price to 52-week range
        5. Determine if the stock appears overvalued, undervalued, or fairly valued
        
        Provide data-driven insights, not opinions without numbers.
        """,
        expected_output="""
        A quantitative analysis report including:
        - Current price and valuation summary
        - Key metrics analysis (P/E, dividend yield, etc.)
        - Technical indicator signals (bullish/bearish)
        - Valuation assessment (Overvalued/Undervalued/Fair Value)
        - Risk level based on volatility and price position
        """,
        agent=agent
    )


def create_regulatory_analysis_task(agent, ticker: str, company_name: str):
    
    return Task(
        description=f"""
        Review SEC filings and regulatory status for {company_name} (ticker: {ticker}).
        
        Your job is to:
        1. Use your SEC filings tool to fetch recent regulatory filings
        2. Identify recent 10-K (annual) and 10-Q (quarterly) filings
        3. Note any 8-K filings (significant events)
        4. Look for any regulatory red flags or concerns
        5. Assess the company's compliance and disclosure quality
        
        Focus on identifying any material risks or changes disclosed in filings.
        """,
        expected_output="""
        A regulatory compliance report including:
        - Summary of recent SEC filings
        - Any material events from 8-K filings
        - Risk factors identified
        - Compliance assessment (Good/Moderate/Concerning)
        - Any red flags that investors should be aware of
        """,
        agent=agent
    )


def create_final_recommendation_task(agent, ticker: str, company_name: str, context_tasks: list):

    return Task(
        description=f"""
        As the Lead Investment Analyst, synthesize all research on {company_name} ({ticker}) 
        and provide a final investment recommendation.
        
        You will receive analysis from:
        1. Data Journalist - News sentiment and market perception
        2. Quantitative Analyst - Stock data and valuations
        3. Regulatory Specialist - SEC filings and compliance
        
        Your job is to:
        1. Weigh all the evidence from your team
        2. Identify the most important factors for the investment decision
        3. Consider both opportunities and risks
        4. Make a clear, decisive recommendation
        5. Explain your reasoning in simple terms
        
        Remember: You must make a call. No fence-sitting allowed!
        """,
        expected_output="""
        A final investment recommendation report with:
        
        1. RECOMMENDATION: Clear BUY, HOLD, or SELL rating
        
        2. CONFIDENCE LEVEL: High/Medium/Low with explanation
        
        3. KEY FACTORS:
           - Top 3 reasons supporting your recommendation
           - Top 2 risks to consider
        
        4. SUMMARY: A 2-3 sentence executive summary that a busy investor 
           can read and understand the key takeaway
        
        5. DISCLAIMER: Brief reminder that this is AI-generated analysis 
           and not financial advice
        """,
        agent=agent,
        context=context_tasks  # This task needs the other tasks' outputs
    )

# Creates all tasks for the crew and returns tasks in the order they should be executed.
def create_all_tasks(agents: dict, ticker: str, company_name: str):
    
    news_task = create_news_analysis_task(
        agents["data_journalist"], 
        ticker, 
        company_name
    )
    
    stock_task = create_stock_analysis_task(
        agents["quantitative_analyst"], 
        ticker, 
        company_name
    )
    
    regulatory_task = create_regulatory_analysis_task(
        agents["regulatory_specialist"], 
        ticker, 
        company_name
    )
    
    final_task = create_final_recommendation_task(
        agents["lead_analyst"],
        ticker,
        company_name,
        context_tasks=[news_task, stock_task, regulatory_task]
    )
    
    return [news_task, stock_task, regulatory_task, final_task]
