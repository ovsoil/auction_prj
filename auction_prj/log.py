import logging
from logging.handlers import RotatingFileHandler


logfmt = '%(asctime)s %(filename)-12s %(levelname)-8s %(message)s'
logging.basicConfig(format=logfmt)
# console log: StreamhandlerHandler, loglevel=warning
console = logging.StreamHandler()
console.setLevel(logging.WARNING)
formatter = logging.Formatter(logfmt)
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

# file log: RotatingFileHandler, 5 * 1M
rthandler = RotatingFileHandler('auction_prj.log', maxBytes=1 * 1024 * 1024, backupCount=5)
rthandler.setLevel(logging.INFO)
formatter = logging.Formatter(logfmt)
Rthandler.setFormatter(formatter)
logging.getLogger('').addHandler(rthandler)
