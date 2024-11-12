from pydantic import BaseModel, constr, EmailStr


class UserSchema(BaseModel):
    email: EmailStr
    password: constr(min_length=8)


class LoginUserSchema(UserSchema):
    pass


class RegisterUserSchema(UserSchema):
    pass
