import datetime
import logging
from contextlib import asynccontextmanager

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from faststream import FastStream
from faststream.kafka import KafkaBroker
from pytz import utc

from src.analysis.router import router as analysis_router
from src.config import settings
from src.utils import change_iam_token

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',

)
scheduler = AsyncIOScheduler(timezone=utc)


@asynccontextmanager
async def lifespan(_: FastStream):
    scheduler.add_job(
        func=change_iam_token,
        trigger="interval",
        hours=6,
        next_run_time=datetime.datetime.now()
    )
    scheduler.start()
    yield
    scheduler.shutdown()


broker = KafkaBroker(settings.kafka_url)
app = FastStream(broker, lifespan=lifespan)
broker.include_router(analysis_router)
