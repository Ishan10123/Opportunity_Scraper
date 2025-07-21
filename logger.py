import logging
import os
from datetime import datetime

def setup_logger():
    logs_dir = "logs"
    os.makedirs(logs_dir, exist_ok=True)

    log_filename = datetime.now().strftime("run_log_%Y%m%d_%H%M%S.log")
    log_path = os.path.join(logs_dir, log_filename)

    logger = logging.getLogger("sam_scraper")
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    console_handler = logging.StreamHandler()

    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    if not logger.hasHandlers():
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger

def get_logger():
    return logging.getLogger("sam_scraper")
