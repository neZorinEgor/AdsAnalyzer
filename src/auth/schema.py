from pydantic import BaseModel, EmailStr, conbytes, constr


class UserSchema(BaseModel):
    email: EmailStr
    password: constr(min_length=8)


class LoginUserSchema(UserSchema):
    pass


class RegisterUserSchema(UserSchema):
    pass


class JWTTokenInfoSchema(BaseModel):
    access_token: str
    token_type: str
