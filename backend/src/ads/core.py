from abc import ABC, abstractmethod


class IADSInfoRepository(ABC):
    @staticmethod
    @abstractmethod
    async def save_asd_info() -> int:
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    async def get_asd_info_by_id(user_id: int, ads_info_id: int) -> ...:
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    async def delete_asd_info_by_id(user_id: int, ads_info_id: int) -> None:
        raise NotImplementedError()
