"""
Tech Lead Agent
Responsible for technical specifications and issue creation
"""
from crewai import Agent
from loguru import logger

def create_tech_lead_agent(llm, tools) -> Agent:
    """
    Create the Tech Lead agent
    
    Args:
        llm: Language model instance
        tools:  List of tools available to the agent
        
    Returns: 
        Agent instance
    """
    logger.info("Creating Tech Lead agent")
    
    return Agent(
        role="Tech Lead",
        goal="""Analyze functional specifications, create technical specifications, 
        and break down work into GitHub issues with proper sequencing""",
        backstory="""You are a seasoned Tech Lead with 15 years of software development 
        experience. You have deep knowledge of software architecture, design patterns, and 
        best practices. You excel at breaking down complex requirements into manageable tasks 
        and creating clear technical specifications.  You understand the importance of proper 
        task sequencing and dependencies.""",
        verbose=True,
        allow_delegation=False,
        llm=llm,
        tools=tools
    )