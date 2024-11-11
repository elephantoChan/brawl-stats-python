from datetime import datetime
from enum import Enum


class Log:
    COLORS = {
        "INFO": "\033[94m",  # Blue
        "WARNING": "\033[93m",  # Yellow
        "ERROR": "\033[91m",  # Red
        "ENDC": "\033[0m",  # Reset color
    }

    def log(self, message: str, level: str = "INFO"):
        """
        Logs a message with a timestamp and color.

        Parameters:
            message (str): The message to log.
            level (str): The log level ('INFO', 'WARNING', 'ERROR').
        """
        if level not in self.COLORS:
            level = "INFO"

        color = self.COLORS[level]
        endc = self.COLORS["ENDC"]
        timestamp = datetime.now().strftime("[%d-%m-%Y %H:%M:%S]")
        print(f"{color}{timestamp} {level}: {message}{endc}")


class LogLevels(Enum):
    info = "INFO"
    warn = "WARNING"
    err = "ERROR"
