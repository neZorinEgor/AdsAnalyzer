from pydantic import BaseModel, EmailStr


class UserTokenPayloadSchema(BaseModel):
    iat: int | float
    exp: int | float
    sub: int
    email: EmailStr
    is_banned: bool
    is_superuser: bool
    