from fastapi import UploadFile, File

from src.ml.core import IMLRepository


class MLService:
    def __init__(self, repository):
        if not isinstance(repository, IMLRepository):
            raise TypeError(f"Expected {IMLRepository}, got {type(repository)}")
        self.__repository: IMLRepository = repository

    async def create_clusterization_model(self, endpoint_path: str, dataset: UploadFile = File(...)):
        pass
