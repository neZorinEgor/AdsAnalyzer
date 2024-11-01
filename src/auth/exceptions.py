from fastapi import status
from fastapi.exceptions import HTTPException

UserByThisEmailAlreadyExistException = HTTPException(
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

ExpiredTokenException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Token has expired."
)
