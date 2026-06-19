import logging
import os

# Create logs directory automatically
os.makedirs(
    "logs",
    exist_ok=True
)

# Configure logging
logging.basicConfig(
    filename="logs/app.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


def log(message):
    """
    Log normal information.
    """
    print(message)
    logging.info(message)


def log_error(message):
    """
    Log errors.
    """
    print(f"ERROR: {message}")
    logging.error(message)


def log_warning(message):
    """
    Log warnings.
    """
    print(f"WARNING: {message}")
    logging.warning(message)