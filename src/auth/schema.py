import datetime

from pydantic import BaseModel, EmailStr, conbytes, constr


class UserSchema(BaseModel):
    email: EmailStr
    password: constr(min_length=8)


class LoginUserSchema(UserSchema):
    pass


class RegisterUserSchema(UserSchema):
    pass


class UserCredentialsSchema(BaseModel):
    id: int
    email: EmailStr


class UserSuccessfulRegisterMessage(BaseModel):
    message: str
    register_user_id: int


class DecodeAccessTokenSchema(BaseModel):
    sub: int
    email: EmailStr
    exp: int | float
    iat: int | float


class JWTTokenInfo(BaseModel):
    access_token: str
    token_type: str
