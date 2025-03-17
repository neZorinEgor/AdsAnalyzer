from abc import ABC, abstractmethod
from typing import Optional, List

from src.ads.schemas import ADSInfoSchema


class IADSInfoRepository(ABC):
    @staticmethod
    @abstractmethod
    async def save_asd_info(
            is_ready: bool,
            optimal_clusters: int,
            bad_company_segment: str,
            cluster_image_link: str
    ) -> int:
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    async def get_asd_info_by_id(owner_id: int, ads_info_id: int) -> Optional[ADSInfoSchema]:
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    async def delete_asd_info_by_id(user_id: int, ads_info_id: int) -> None:
        raise NotImplementedError()
