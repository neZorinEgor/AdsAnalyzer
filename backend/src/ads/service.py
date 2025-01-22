import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
from io import StringIO, BytesIO
import asyncio
from typing import Type
from fastapi.responses import StreamingResponse

from src.ads.exceptions import report_not_founded
from src.ads.repository import ADSInfoRepository
from src.report.core import ReportType
from src.report.factory import report_factory
from src.s3 import s3_client
from celery import shared_task

import pandas as pd

from src.ads.core import IADSInfoRepository
from src.settings import settings
from src.utils import zip_files

matplotlib.use("agg")


class PreprocessingServie:
    def __init__(self, repository: Type[IADSInfoRepository]):
        self.__repository = repository()

    async def preprocessing_dataset(
            self,
            dataset_csv: str,
            filename: str,
            user_id: int,
            report_type: ReportType
    ):
        await self.__repository.save_asd_info(owner_id=user_id, report_name=filename)
        dataframe = pd.read_csv(StringIO(dataset_csv), header=4, low_memory=False)
        columns_to_drop = [col for col in dataframe.columns if dataframe[col].nunique() <= 1]
        dataframe.drop(columns=columns_to_drop, inplace=True)
        plt.figure(figsize=(15, 15))
        gs = gridspec.GridSpec(3, 2, height_ratios=[1, 1, 1])

        ax1 = plt.subplot(gs[0, 0])
        sns.countplot(data=dataframe, x='Возраст', hue='Пол', palette='Blues', ax=ax1)
        ax1.set_title('Соотношение мужчин и женщин разного возраста')
        ax1.set_ylabel('Количество')
        ax1.set_xlabel('Возраст')

        ax2 = plt.subplot(gs[0, 1])
        sns.countplot(data=dataframe, x='Возраст', hue='Группа', palette='Greens', ax=ax2)
        ax2.set_title('Группа в зависимости от возраста')
        ax2.set_ylabel('Количество')
        ax2.set_xlabel('Возраст')

        ax3 = plt.subplot(gs[1, 0])
        sns.countplot(data=dataframe, x='Тип операционной системы', hue='Тип инвентаря', palette='Oranges', ax=ax3)
        ax3.set_title('Условия показа в зависимости от операционной системы')
        ax3.set_ylabel('Количество')
        ax3.set_xlabel('Тип операционной системы')

        ax4 = plt.subplot(gs[1, 1])
        sns.countplot(data=dataframe, x='Тип операционной системы', hue='Уровень платежеспособности', palette='YlOrBr',
                      ax=ax4)
        ax4.set_title('Уровень платежеспособности в зависимости от операционной системы')
        ax4.set_ylabel('Количество')
        ax4.set_xlabel('Тип операционной системы')

        ax5 = plt.subplot(gs[2, 0])
        sns.countplot(data=dataframe, x='Тип операционной системы', hue='Группа', palette='YlOrRd', ax=ax5)
        ax5.set_title('Группа в зависимости от операционной системы')
        ax5.set_ylabel('Количество')
        ax5.set_xlabel('Тип операционной системы')

        ax6 = plt.subplot(gs[2, 1])
        sns.countplot(data=dataframe, x='Тип устройства', hue='Тип инвентаря', palette='Purples', ax=ax6)
        ax6.set_title('Условие показа в зависимости от типа устройства')
        ax6.set_ylabel('Количество')
        ax6.set_xlabel('Тип устройства')

        plt.tight_layout()
        report_image_buffer = BytesIO()
        plt.savefig(report_image_buffer, format="png")
        report_image_buffer.seek(0)

        report_generator = report_factory.create(report_type=ReportType(report_type))
        report = report_generator.generate(image=report_image_buffer)
        report_steem = BytesIO()
        report.save(report_steem)
        report_steem.seek(0)
        await s3_client.upload_file(
            bucket=settings.S3_BUCKETS,
            key=f"{user_id}/{filename}.zip",
            file=zip_files(
                [
                    (report_steem, f"{filename}.docx")
                ]
            )
        )

    async def download_ads_report(self, owner_id: int, report_id: int):
        ads_info = await self.__repository.get_asd_info_by_id(owner_id=owner_id, ads_info_id=report_id)
        if not ads_info:
            raise report_not_founded
        report = await s3_client.get_file(bucket=settings.S3_BUCKETS, key=...)
        return StreamingResponse(
            content=BytesIO(report),
            media_type="application/zip",
            headers={
                "Access-control-Expose-Headers": "Content-Disposition",
                "Content-Disposition": f"attachment; filename={ads_info.report_name}.zip"
            }
        )


@shared_task
def distributed_preprocessing_dataset(
        dataset_csv: str,
        filename: str,
        user_id: int,
        report_type: ReportType
):
    service = PreprocessingServie(repository=ADSInfoRepository)
    asyncio.run(
        service.preprocessing_dataset(dataset_csv, filename, user_id, report_type)
    )
