from src.database import session_factory
from src.ml.clusterization.core import IMLRepository


class MLRepository(IMLRepository):
    async def find_endpoint_by_path(self, path: str):
        async with session_factory() as session:
            pass
