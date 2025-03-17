import datetime
from typing import Optional, List

from src.ads.core import IADSInfoRepository
from src.ads.model import ADSInfoModel
from src.ads.schemas import ADSInfoSchema
from src.database import session_factory
from sqlalchemy import select, delete, update


class ADSInfoRepository(IADSInfoRepository):
    @staticmethod
    async def save_asd_info(is_ready: bool, optimal_clusters: int, bad_company_segment: str, cluster_image_link: str) -> int:
        async with session_factory() as session:
            save_ads_info_statement = ADSInfoModel(
                uploaded_at=datetime.datetime.today(),
                is_ready=False,
                optimal_clusters=optimal_clusters,
                bad_company_segments=bad_company_segment,
                cluster_image_link=cluster_image_link,
            )
            session.add(save_ads_info_statement)
            await session.commit()
            return save_ads_info_statement.id

    @staticmethod
    async def get_asd_info_by_id(owner_id: int, ads_info_id: int) -> Optional[ADSInfoSchema]:
        # async with session_factory() as session:
        #     ads_info_query_by_id = select(ADSInfoModel).where(ADSInfoModel.owner_id == owner_id).where(ADSInfoModel.id == ads_info_id)
        #     result = await session.execute(ads_info_query_by_id)
        #     result = result.scalar_one_or_none()
        #     return ADSInfoSchema(**result.__dict__) if result else None
        pass

    @staticmethod
    async def delete_asd_info_by_id(user_id: int, ads_info_id: int) -> None:
        pass
