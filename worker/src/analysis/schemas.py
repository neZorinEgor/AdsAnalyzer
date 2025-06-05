from pydantic import BaseModel


class AnalysisMessage(BaseModel):
    uuid: str
    company_id: int
    yandex_id_token: str
    report_name: str
