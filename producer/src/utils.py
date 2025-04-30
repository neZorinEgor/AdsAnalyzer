from io import BytesIO
from zipfile import ZipFile, ZIP_DEFLATED

import requests


def zip_files(files: list[tuple[BytesIO, str]]) -> BytesIO:
    zip_buffer = BytesIO()
    with ZipFile(file=zip_buffer, mode="w", compression=ZIP_DEFLATED) as zip_file:
        for file_object, file_name in files:
            file_object.seek(0)
            zip_file.writestr(file_name, file_object.read())
    zip_buffer.seek(0)
    return zip_buffer


def get_user_payload(token: str):
    result = requests.get(
        url="https://login.yandex.ru/info",
        headers={
            "Authorization": f"OAuth {token}"
        }
    )
    return result.json()
