from src.ads.repository import ADSInfoRepository
from src.ads.service import AnalysisServie


def analysis_service():
    return AnalysisServie(repository=ADSInfoRepository)
