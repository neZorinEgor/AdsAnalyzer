import logging

import requests

from src.config import settings

logger = logging.getLogger(__name__)


def change_iam_token():
    logger.info("Try change YANDEX_CLOUD_IAM_TOKEN")
    new_iam_token_request = requests.post(
        url=settings.YANDEX_IAM_TOKEN_API_URL,
        json={
            "yandexPassportOauthToken": settings.YANDEX_OAUTH_TOKEN,
        }
    )
    match new_iam_token_request.status_code:
        case 200:
            logger.info("Successful change YANDEX_CLOUD_IAM_TOKEN")
            settings.YANDEX_CLOUD_IAM_TOKEN = new_iam_token_request.json().get("iamToken")
        case _:
            logger.info("Error during request for YANDEX_IAM_TOKEN")
            logger.warning(new_iam_token_request.status_code, new_iam_token_request.text)
