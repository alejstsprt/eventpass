import logging
from logging.handlers import RotatingFileHandler


class Logger:
    def __init__(self, name_logger: str, level: int = logging.DEBUG):
        self.logger = logging.getLogger(name_logger)
        if self.logger.handlers:
            return

        self.logger.setLevel(level)

        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] %(name)s: %(message)s"
        )

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        file_handler = RotatingFileHandler(
            filename=f"{name_logger}.log",
            maxBytes=1_000_000,
            backupCount=3,
            encoding="utf-8",
        )
        file_handler.setFormatter(formatter)

        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)

    def info(self, text: str) -> None:
        self.logger.info(text)

    def warning(self, text: str) -> None:
        self.logger.warning(text)

    def error(self, text: str) -> None:
        self.logger.error(text)

    def exception(self, text: str) -> None:
        self.logger.exception(text)


logger_api = Logger("api_logger")
