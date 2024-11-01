from fastapi import HTTPException, status


UserByThisEmailAlreadyExistException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="User by this email already exist."
)
