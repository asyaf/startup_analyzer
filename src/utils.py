import logging
import random
import string


def setup_logger():
    logger = logging.getLogger('analysis')
    logger.setLevel(logging.DEBUG)
    log_file = logging.FileHandler('log.txt', 'w', 'utf-8')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    log_file.setFormatter(formatter)
    logger.addHandler(log_file)
    return logger


logger = setup_logger()


def random_string(size=3, chars=string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))
