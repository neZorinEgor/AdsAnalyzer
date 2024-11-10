from fastapi import status
from fastapi.exceptions import HTTPException


InvalidTokenException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid token."
)

ExpiredTokenException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Token has expired."
)

UserIsBlockedException = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="User is blocked."
)