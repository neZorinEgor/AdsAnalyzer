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
    email: EmailStr | None = None
    jti: str


class JWTTokenInfo(BaseModel):
    refresh_token: str | None = None
    access_token: str
    token_type: str = "Bearer"
