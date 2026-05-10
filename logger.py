import logging
import sys
import os

# Create logs directory if not exists
os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/app.log", mode="a"),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)