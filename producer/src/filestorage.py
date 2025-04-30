import logging
from contextlib import asynccontextmanager
from src.settings import settings

from botocore.exceptions import ClientError
from aiobotocore.session import get_session

logger = logging.getLogger(__name__)


class S3Client:
    def __init__(
            self: "S3Client",
            access_key: str,
            secret_key: str,
            endpoint_url: str,
    ):
        self.__config = {
            "aws_access_key_id": access_key,
            "aws_secret_access_key": secret_key,
            "endpoint_url": endpoint_url,
        }
        self.__session = get_session()

    @asynccontextmanager
    async def __get_client(self):
        async with self.__session.create_client("s3", **self.__config) as client:
            yield client

    async def create_bucket(self, bucket_name: str):
        async with self.__get_client() as client:
            try:
                await client.create_bucket(Bucket=bucket_name)
                logger.info("Successful create bucket")
            except ClientError as e:
                match e.response['Error']['Code']:
                    case "BucketAlreadyOwnedByYou":
                        logger.warning("Bucket already exist")

    async def upload_file(self, bucket: str, key: str, file: bytes):
        async with self.__get_client() as client:
            return await client.put_object(Bucket=bucket, Key=key, Body=file)

    async def get_file(self, bucket: str, key: str) -> bytes:
        async with self.__get_client() as client:
            response = await client.get_object(Bucket=bucket, Key=key)
            async with response['Body'] as stream:
                return await stream.read()

    async def delete_file(self, bucket: str, key: str):
        async with self.__get_client() as client:
            return await client.delete_object(Bucket=bucket, Key=key)


s3_client = S3Client(
    access_key=settings.AWS_ACCESS_KEY_ID,
    secret_key=settings.AWS_SECRET_ACCESS_KEY,
    endpoint_url=settings.s3_endpoint_url,
)
