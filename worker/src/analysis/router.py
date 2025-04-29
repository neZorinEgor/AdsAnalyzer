import logging

from faststream import Depends
from faststream.kafka import KafkaRouter

from src.analysis.dependency import analysis_service
from src.analysis.schemas import Message
from src.analysis.service import AnalysisService
from src.analysis.utils import check_idempotency
from src.config import settings

logger = logging.getLogger(__name__)
router = KafkaRouter()


@router.subscriber(settings.ANALYSIS_TOPIC)
async def analysis(
    message: Message,
    service: AnalysisService = Depends(analysis_service)
) -> None:
    check_idempotency(message.uuid)
    await service.analysis_company(message)
