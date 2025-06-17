import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    RABBIT_USER: str = os.getenv("RABBIT_USER", "eventpass")
    RABBIT_PASSWORD: str = os.getenv("RABBIT_PASSWORD", "eventpass12345")
    QUEUE_NAME: str = os.getenv("QUEUE_NAME", "notifications")

    EMAIL: str = os.getenv("EMAIL", "None")
    PASSWORD_KEY: str = os.getenv("PASSWORD_KEY", "None")


config = Settings()
