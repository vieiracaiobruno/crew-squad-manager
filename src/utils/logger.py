"""
Logger configuration using loguru
"""
import os
import sys
from loguru import logger

def setup_logger():
    """
    Setup logger with custom configuration
    """
    # Remove default handler
    logger.remove()
    
    # Get log level from environment or default to INFO
    log_level = os.getenv("LOG_LEVEL", "INFO")
    
    # Add console handler with colors
    logger.add(
        sys.stdout,
        colorize=True,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level:  <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
        level=log_level
    )
    
    # Add file handler
    logger.add(
        "logs/squad_manager.log",
        rotation="500 MB",
        retention="10 days",
        level=log_level,
        format="{time: YYYY-MM-DD HH: mm:ss} | {level:  <8} | {name}:{function} - {message}"
    )
    
    return logger