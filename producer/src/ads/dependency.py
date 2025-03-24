from typing import Annotated

from src.ads.repository import ADSInfoRepository
from src.ads.service import AutoAnaalyzerService
from fastapi import Cookie


# def ads_

def ads_token(ads_analyzer: Annotated[str | None, Cookie()] = None):
    return ads_analyzer



def analysis_service():
    return AutoAnaalyzerService(repository=ADSInfoRepository)
