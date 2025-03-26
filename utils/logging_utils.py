"""
Logging configuration for the CO2 Storage Assessment system.
"""

import logging

def setup_logging():
    """Configure the logging system with appropriate format and level."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)
    return logger
