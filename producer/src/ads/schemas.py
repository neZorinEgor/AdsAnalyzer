from pydantic import BaseModel


class Message(BaseModel):
    uuid: str
    report_id: int
    yandex_id_token: str
    report_name: str


class AdsReportInfoSchema(BaseModel):
    id: int
    user_email: str
    report_id: int
    is_ready: bool
    info: str | None = None
    bad_segments: str | None = None
    path_to_df: str | None = None
