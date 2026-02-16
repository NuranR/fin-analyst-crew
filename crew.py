import time
from concurrent.futures import ThreadPoolExecutor, as_completed
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


def execute_task_with_crew(agent, task):
    """
    Helper to execute a single task with its agent.
    Used for concurrent execution of independent tasks.
    """
    crew = Crew(
        agents=[agent],
        tasks=[task],
        process=Process.sequential,
        verbose=True
    )
    return crew.kickoff()


def run_analysis_concurrent(ticker: str) -> dict:
    company_name = get_company_name(ticker)
    print(f"\n{'='*60}")
    print(f"🚀 Starting A-FIN Analysis for {company_name} ({ticker.upper()})")
    print(f"⚡ Mode: CONCURRENT EXECUTION")
    print(f"{'='*60}\n")
    
    total_start = time.time()
    
    # Create our team of specialized agents
    print("📋 Assembling the analyst team...")
    agents = get_all_agents()
    
    # Create tasks for each agent
    print("📝 Assigning tasks to agents...")
    tasks = create_all_tasks(agents, ticker.upper(), company_name)
    
    research_tasks = tasks[:3]  # News, Stock, SEC filings
    final_task = tasks[3]  # Lead analyst synthesis
    
    print("🔍 Starting parallel research phase...\n")
    parallel_start = time.time()
    
    research_results = []
    agent_names = ["data_journalist", "quantitative_analyst", "regulatory_specialist"]
    
    with ThreadPoolExecutor(max_workers=3) as executor:
        # Submit all 3 research tasks at once
        future_to_task = {
            executor.submit(
                execute_task_with_crew,
                agents[agent_names[i]],
                research_tasks[i]
            ): (agent_names[i], research_tasks[i])
            for i in range(3)
        }
        
        # Collect results as they complete
        for future in as_completed(future_to_task):
            agent_name, task = future_to_task[future]
            try:
                result = future.result()
                research_results.append(result)
                print(f"✅ {agent_name.replace('_', ' ').title()} completed\n")
            except Exception as e:
                print(f"❌ {agent_name} encountered an error: {str(e)}\n")
    
    parallel_time = time.time() - parallel_start
    
    # Execute the final synthesis task sequentially
    print("🎯 Starting final synthesis phase...\n")
    synthesis_start = time.time()
    
    final_crew = Crew(
        agents=[agents["lead_analyst"]],
        tasks=[final_task],
        process=Process.sequential,
        verbose=True
    )
    
    final_result = final_crew.kickoff()
    synthesis_time = time.time() - synthesis_start
    
    total_time = time.time() - total_start
    
    print(f"\n{'='*60}")
    print("✅ Analysis Complete!")
    print(f"⏱️  Parallel Research: {parallel_time:.2f}s")
    print(f"⏱️  Final Synthesis: {synthesis_time:.2f}s")
    print(f"⏱️  Total Time: {total_time:.2f}s")
    print(f"{'='*60}\n")
    
    return {
        "result": str(final_result),
        "timing": {
            "parallel_research": parallel_time,
            "final_synthesis": synthesis_time,
            "total": total_time
        }
    }


def run_analysis(ticker: str) -> str:
    """
    The original sequential execution function - kept for comparison.
    All agents run one after another in order.
    
    Args:
        ticker: Stock ticker symbol (e.g., "AAPL", "GOOGL")
    
    Returns:
        The final investment recommendation as a string
    """
    company_name = get_company_name(ticker)
    print(f"\n{'='*60}")
    print(f"🚀 Starting A-FIN Analysis for {company_name} ({ticker.upper()})")
    print(f"📝 Mode: SEQUENTIAL EXECUTION")
    print(f"{'='*60}\n")
    
    start_time = time.time()
    
    # Create our team of specialized agents
    print("📋 Assembling the analyst team...")
    agents = get_all_agents()
    
    # Create tasks for each agent
    print("📝 Assigning tasks to agents...")
    tasks = create_all_tasks(agents, ticker.upper(), company_name)
    
    # Create the crew and set up the workflow
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
    
    # Let the crew do their thing
    print("🔍 Starting analysis... This may take a minute or two.\n")
    result = crew.kickoff()
    
    total_time = time.time() - start_time
    
    print(f"\n{'='*60}")
    print("✅ Analysis Complete!")
    print(f"⏱️  Total Time: {total_time:.2f}s")
    print(f"{'='*60}\n")
    
    return str(result)


if __name__ == "__main__":
    print("A-FIN - Autonomous Financial Information Nexus")
    print("=" * 60)
    ticker = input("Enter a stock ticker (e.g., AAPL): ").strip().upper()
    
    if ticker:
        # Default to concurrent for better performance
        result_data = run_analysis_concurrent(ticker)
        print("\n" + "="*60)
        print("FINAL RECOMMENDATION:")
        print("="*60)
        print(result_data["result"])
