from abc import ABC, abstractmethod


class IADSRepository(ABC):
    @staticmethod
    @abstractmethod
    async def save_asd_report_info(user_email: str, **kwargs) -> int:
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    async def get_ads_report_paginate(limit: int, offset: int, user_email: str):
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    async def get_report_info_by_id(report_id: int, user_email: str):
        raise NotImplementedError()
