from logging.handlers import RotatingFileHandler
import logging

class Logger:
    def __init__(self, name_logger, level=logging.DEBUG):
        self.logger = logging.getLogger(name_logger)
        if self.logger.handlers:
            return

        self.logger.setLevel(level)

        formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(name)s: %(message)s")

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        file_handler = RotatingFileHandler(f'{name_logger}.log', encoding='utf-8')
        file_handler.setFormatter(formatter)

        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)

    def info(self, text: str) -> None:
        self.logger.info(text)

    def warning(self, text: str) -> None:
        self.logger.warning(text)

    def error(self, text: str) -> None:
        self.logger.error(text)