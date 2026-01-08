"""
Squad Crew - Orchestrates the entire IT squad workflow
"""
import os
from crewai import Crew, Task, Process
from langchain_openai import ChatOpenAI
from composio_crewai import ComposioToolSet, Action, App
from loguru import logger

from src.agents.project_manager import create_project_manager_agent
from src. agents.tech_lead import create_tech_lead_agent
from src.agents.developer import create_developer_agent
from src.agents. tester import create_tester_agent

class SquadCrew: 
    """
    Manages the IT Squad using CrewAI
    """
    
    def __init__(self):
        """Initialize the squad crew"""
        logger.info("Initializing Squad Crew")
        
        # Initialize OpenAI LLM
        self.llm = ChatOpenAI(
            model=os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview"),
            temperature=0.7
        )
        
        # Initialize Composio toolset
        self.toolset = ComposioToolSet(api_key=os.getenv("COMPOSIO_API_KEY"))
        
        # Get GitHub tools
        self.github_tools = self.toolset.get_tools(apps=[App.GITHUB])
        
        # Create agents
        self.project_manager = create_project_manager_agent(self.llm)
        self.tech_lead = create_tech_lead_agent(self.llm, self.github_tools)
        self.developer = create_developer_agent(self.llm, self.github_tools)
        self.tester = create_tester_agent(self.llm, self.github_tools)
        
        logger.success("Squad Crew initialized successfully")
    
    def execute(self, task_description: str) -> dict:
        """
        Execute the squad workflow
        
        Args:
            task_description: Description of the task to be completed
            
        Returns:
            dict:  Results of the execution
        """
        logger.info("Starting squad execution")
        
        # Task 1: Project Manager creates functional specification
        functional_spec_task = Task(
            description=f"""
            Analyze the following project requirement and create a comprehensive functional specification: 
            
            {task_description}
            
            The functional specification should include:
            1. Project Overview
            2. User Stories
            3. Functional Requirements (detailed list)
            4. Non-Functional Requirements
            5. Acceptance Criteria
            6. Success Metrics
            
            Be thorough and clear.  Think from the user's perspective.
            """,
            agent=self.project_manager,
            expected_output="A comprehensive functional specification document in markdown format"
        )
        
        # Task 2: Tech Lead creates technical specification and issues
        technical_spec_task = Task(
            description=f"""
            Based on the functional specification from the Project Manager, create: 
            
            1. A detailed technical specification including:
               - System Architecture
               - Technology Stack
               - Database Schema (if applicable)
               - API Endpoints (if applicable)
               - Security Considerations
               - Performance Requirements
            
            2. Break down the work into GitHub issues with: 
               - Clear titles
               - Detailed descriptions
               - Labels (feature, bug, documentation, etc.)
               - Logical sequence (dependencies)
               - Estimated complexity
            
            Repository:  {os.getenv('GITHUB_REPO_OWNER')}/{os.getenv('GITHUB_REPO_NAME')}
            
            Create the issues in the GitHub repository using the available tools.
            Number the issues in the order they should be completed.
            """,
            agent=self.tech_lead,
            expected_output="Technical specification document and list of created GitHub issues with their numbers",
            context=[functional_spec_task]
        )
        
        # Task 3: Developer implements the first issue
        development_task = Task(
            description="""
            Review the first issue created by the Tech Lead and implement the solution. 
            
            Your implementation should:
            1. Follow the technical specification
            2. Include proper error handling
            3. Have clear comments and documentation
            4. Follow Python best practices (PEP 8)
            5. Be modular and maintainable
            
            Provide the implementation code and explain your approach.
            """,
            agent=self.developer,
            expected_output="Implementation code with documentation and explanation",
            context=[functional_spec_task, technical_spec_task]
        )
        
        # Task 4: Tester creates and executes tests
        testing_task = Task(
            description="""
            Based on the functional specification, technical specification, and the developer's implementation: 
            
            1. Create comprehensive test cases including:
               - Unit tests
               - Integration tests
               - Edge cases
               - Error scenarios
            
            2. Analyze the implementation for potential bugs
            
            3. Generate a test report with:
               - Test cases executed
               - Results (pass/fail)
               - Bugs found (if any) with: 
                 * Severity (critical, high, medium, low)
                 * Steps to reproduce
                 * Expected vs actual behavior
               - Overall quality assessment
            
            If bugs are found, document them clearly for the developer.
            If no bugs are found, provide final approval recommendation to PM and Tech Lead.
            """,
            agent=self.tester,
            expected_output="Complete test report with test cases, results, and quality assessment",
            context=[functional_spec_task, technical_spec_task, development_task]
        )
        
        # Create the crew
        crew = Crew(
            agents=[self.project_manager, self.tech_lead, self.developer, self.tester],
            tasks=[functional_spec_task, technical_spec_task, development_task, testing_task],
            process=Process.sequential,
            verbose=True
        )
        
        # Execute the crew
        logger.info("Executing crew tasks...")
        result = crew.kickoff()
        
        logger. success("Squad execution completed")
        return result