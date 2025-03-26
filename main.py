"""
Main entry point for the CO2 Storage Assessment system.
"""

from praisonaiagents import PraisonAIAgents
from config.config import LLM_MODEL
from agents import create_agents, create_tasks
from utils import setup_logging

def main():
    """
    Main function to initialize and run the CO2 Storage Assessment system.
    """
    # Set up logging
    logger = setup_logging()
    logger.info("Starting CO2 Storage Assessment system")
    
    # Create agents and tasks
    agents = create_agents()
    tasks = create_tasks(agents)
    
    logger.info(f"Created {len(agents)} agents and {len(tasks)} tasks")
    
    # Initialize the multi-agent system
    agents_system = PraisonAIAgents(
        agents=agents,
        tasks=tasks,
        manager_llm=LLM_MODEL,
        process='sequential',
        memory=True
    )
    
    logger.info("Starting analysis process")
    
    # Run the system and get the result
    result = agents_system.start()
    
    logger.info("Analysis complete")
    return result

if __name__ == "__main__":
    main()
