from contextlib import asynccontextmanager
from fastapi import UploadFile
from aiobotocore.session import get_session
from aiobotocore.client import AioBaseClient

from src.settings import settings


class S3Client:
    def __init__(self, access_key: str, secret_key: str, endpoint_url: str, bucket_name: str):
        self.session = get_session()
        self.bucket_name = bucket_name
        self.config = {
            "aws_access_key_id": access_key,
            "aws_secret_access_key": secret_key,
            "endpoint_url": endpoint_url,
        }

    @asynccontextmanager
    async def get_client(self) -> AioBaseClient:
        """
        Dependency for inner usage
        """
        async with self.session.create_client("s3", **self.config) as client:
            yield client

    async def upload_file(self, file: UploadFile) -> None:
        """
        Upload file from router
        """
        async with self.get_client() as client:
            await client.put_object(
                Bucket=self.bucket_name,
                Key=file.filename,
                Body=file.file
            )

    async def create_bucket(self) -> None:
        """
        Create bucket
        """
        async with self.get_client() as client:
            await client.create_bucket(Bucket=self.bucket_name)

    async def close(self):
        async with self.get_client() as client:
            client.close()


s3_client = S3Client(
        access_key=settings.S3_ACCESS_KEY,
        secret_key=settings.S3_SECRET_KEY,
        endpoint_url=f"https://{settings.S3_HOST}:{settings.S3_PORT}",
        bucket_name=settings.S3_BUCKET_NAME
    )
