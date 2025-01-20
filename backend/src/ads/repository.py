from src.ads.core import IADSInfoRepository


class ADSInfoRepository(IADSInfoRepository):
    @staticmethod
    async def save_asd_info() -> int:
        pass

    @staticmethod
    async def get_asd_info_by_id(user_id: int, ads_info_id: int) -> ...:
        pass

    @staticmethod
    async def delete_asd_info_by_id(user_id: int, ads_info_id: int) -> None:
        pass
