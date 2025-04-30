from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse


from src.ads.dependency import ads_token, ads_service
from src.ads.service import AdsService

from src.settings import settings


router = APIRouter(prefix="/ads", tags=["ADS"])


@router.get(path="/yandex/oauth/login", tags=["ADS"])
def yandex_oauth():
    return RedirectResponse(f"https://oauth.yandex.ru/authorize?response_type=code&client_id={settings.CLIENT_ID}")


@router.post("/report/create")
async def analyze_company(
    company_id: int = 97236485,
    token: str = Depends(ads_token),
    service: AdsService = Depends(ads_service)
):
    return await service.generate_report_by_company(company_id=company_id, token=token)


@router.get("/reports/paginate")
async def paginate_user_report(
    limit: int,
    offset: int,
    token: str | None = Depends(ads_token),
    service: AdsService = Depends(ads_service)
):
    return await service.paginate_user_report(limit=limit, offset=offset, token=token)


@router.get("/report/{report_id}")
async def get_full_report_information(
    report_id: int,
    token: str | None = Depends(ads_token),
    service: AdsService = Depends(ads_service)
):
    return await service.get_report_info_by_id(report_id=report_id, token=token)


@router.post(path="/companies")
async def get_user_companies(
    token: str | None = Depends(ads_token),
    service: AdsService = Depends(ads_service)
):
    return await service.get_user_companies(token=token)
