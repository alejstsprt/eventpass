from pydantic import BaseSettings


class Settings(BaseSettings):
    rabbitmq_url: str = "amqp://guest:guest@localhost:5672/"
    queue_name: str = "notifications"

    class Config:
        env_file = ".env"


settings = Settings()
