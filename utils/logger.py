import logging
import os
import logging.handlers

class Logger:
    def __init__(self):
        log_dir = os.path.join(os.getcwd(), "data", "logs")
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, "app.log")

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)  # You can change this level dynamically based on environment
        self.logger.propagate = False

        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

        # Set up log rotation to avoid large log files
        file_handler = logging.handlers.RotatingFileHandler(log_file, maxBytes=10*1024*1024, backupCount=5)
        file_handler.setFormatter(formatter)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)

        # Add handlers to logger if not already added
        if not self.logger.handlers:
            self.logger.addHandler(file_handler)
            self.logger.addHandler(stream_handler)

    def log_debug(self, message: str):
        self.logger.debug(message)

    def log_info(self, message: str):
        self.logger.info(message)

    def log_warning(self, message: str):
        self.logger.warning(message)

    def log_error(self, message: str):
        self.logger.error(message)

    def log_exception(self, ex: Exception):
        """Log exception with traceback."""
        self.logger.error("Exception occurred", exc_info=ex)
