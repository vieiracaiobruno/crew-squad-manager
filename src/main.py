"""
Crew Squad Manager - Main Entry Point
"""
import os
from dotenv import load_dotenv
from loguru import logger
from src.crew.squad_crew import SquadCrew
from src. utils.logger import setup_logger

def main():
    """
    Main function to execute the Squad Crew workflow
    """
    # Load environment variables
    load_dotenv()
    
    # Setup logger
    setup_logger()
    
    logger.info("🚀 Starting Crew Squad Manager")
    
    # Validate environment variables
    required_vars = ["OPENAI_API_KEY", "COMPOSIO_API_KEY", "GITHUB_TOKEN", 
                     "GITHUB_REPO_OWNER", "GITHUB_REPO_NAME"]
    
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        logger.error(f"❌ Missing required environment variables: {', '.join(missing_vars)}")
        logger.info("Please check your .env file and ensure all required variables are set")
        return
    
    # Example task description
    task_description = """
    Criar uma API REST simples em Python usando Flask para gerenciamento de tarefas (To-Do List) com as seguintes funcionalidades: 
    
    1. Criar uma nova tarefa (título, descrição, status)
    2. Listar todas as tarefas
    3. Obter detalhes de uma tarefa específica
    4. Atualizar uma tarefa existente
    5. Excluir uma tarefa
    6. Marcar tarefa como concluída
    
    Requisitos:
    - Usar SQLite como banco de dados
    - Implementar validações básicas
    - Retornar respostas em JSON
    - Incluir tratamento de erros
    - Adicionar documentação básica
    """
    
    try:
        # Initialize and execute the squad
        squad = SquadCrew()
        
        logger.info("📋 Task Description:")
        logger.info(task_description)
        
        # Execute the workflow
        result = squad.execute(task_description)
        
        logger.success("✅ Squad execution completed!")
        logger.info(f"Result: {result}")
        
    except Exception as e:
        logger.error(f"❌ Error during execution: {str(e)}")
        raise

if __name__ == "__main__":
    main()