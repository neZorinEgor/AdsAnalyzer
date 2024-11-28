from pydantic import BaseModel


class MessageResponse(BaseModel):
    status: int
    message: str
