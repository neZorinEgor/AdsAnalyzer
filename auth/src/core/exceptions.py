from fastapi import status
from fastapi.exceptions import HTTPException

UserAlreadyExistException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="User by this email already exist."
)

InvalidCredentialsException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid email or password."
)

InvalidTokenException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid token."
)

InvalidTokenTypeException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid token type."
)

ExpiredTokenException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Token has expired."
)

UserIsBlockedException = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="User is blocked."
)

UserIsNotSuperException = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Permission denied."
)
