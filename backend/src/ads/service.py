from typing import Type

from src.ads.core import IADSInfoRepository


class PreprocessingServie:
    def __init__(self, repository: Type[IADSInfoRepository]):
        self.__repository = repository()

