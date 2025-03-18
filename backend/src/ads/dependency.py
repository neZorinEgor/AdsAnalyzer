from src.ads.repository import ADSInfoRepository
from src.ads.service import AutoAnaalyzerService


def analysis_service():
    return AutoAnaalyzerService(repository=ADSInfoRepository)
