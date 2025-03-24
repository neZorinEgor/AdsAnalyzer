from pydantic import BaseModel, EmailStr, constr

from src.auth.models import Role


class UserSchema(BaseModel):
    email: EmailStr
    password: constr(min_length=8, max_length=20)


class LoginUserSchema(UserSchema):
    pass


class RegisterUserSchema(UserSchema):
    pass


class UserSuccessfulRegisterMessage(BaseModel):
    message: str
    user_id: int


class UserPayloadSchema(BaseModel):
    iat: int | float
    exp: int | float
    sub: int
    email: EmailStr | None = None
    role: Role


class JWTTokenInfo(BaseModel):
    refresh_token: str | None = None
    access_token: str
    token_type: str = "Bearer"
