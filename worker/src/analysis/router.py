import logging

from faststream import Depends
from faststream.kafka import KafkaRouter

from src.analysis.dependency import analysis_service
from src.analysis.schemas import Message
from src.analysis.service import AnalysisService
from src.analysis.utils import check_idempotency
from src.config import settings

router = KafkaRouter()
logger = logging.getLogger(__name__)


@router.subscriber(settings.ANALYSIS_TOPIC)
async def analysis(
    message: Message,
    service: AnalysisService = Depends(analysis_service)
) -> None:
    check_idempotency(message.uuid)
    await service.kill_cpu_and_gpu_by_ml(message)
