# Logger module
import logging

def setup_logger():
    logger = logging.getLogger("joulebot")
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler("joulebot.log")
    file_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger

logger = setup_logger()