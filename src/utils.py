import logging
import os
import random
import string

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGE_DIR = os.path.join(ROOT_DIR, 'data')
OUT_DIR = os.path.join(ROOT_DIR, 'out')
LOG_FILE_PATH = os.path.join(*[ROOT_DIR, 'out', 'log.txt'])


def setup_logger(log_file_path):
    logger = logging.getLogger('analysis')
    logger.setLevel(logging.DEBUG)
    log_file = logging.FileHandler(log_file_path, 'w', 'utf-8')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    log_file.setFormatter(formatter)
    logger.addHandler(log_file)
    return logger


logger = setup_logger(LOG_FILE_PATH)


def random_string(size=3, chars=string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))
