import os
from contextlib import asynccontextmanager

from aiobotocore.session import get_session, ClientCreatorContext


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
    async def get_client(self) -> ClientCreatorContext:
        async with self.session.create_client("s3", **self.config) as client:
            yield client

    async def upload_file(self, file_path: str):
        object_name = file_path.split(os.sep)[-1]
        async with self.get_client() as client:
            with open(file_path, "rb") as file:
                await client.put_object(
                    Bucket=self.bucket_name,
                    Key=object_name,
                    Body=file
                )

    async def list_files(self):
        """Список всех файлов в бакете."""
        async with self.get_client() as client:
            response = await client.list_objects_v2(Bucket=self.bucket_name)
            return [item['Key'] for item in response.get('Contents', [])]

    async def file_exists(self, file_name: str) -> bool:
        """Проверка, существует ли файл в бакете."""
        files = await self.list_files()
        return file_name in files

    async def create_bucket(self):
        """Создание бакета, если его ещё нет."""
        async with self.get_client() as client:
            try:
                await client.create_bucket(Bucket=self.bucket_name)
                print(f"Бакет '{self.bucket_name}' создан.")
            except client.exceptions.BucketAlreadyExists:
                print(f"Бакет '{self.bucket_name}' уже существует.")
            except client.exceptions.BucketAlreadyOwnedByYou:
                print(f"Бакет '{self.bucket_name}' уже принадлежит вам.")
