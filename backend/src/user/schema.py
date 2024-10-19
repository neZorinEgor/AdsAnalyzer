from pydantic import BaseModel, EmailStr


class LoginUser(BaseModel):
    username: str
    password: str


class RegisterUser(LoginUser):
    email: EmailStr




