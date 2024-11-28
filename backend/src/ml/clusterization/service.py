from fastapi import UploadFile
import pandas as pd
import joblib
from sklearn.cluster import KMeans

from src.ml.clusterization.core import IMLRepository


class MLService:
    def __init__(self, repository):
        self.__repository: IMLRepository = repository()

    async def create_clusterization_model(self, owner: int, endpoint_path: str, dataset: UploadFile):
        data_frame = pd.read_csv(dataset.file)
        data_frame.dropna(inplace=True)
