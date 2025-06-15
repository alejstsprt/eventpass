import asyncio
import logging

from backend.notify_service.app.broker.consumer import start_consuming

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    asyncio.run(start_consuming())
