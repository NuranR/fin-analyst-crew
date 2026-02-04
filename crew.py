from crewai import Crew, Process
from agents import get_all_agents
from tasks import create_all_tasks


def get_company_name(ticker: str) -> str:
    """
    Helper function to get company name from ticker using yfinance.    
    Falls back to ticker if lookup fails - not a big deal as agents will figure it out.
    """
    try:
        import yfinance as yf
        stock = yf.Ticker(ticker)
        info = stock.info
        return info.get("longName", info.get("shortName", ticker.upper()))
    except Exception:
        return ticker.upper()


def run_analysis(ticker: str) -> str:
    """
    The main function that runs the entire A-FIN analysis.
    
    Args:
        ticker: Stock ticker symbol (e.g., "AAPL", "GOOGL")
    
    Returns:
        The final investment recommendation as a string
    """
    # Step 1: Get the company name for more human-readable outputs
    company_name = get_company_name(ticker)
    print(f"\n{'='*60}")
    print(f"🚀 Starting A-FIN Analysis for {company_name} ({ticker.upper()})")
    print(f"{'='*60}\n")
    
    # Step 2: Create our team of specialized agents
    print("📋 Assembling the analyst team...")
    agents = get_all_agents()
    
    # Step 3: Create tasks for each agent
    print("📝 Assigning tasks to agents...")
    tasks = create_all_tasks(agents, ticker.upper(), company_name)
    
    # Step 4: Create the crew and set up the workflow
    print("🤝 Creating the A-FIN crew...\n")
    
    crew = Crew(
        agents=[
            agents["data_journalist"],
            agents["quantitative_analyst"],
            agents["regulatory_specialist"],
            agents["lead_analyst"]
        ],
        tasks=tasks,
        process=Process.sequential,  # Tasks execute in order
        verbose=True
    )
    
    # Step 5: Let the crew do their thing
    print("🔍 Starting analysis... This may take a minute or two.\n")
    result = crew.kickoff()
    
    print(f"\n{'='*60}")
    print("✅ Analysis Complete!")
    print(f"{'='*60}\n")
    
    return str(result)


if __name__ == "__main__":

    ticker = input("Enter a stock ticker (e.g., AAPL): ").strip().upper()
    if ticker:
        result = run_analysis(ticker)
        print("\n" + "="*60)
        print("FINAL RECOMMENDATION:")
        print("="*60)
        print(result)
