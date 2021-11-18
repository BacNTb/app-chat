import logging

def logging_message(PATH_FILE):
    logging.basicConfig(filename=PATH_FILE, filemode='a', format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    return logger
