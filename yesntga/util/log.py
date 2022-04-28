import logging.handlers
lg = logging.getLogger(__name__)

handler = logging.handlers.TimedRotatingFileHandler(filename='core.log', when='H', interval=1, backupCount=4,
                                                    encoding='utf-8', delay=False)
fmtr = logging.Formatter(fmt="[%(levelname)s @ %(module)s/%(process)d | %(asctime)s] %(message)s")
handler.setFormatter(fmtr)
lg.addHandler(handler)