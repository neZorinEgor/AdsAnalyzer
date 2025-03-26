from abc import ABC, abstractmethod
from typing import Optional, List


class IADSInfoRepository(ABC):
    @staticmethod
    @abstractmethod
    async def save_asd_report_info(user_email: str, **kwargs) -> int:
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    async def get_ads_report_paginate(limit: int, offset: int, user_email: str):
        raise NotImplementedError()
