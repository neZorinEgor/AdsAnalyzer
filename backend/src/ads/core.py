from abc import ABC, abstractmethod
from typing import Optional, List

from src.ads.schemas import ADSInfoSchema


class IADSInfoRepository(ABC):
    @staticmethod
    @abstractmethod
    async def save_asd_info(owner_id: int, **kwargs) -> int:
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    async def get_all_asd_info(owner_id: int) -> Optional[ADSInfoSchema]:
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    async def get_asd_info_by_id(owner_id: int, ads_info_id: int) -> Optional[List[ADSInfoSchema]]:
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    async def delete_asd_info_by_id(user_id: int, ads_info_id: int) -> None:
        raise NotImplementedError()
