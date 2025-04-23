"""
Logging utilities for the Corezoid SDK.
"""

import logging
import sys
from typing import Optional


def get_logger(name: str = "corezoid", level: Optional[int] = None) -> logging.Logger:
    """
    Get a logger for the Corezoid SDK.
    
    Args:
        name: The logger name
        level: The log level (defaults to WARNING)
        
    Returns:
        The logger
    """
    logger = logging.getLogger(name)
    
    if level is not None:
        logger.setLevel(level)
    elif not logger.handlers:
        # Only set the default level if no handlers have been configured
        logger.setLevel(logging.WARNING)
    
    if not logger.handlers:
        # Add a handler if none exists
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    return logger


# Default logger
logger = get_logger()
