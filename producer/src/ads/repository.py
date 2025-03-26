import datetime
from typing import Optional, List

from src.ads.core import IADSInfoRepository
from src.ads.model import AdsReportModel
from src.ads.schemas import AdsReportInfoSchema
from src.database import session_factory
from sqlalchemy import select, delete, update


class ADSInfoRepository(IADSInfoRepository):
    @staticmethod
    async def get_ads_report_paginate(limit: int, offset: int, user_email: str):
        async with session_factory() as session:
            pagination_query = select(AdsReportModel).where(AdsReportModel.user_email==user_email).offset(offset).limit(limit)
            ads_report_user = await session.execute(pagination_query)
            ads_report_user = ads_report_user.scalars().all()
            return [AdsReportInfoSchema(**i.__dict__) for i in ads_report_user]

    @staticmethod
    async def save_asd_report_info(user_email: str, **kwargs) -> None:
        async with session_factory() as session:
            model = AdsReportModel(user_email=user_email, **kwargs)
            session.add(model)
            await session.commit()

    @staticmethod
    async def get_report_by_id(report_id: int, user_email: str) -> Optional[AdsReportInfoSchema]:
        async with session_factory() as session:
            query = select(AdsReportModel).where(
                (AdsReportModel.id == report_id) &
                (AdsReportModel.user_email == user_email)
            )
            result = await session.execute(query)
            report = result.scalar_one_or_none()

            if report:
                return AdsReportInfoSchema(**report.__dict__)
            return None
