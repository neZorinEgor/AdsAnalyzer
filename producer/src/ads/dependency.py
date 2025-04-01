from typing import Annotated

from src.ads.repository import ADSInfoRepository
from src.ads.service import AutoAnaalyzerService
from fastapi import Cookie, Depends


def ads_token(ads_analyzer: Annotated[str | None, Cookie()] = None):
    return ads_analyzer


def user_payload(token: str | None = Depends(ads_token)):
    from yandexid import YandexID
    return YandexID(token).get_user_info_json()


def analysis_service():
    return AutoAnaalyzerService(repository=ADSInfoRepository)

