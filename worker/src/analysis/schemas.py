from pydantic import BaseModel


class Message(BaseModel):
    uuid: str
    report_id: int
    yandex_id_token: str
    report_name: str
