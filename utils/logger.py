import logging
import os

class Logger:
    def __init__(self):
        log_dir = os.path.join(os.getcwd(), "data", "logs")
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, "app.log")

        logging.basicConfig(
            filename=log_file,
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )
        self.logger = logging.getLogger()

    def log_info(self, message: str):
        self.logger.info(message)

    def log_error(self, message: str):
        self.logger.error(message)
