from typing import Type
from warnings import filterwarnings

import shap
import numpy as np
import pandas as pd

from lightgbm import LGBMClassifier
from imblearn.under_sampling import RandomUnderSampler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.metrics import classification_report

from src.analysis.core import IAnalysisRepository, IFileStorage
from src.analysis.schemas import Message

filterwarnings("ignore")


class AnalysisService:
    # Dependency Inversion & Injection
    def __init__(
            self,
            repository: Type[IAnalysisRepository],
            filestorage: Type[IFileStorage]
    ):
        self.__repository = repository()
        self.__filestorage = filestorage()

    async def __download_yandex_report(self) -> pd.DataFrame:
        pass

    async def kill_cpu_and_gpu_by_ml(self, message: Message) -> None:
        """
        Automatically analysis ads-company.

        :param message: message from kafka with user token and uuid
        :return: `None`
        """
        company_df = await self.__download_yandex_report()
        if not company_df:
            # If the report cannot be generated online, an error is returned.
            await self.__repository.update_company_report_info(report_id=message.report_id, info="Error: report cannot be generated online.")
            return
