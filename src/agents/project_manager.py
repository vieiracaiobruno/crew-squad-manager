"""
Project Manager Agent
Responsible for understanding requirements and generating functional specifications
"""
from crewai import Agent
from loguru import logger

def create_project_manager_agent(llm) -> Agent:
    """
    Create the Project Manager agent
    
    Args:
        llm: Language model instance
        
    Returns:
        Agent instance
    """
    logger.info("Creating Project Manager agent")
    
    return Agent(
        role="Project Manager",
        goal="Understand project requirements and create comprehensive functional specifications",
        backstory="""You are an experienced Project Manager with over 10 years of experience 
        in software development projects. You excel at understanding client needs, translating 
        them into clear functional specifications, and ensuring all stakeholders are aligned.  
        You have a keen eye for detail and always think about user experience and business value.""",
        verbose=True,
        allow_delegation=False,
        llm=llm
    )