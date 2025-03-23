import asyncio

from faststream import FastStream
from faststream.kafka import KafkaBroker

from src.analysis.router import router as analysis_router


if __name__ == "__main__":
    broker = KafkaBroker("localhost:9092")
    app = FastStream(broker)
    # Routing
    broker.include_router(analysis_router)
    # Run microservice
    asyncio.run(
        app.run()
    )
