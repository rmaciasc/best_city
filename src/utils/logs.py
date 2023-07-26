import logging
from logging.handlers import TimedRotatingFileHandler


handler = TimedRotatingFileHandler(
    filename="./logs/logs.log", when="D", interval=1, backupCount=15, encoding="utf-8", delay=False
)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)

logger = logging.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.INFO)
