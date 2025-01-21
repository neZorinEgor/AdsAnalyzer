import datetime

from fastapi import HTTPException, status

report_not_founded = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail={
        "status_code": status.HTTP_404_NOT_FOUND,
        "message": "Report not founded.",
        "timestamp": datetime.datetime.timestamp(datetime.datetime.now(datetime.UTC))
    }
)
