from contextlib import asynccontextmanager

from src.analysis.core import IFileStorage
from src.config import settings

from aiobotocore.session import get_session


class S3Client(IFileStorage):
    __session = get_session()
    __config = {
        "aws_access_key_id": settings.AWS_ACCESS_KEY_ID,
        "aws_secret_access_key": settings.AWS_SECRET_ACCESS_KEY,
        "endpoint_url": settings.s3_endpoint_url,
    }

    @asynccontextmanager
    async def __get_client(self):
        async with self.__session.create_client("s3", **self.__config) as client:
            yield client

    async def upload_file(self, bucket: str, key: str, file: bytes):
        async with self.__get_client() as client:
            return await client.put_object(Bucket=bucket, Key=key, Body=file)

    async def get_file(self, bucket: str, key: str):
        async with self.__get_client() as client:
            response = await client.get_object(Bucket=bucket, Key=key)
            async with response['Body'] as stream:
                return await stream.read()

    async def delete_file(self, bucket: str, key: str):
        async with self.__get_client() as client:
            return await client.delete_object(Bucket=bucket, Key=key)
