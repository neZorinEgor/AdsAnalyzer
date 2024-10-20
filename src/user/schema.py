from pydantic import BaseModel, EmailStr


class LoginUser(BaseModel):
    username: str
    password: str


class RegisterUser(LoginUser):
    email: EmailStr


class UserReadInfo(BaseModel):
    username: str
    register_at: str
    email: EmailStr
    id: int
