"""
Definitions for the tasks to be executed by the agents in the CO2 storage assessment system.
"""

from praisonaiagents import Task

def create_tasks(agents):
    """
    Create and return all the tasks needed for CO2 storage assessment.
    
    Args:
        agents (list): List of Agent objects
        
    Returns:
        list: List of Task objects
    """
    # Extract agents by role for clarity
    petrophysicist = next(a for a in agents if a.role == "Petrophysicist")
    core_analyst = next(a for a in agents if a.role == "Core Analyst")
    structural_geologist = next(a for a in agents if a.role == "Structural Geologist")
    report_writer = next(a for a in agents if a.role == "Technical Report Writer")
    
    petrophysics_analysis_task = Task(
        name="petrophysical_analysis",
        description=(
            "First review the well completion report to identify all reservoirs (siliciclastic or saline) that exhibit key characteristics indicative of potential CO₂ storage.\n"
            "Examine the petrophysical logs and measurements of each reservoir. Analyze parameters such as: "
            "porosity, permeability, and fluid saturation to assess the quality of the identified reservoirs. \n"
            "Also perform an indepth analysis on the pressure and temperature condition in the reservoirs. Also give insight into the reservoirs' chemical reactivity.\n"
            "Supplement your evaluation by using the arxiv_search and internet_search tool to gather case studies and recent research on petrophysical assessments. "
            "Craft your search queries to target research papers that discusses the petrophysics of the well, formation, area, or field described in the report. "
            "Integrate insights from the well report with findings from arxiv_search and internet_search to generate your final response."
        ),
        agent=petrophysicist,
        expected_output="A detailed report of the analysis of the petrophysical evaluation of the reservoirs, highlighting their CO₂ storage potential."
    )

    core_analysis_task = Task(
        name="core_analysis",
        description=(
            "If any, first analyze the core sample information provided in the well completion report. Focus on evaluating: "
            "Porosity distribution, Permeability trends, Grain size and sorting, and Mineralogy to determine the suitability of each reservoir for CO₂ storage. \n"
            "Enhance your analysis by leveraging the arxiv_search and internet_search tools to find recent advancements or case studies in core analysis of these reservoirs. "
            "Ensure your search queries are tailored to the retrieve core information specific to the well, formation, area, or field in the well report. "
            "Combine the internal core analysis with external research results from arxiv_search and internet_search to generate a comprehensive response."
        ),
        agent=core_analyst,
        expected_output="A detailed assessment of the core samples and their implications for CO₂ storage potential in the reservoirs."
    )

    structural_analysis_task = Task(
        name="structural_analysis",
        description=(
            "Examine the structural geological information in the well completion report. Identify and assess fault networks, fractures, "
            "and sealing systems that could impact each reservoir's integrity and CO₂ storage potential. \n"
            "For additional context, invoke the arxiv_search and internet_search tool to retrieve the latest literature on structural controls. "
            "Ensure your search queries are specifically tailored retrieve fault or seal system information related to the well, formation, area, or field described in the report. "
            "Integrate the internal structural data with findings from arxiv_search and internet_search to generate a thorough and cohesive response."
        ),
        agent=structural_geologist,
        expected_output="An report detailing the structures that overlies each reservoir for CO₂ storage potential."
    )

    generate_report_task = Task(
        name="generate_technical_report",
        description=(
            "Compile a 3000-word technical report that synthesizes insights from the petrophysicist, "
            "core analyst, and structural geologist agents on the CO2 storage potential in the well."
            "The report should include, but not be limited to:\n"
            "- An executive summary of the findings.\n"
            "- List the identified reservoir and give a detailed discussion on each and their CO₂ storage potential.\n"
            "- Using the M.H rating system outlined in https://www.mdpi.com/2071-1050/15/8/6599, rank (on a scale of 1 -5) and tabulate the suitability of the reservoirs for CO2 storage based on the following criteria: \n"
            " - storage capacity, storage efficiency, containment and integrity, injection rate, safety risk and mitigation, residual trapping and potential to improve.\n" 
            "- Identification of any potential wellbore drilling, leakage, or injection risks (such as ).\n"
            "- Give recommendations for CO₂ injection and any identified uncertainties.\n"
            "Ensure that your final report integrates both the internal data from the well completion report and the external insights obtained via targeted internet and arxiv results. "
            "Use the combined results to generate a robust, evidence-based report. The report must be full sentences."
            "Using the save_co2_report_to_pdf tool, save the report into a pdf file on the system"
        ),
        agent=report_writer,
        expected_output="A comprehensive technical report detailing the CO₂ storage potential of the reservoirs and associated risks and recommendations."
    )
    
    return [
        petrophysics_analysis_task,
        core_analysis_task,
        structural_analysis_task,
        generate_report_task
    ]
