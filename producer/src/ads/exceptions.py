from fastapi import HTTPException, status

report_not_ready_error = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Report not ready."
)


report_not_founded_error = HTTPException(
    status_code=404,
    detail="Report by this id for this user not founded."
)
