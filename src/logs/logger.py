import logging
from pathlib import Path

APP_DIR  = Path.home() / ".books"
LOG_DIR  = APP_DIR / "logs"
LOG_FILE = LOG_DIR / "countbooks.log"

LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("CountBooks")