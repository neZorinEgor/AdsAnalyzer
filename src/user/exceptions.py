from fastapi import HTTPException, status


bad_user_credentials_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="User not founded, check username or password."
)

user_banned_exceptions = HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is banned. Permission denied."
        )
user_already_exist_exception = HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User by this email or username already exist"
        )

token_not_founded_exception = HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Token not founded",
        )

bad_token_exception = HTTPException(
            detail="Uncorrected token",
            status_code=status.HTTP_403_FORBIDDEN,
        )
