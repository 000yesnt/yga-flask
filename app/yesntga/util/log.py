import logging.handlers
from logging import DEBUG
lg = logging.getLogger(__name__)

file_handler = logging.handlers.TimedRotatingFileHandler(filename='core.log', when='H', interval=1, backupCount=4,
                                                    encoding='utf-8', delay=False)
std_handler = logging.StreamHandler()

formatter = logging.Formatter(fmt="[%(levelname)s @ %(module)s/%(process)d | %(asctime)s] %(message)s")
std_handler.setFormatter(file_formatter)
file_handler.setFormatter(formatter)

lg.addHandler(file_handler)
lg.addHandler(std_handler)
lg.setLevel(DEBUG)