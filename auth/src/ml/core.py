from abc import ABC, abstractmethod


class IMLRepository(ABC):
    @abstractmethod
    async def find_endpoint_by_path(self, path: str):
        pass
