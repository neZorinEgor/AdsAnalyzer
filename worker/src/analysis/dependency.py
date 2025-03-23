# from faststream import Depends
from src.analysis.service import AnalysisService
from src.analysis.repository import SQLAnalysisRepository
from src.filestorage import S3Client


def analysis_service() -> AnalysisService:
    return AnalysisService(
        repository=SQLAnalysisRepository,
        filestorage=S3Client,
    )

