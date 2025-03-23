from abc import ABC, abstractmethod


class IAnalysisRepository(ABC):
    @staticmethod
    @abstractmethod
    async def update_company_report_info(report_id: int, **kwargs):
        pass


class IFileStorage(ABC):
    @abstractmethod
    async def upload_file(self, **kwargs):
        pass

    @abstractmethod
    async def get_file(self, **kwargs):
        pass
