from fastapi import UploadFile
from pydantic import create_model

import pandas as pd
from sklearn.cluster import KMeans

from src.core.abstract import ABCRepository


class MLService:
    __repository: ABCRepository = None

    def __init__(self, repository: ABCRepository):
        self.__repository = repository

    def crete_clusterizations(self, endpoint_path: str, dataset: UploadFile):
        data_frame = pd.read_csv(dataset.file)
        data_frame.dropna(inplace=True)
        data_frame = pd.get_dummies(data_frame)
        feature_names = list(data_frame)
        python_types = data_frame.dtypes.map(lambda dtype: dtype.name)
        for column, dtype in zip(feature_names, python_types):
            print(f"Столбец '{column}': {dtype}")
        # schema = create_model("Schema", **{name: (float, ...) for name in feature_names})

