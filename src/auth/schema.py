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
    is_banned: bool
    is_superuser: bool


class UserSuccessfulRegisterMessage(BaseModel):
    message: str
    user_id: int


class UserFromDatabaseSchema(BaseModel):
    id: int
    email: EmailStr
    password: str
    register_at: datetime.datetime
    is_banned: bool
    is_superuser: bool


class UserTokenPayloadSchema(BaseModel):
    iat: int | float
    exp: int | float
    sub: int
    email: EmailStr
    is_banned: bool
    is_superuser: bool


class JWTTokenInfo(BaseModel):
    access_token: str
    token_type: str
