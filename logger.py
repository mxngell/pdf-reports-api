from logging import Formatter, StreamHandler, basicConfig, getLogger
from logging.handlers import RotatingFileHandler
import logging

from config import settings

basicConfig(
    level=logging.INFO,
    format="%(levelname)-8s %(asctime)s | %(name)s : %(message)s",
    datefmt="%d.%m.%Y %H:%M:%S",
    encoding="utf-8",
    handlers=[
        StreamHandler()
    ]
)

logging.getLogger('fontTools').setLevel(logging.WARNING)
logging.getLogger('fontTools').propagate = False

log = getLogger("ROOT")
reports_log = getLogger("REPORTS_LOG")

reports_log.setLevel(logging.INFO)
reports_log.propagate = False
reports_log_file_handler = RotatingFileHandler(
    filename=f"{settings.LOGS_DIR}/reports.log",
    maxBytes=5*1024*1024,
    backupCount=2,
    encoding="utf-8"
)
reports_log_formatter = Formatter(
    fmt="%(asctime)s | %(name)s : Report with ID=%(report_id)s, " \
    "filename=%(report_filename)s, file_path=%(file_path)s was generated",
    datefmt="%d.%m.%Y %H:%M:%S",
)
reports_log_file_handler.setFormatter(reports_log_formatter)
reports_log.handlers = [reports_log_file_handler]