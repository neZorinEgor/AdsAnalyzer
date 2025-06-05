import logging

from faststream import Depends
from faststream.kafka import KafkaRouter

from src.analysis.dependency import analysis_service
from src.analysis.schemas import AnalysisMessage
from src.analysis.service import AnalysisService
from src.analysis.utils import check_idempotency
from src.config import settings

logger = logging.getLogger(__name__)
router = KafkaRouter()


@router.subscriber(
    settings.KAFKA_ANALYSIS_TOPIC,
)
async def analysis(
    message: AnalysisMessage,
    service: AnalysisService = Depends(analysis_service)
) -> None:
    check_idempotency(uuid=message.uuid)
    await service.analysis_company(message)
