from fastapi import UploadFile

from src.ml.clusterization.core import IMLRepository


class MLService:
    def __init__(self, repository):
        if not isinstance(repository, IMLRepository):
            raise TypeError(f"Expected {IMLRepository}, got {type(repository)}")
        self.__repository: IMLRepository = repository

    async def create_clusterization_model(self, owner: int, endpoint_path: str, dataset: UploadFile):
        pass
