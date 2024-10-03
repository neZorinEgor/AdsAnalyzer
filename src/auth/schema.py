from pydantic import BaseModel


class POSTUser(BaseModel):
    user_id: int
    username: str
    password: str
