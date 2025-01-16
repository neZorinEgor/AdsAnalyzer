from fastapi import status
from fastapi.exceptions import HTTPException

user_already_exist_exception = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="User by this email already exist."
)


invalid_credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid email or password."
)


invalid_token_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid token."
)


invalid_token_type_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid token type."
)


expired_token_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Token has expired."
)


user_is_blocked_exception = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="User is banned."
)


user_is_not_super_exception = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Permission denied."
)
