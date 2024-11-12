from datetime import datetime

COLORS = {
    "INFO": "\033[94m",  # Blue
    "WARNING": "\033[93m",  # Yellow
    "ERROR": "\033[91m",  # Red
    "ENDC": "\033[0m",  # Reset color
}


def log(message: str, level: str = "INFO"):
    """
    Logs a message with a timestamp and color.

    Parameters:
        message (str): The message to log.
        level (str): The log level ('INFO', 'WARNING', 'ERROR').
    """
    if level not in COLORS:
        level = "INFO"
    color = COLORS[level]
    endc = COLORS["ENDC"]
    timestamp = datetime.now().strftime("[%d-%m-%Y %H:%M:%S]")
    print(f"{color}{timestamp} {level}: {message}{endc}")
