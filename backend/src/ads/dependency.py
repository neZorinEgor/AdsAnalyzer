from src.ads.repository import ADSInfoRepository
from src.ads.service import PreprocessingServie


def preprocessing_service():
    return PreprocessingServie(repository=ADSInfoRepository)
