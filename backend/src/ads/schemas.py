from pydantic import BaseModel


class ADSInfoSchema(BaseModel):
    id: int
    report_name: str
