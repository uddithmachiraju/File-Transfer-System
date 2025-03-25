import os 
import logging 
from datetime import datetime

log_bas_dir = "logs"
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") 
log_dir = os.path.join(log_bas_dir, timestamp) 

os.makedirs(log_bas_dir, exist_ok = True) 

def get_logger(file_name):
    """
    Create a logger that logs to a file inside a time-stamped folder"""
    
    log_filename = os.path.join(log_dir, f"{file_name}.log") 
    
    logger = logging.getLogger(file_name) 
    logger.setLevel(logging.INFO) 

    # Remove any existing handlers to prevent duplication
    if logger.hasHandlers():
        logger.handlers.clear() 

    # File handler
    file_handler = logging.FileHandler(log_filename, mode = 'a')
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", datefmt = '%Y-%m-%d %H:%M:%S')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    logger.propagate = False 

    return logger 