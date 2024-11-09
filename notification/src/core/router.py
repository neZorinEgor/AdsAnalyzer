from fastapi import APIRouter, Depends

from src.core.auth.dependency import AuthDependency
from src.core.auth.schema import UserTokenPayloadSchema
from src.core.service import NotificationService

router = APIRouter(prefix="/notification")


@router.post("/send")
def send_email(user_credentials: UserTokenPayloadSchema = Depends(AuthDependency.not_banned_user)):
    try:
        NotificationService.send_email(user_credentials.email)
    except Exception as e:
        return str(e)
