import logging
from logging.handlers import RotatingFileHandler
import os
from colorama import Fore, Style, init

init(autoreset=True)

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "app.log")

class ColorFormatter(logging.Formatter):
    COLORS = {
        'DEBUG': Fore.CYAN,
        'INFO': Fore.GREEN,
        'WARNING': Fore.YELLOW,
        'ERROR': Fore.RED,
        'CRITICAL': Fore.RED + Style.BRIGHT,
    }

    def format(self, record):
        color = self.COLORS.get(record.levelname, Fore.WHITE)
        msg = super().format(record)
        return f"{color}{msg}{Style.RESET_ALL}"

formatter = ColorFormatter(
    fmt="%(asctime)s | %(levelname)-8s | %(module)s:%(lineno)d - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)

file_formatter = logging.Formatter(
    fmt="%(asctime)s | %(levelname)-8s | %(module)s:%(lineno)d - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

file_handler = RotatingFileHandler(LOG_FILE, maxBytes=10*1024*1024, backupCount=5)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(file_formatter)

logger = logging.getLogger("app")
logger.setLevel(logging.DEBUG)
logger.addHandler(console_handler)
logger.addHandler(file_handler)
logger.propagate = False

for name in ["uvicorn", "uvicorn.error", "uvicorn.access", "fastapi"]:
    log = logging.getLogger(name)
    log.handlers = [console_handler, file_handler]
    log.setLevel(logging.DEBUG)