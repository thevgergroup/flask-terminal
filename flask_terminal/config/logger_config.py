import logging
from logging.handlers import RotatingFileHandler
import os

def configure_logger(name):
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Create console handler and set level to info
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    # Check if logs directory exists, if not create it
    if not os.path.exists('logs'):
        os.makedirs('logs', exist_ok=True)
    
    # Create file handler and set level to info
    file_handler = RotatingFileHandler('logs/terminal_activities.log', maxBytes=10240, backupCount=5)
    file_handler.setLevel(logging.INFO)
    file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    
    return logger