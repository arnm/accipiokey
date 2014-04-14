import logging

Logger = logging.getLogger('Accipio')
Logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

formatter = logging.Formatter('[%(name)s][%(levelname)s] %(message)s')
ch.setFormatter(formatter)

ch.setFormatter(formatter)

Logger.addHandler(ch)
