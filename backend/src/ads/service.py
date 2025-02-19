from typing import Type
from src.ads.core import IADSInfoRepository
from warnings import filterwarnings

import matplotlib
filterwarnings("ignore")
matplotlib.use("agg")


class AnalysisServie:
    def __init__(self, repository: Type[IADSInfoRepository]):
        self.__repository = repository()
