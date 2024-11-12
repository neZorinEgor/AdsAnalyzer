from pydantic import BaseModel, EmailStr, constr


class UserSchema(BaseModel):
    email: EmailStr
    password: constr(min_length=8)


class LoginUserSchema(UserSchema):
    pass


class RegisterUserSchema(UserSchema):
    pass


class UserSuccessfulRegisterMessage(BaseModel):
    message: str
    user_id: int


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


class NewPassword(BaseModel):
    new_password: constr(min_length=8)