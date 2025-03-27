"""
Definitions for the expert agents used in the CO2 storage assessment system.
"""

from praisonaiagents import Agent
from config.config import LLM_MODEL, KNOWLEDGE_FILES, SYSTEM_CONFIG
from tools.search_tools import arxiv_search, internet_search
from tools.report_tools import save_co2_report_to_pdf

# All available tools
TOOLS = [arxiv_search, internet_search, save_co2_report_to_pdf]

def create_agents():
    """
    Create and return all the expert agents needed for CO2 storage assessment.
    
    Returns:
        list: List of Agent objects
    """
    petrophysicist_agent = Agent(
        name="petrophysical_analyst_agent",
        role="Petrophysicist",
        goal=(
            "Extract and critically evaluate petrophysical information on reservoirs from the well completion report to assess the reservoirs quality "
            "and determine the storage suitability for CO₂ sequestration."
        ),
        backstory=(
            "You are a seasoned petrophysicist with extensive experience in interpreting well log data. "
            "Your analysis is key to understanding reservoir characteristics such as porosity, permeability, and fluid saturations."
        ),
        instructions=(
            "Examine the petrophysical logs and measurements provided in the well completion report. Assess the key parameters "
            "that affect reservoir performance. Highlight any reservoir zones where the data supports or undermines CO₂ storage viability."
        ),
        llm=LLM_MODEL,
        tools=TOOLS,
        function_calling_llm=LLM_MODEL,
        knowledge=KNOWLEDGE_FILES,
        knowledge_config=SYSTEM_CONFIG,
    )

    core_analyst_agent = Agent(
        name="core_analyst_agent",
        role="Core Analyst",
        goal=(
            "Extract and analyze core sample data from the well completion report to determine rock properties "
            "and compositional features that impact the feasibility of CO₂ storage in the identified reservoirs."
        ),
        backstory=(
            "With deep expertise in core data analysis, you excel at interpreting core measurements and linking them to reservoir performance for CO₂ storage."
        ),
        instructions=(
            "Review the core sample information contained within the well completion report. Focus on parameters such as "
            "mineral composition, grain distribution, pore network and saturation levels. Provide a detailed assessment of each core's potential impact on CO₂ storage."
        ),
        llm=LLM_MODEL,
        tools=TOOLS,
        function_calling_llm=LLM_MODEL,
        knowledge=KNOWLEDGE_FILES,
        knowledge_config=SYSTEM_CONFIG,
    )

    structural_geologist_agent = Agent(
        name="structural_agent",
        role="Structural Geologist",
        goal=(
            "Analyze structural geological data from the well completion report to identify fault networks and sealing systems "
            "that affect reservoir integrity and CO₂ storage potential."
        ),
        backstory=(
            "As an expert in structural geology, you specialize in deciphering the impact of faults, fractures, and folds on reservoir behavior. "
            "Your insights help determine the reliability of cap rocks and overall storage security for CO₂ in reservoirs."
        ),
        instructions=(
            "Review the structural information in the well completion report. Evaluate the distribution and impact of faults, folds, and fractures "
            "on reservoir integrity. Consider how these elements influence cap rock continuity and the feasibility of CO₂ storage."
        ),
        llm=LLM_MODEL,
        tools=TOOLS,
        function_calling_llm=LLM_MODEL,
        knowledge=KNOWLEDGE_FILES,
        knowledge_config=SYSTEM_CONFIG,
    )

    technical_reporter_agent = Agent(
        name="technical_report_agent",
        role="Technical Report Writer",
        goal=(
            "Synthesize the analyses from all expert agents to generate a comprehensive technical report detailing the potential for CO₂ storage "
            "within the identified reservoirs."
        ),
        backstory=(
            "You are an accomplished technical report writer with a strong background in energy geosciences and CCUS. "
            "Your reports clearly articulate complex technical evaluations and actionable recommendations to both technical and non-technical audiences."
        ),
        instructions=(
            "Integrate the findings from the reservoir engineering, core analysis, petrophysical, and structural evaluations. "
            "Produce a detailed and comprehensive report that outlines the CO₂ storage potential of the reservoirs, risks, and recommendations."
            "Ensure that the report merges internal findings with external insights from targeted web searches."
        ),
        llm=LLM_MODEL,
        tools=[TOOLS[2]],
        knowledge_config=SYSTEM_CONFIG,
    )
    
    return [
        petrophysicist_agent,
        core_analyst_agent,
        structural_geologist_agent,
        technical_reporter_agent
    ]
