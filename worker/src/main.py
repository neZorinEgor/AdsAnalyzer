import asyncio

from faststream import FastStream
from faststream.kafka import KafkaBroker

from src.analysis.router import router as analysis_router


broker = KafkaBroker("localhost:9092")
app = FastStream(broker)
# Routing
broker.include_router(analysis_router)

