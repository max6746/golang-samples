"""
Copyright 2023 Google. This software is provided as-is, without warranty or representation for any use or purpose.
Your use of it is subject to your agreement with Google.
"""

import logging


class Logger:
    """
    Utility to help capture logs and errors across the application in a standarized manner.
    """

    def __init__(self, name, level=logging.DEBUG, file_name=None, formatter=None):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # Default formatter
        if formatter is None:
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        # File handler (optional)
        if file_name:
            file_handler = logging.FileHandler(file_name)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

    def debug(self, msg):
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)

    def critical(self, msg):
        self.logger.critical(msg)
