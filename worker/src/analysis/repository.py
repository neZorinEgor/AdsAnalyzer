from sqlalchemy import update

from src.analysis.core import IAnalysisRepository
from src.analysis.model import AdsReportModel
from src.database import session_factory


class SQLAnalysisRepository(IAnalysisRepository):
    @staticmethod
    async def update_company_report_info(report_id: int, **kwargs):
        async with session_factory() as session:
            update_statement = update(AdsReportModel).where(AdsReportModel.report_id == report_id).values(**kwargs)
            await session.execute(update_statement)
            await session.commit()
