"""
Developer Agent
Responsible for implementing solutions based on issues
"""
from crewai import Agent
from loguru import logger

def create_developer_agent(llm, tools) -> Agent:
    """
    Create the Developer agent
    
    Args:
        llm: Language model instance
        tools: List of tools available to the agent
        
    Returns: 
        Agent instance
    """
    logger.info("Creating Developer agent")
    
    return Agent(
        role="Senior Developer",
        goal="""Implement high-quality code solutions based on technical specifications 
        and issue requirements""",
        backstory="""You are a Senior Developer with 8 years of experience in Python development. 
        You write clean, maintainable, and well-documented code. You follow SOLID principles, 
        design patterns, and best practices. You always consider edge cases, error handling, 
        and code quality.  You take pride in your work and strive for excellence.""",
        verbose=True,
        allow_delegation=False,
        llm=llm,
        tools=tools
    )