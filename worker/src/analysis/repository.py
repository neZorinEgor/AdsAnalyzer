from src.analysis.core import IAnalysisRepository


class SQLAnalysisRepository(IAnalysisRepository):
    @staticmethod
    async def update_company_report_info(report_id: int, **kwargs):
        pass
