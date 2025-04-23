from faststream import FastStream
from faststream.kafka import KafkaBroker

from src.analysis.router import router as analysis_router
from src.config import BASE_DIR, settings

broker = KafkaBroker("localhost:9092",)
app = FastStream(broker)
broker.include_router(analysis_router)


# @app.on_startup
# def startup():
#     print(settings.PATH_TO_DIFFERENCE_PROMPT)

