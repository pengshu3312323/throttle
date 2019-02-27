import logging
import logging.handlers

from throttle import settings


logger = logging.getLogger('error')
logger.setLevel(logging.ERROR)

logging.basicConfig(datefmt=settings.LOG_DATE_FORMAT)

handler = logging.handlers.RotatingFileHandler(
    settings.LOG_FILE_NAME,
    maxBytes=1024 * 1024,
    backupCount=5
    )
handler.setFormatter(logging.Formatter(settings.LOG_FORMAT))

logger.addHandler(handler)
