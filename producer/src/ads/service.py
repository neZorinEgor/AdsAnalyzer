import datetime

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
from sklearn.base import BaseEstimator
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from typing import Type
import io

from src.ads.core import IADSInfoRepository
from src.filestorage import s3_client

from warnings import filterwarnings

from src.settings import settings

filterwarnings("ignore")
sns.set_theme()

matplotlib.use("agg")


class AutoAnaalyzerService:
    __wcss_errors: dict = {}            # Сумма внутри-кластерных расстояний
    __percentage_error_diff = {}        # Процентные изменения WCSS
    __optimality_threshold: int = 20    # Порог для определения оптимального количества кластеров
    __optimal_num_cluster: int = 3      # Оптимальное количество кластеров
    __bad_company_segments: str         # Сегменты аудитории, для которой лучше отключить рекламу
    __efficiency_columns: list = ["Показы", "Взвешенные показы", "Клики", "CTR (%)", "wCTR (%)", "Расход (руб.)",
                                  "Ср. цена клика (руб.)", "Ср. ставка за клик (руб.)", "Отказы (%)", "Глубина (стр.)",
                                  "Прибыль (руб.)", ]
    __cluster_img_link: str
    __wcss_img_img_link: str
    __scatter_data: pd.DataFrame

    def __init__(
            self,
            company: pd.DataFrame,
            repository: Type[IADSInfoRepository],
            scaler: Type[BaseEstimator] = MinMaxScaler,
            optimality_threshold: int = 20,
    ):
        self.__company = company
        self.__optimality_threshold = optimality_threshold
        self.scaler = scaler()
        self.__repository = repository()

    async def __clustering_ads(self):
        if "cluster_id" in self.__efficiency_columns:
            self.__efficiency_columns.remove("cluster_id")
        # Определение оптимального количества класстеров
        X = pd.get_dummies(self.__company[self.__efficiency_columns])
        for i in range(1, 11):
            kmeans = KMeans(n_clusters=i, max_iter=1000, init="k-means++", random_state=42)
            self.__wcss_errors[i] = kmeans.fit(X).inertia_
            # Понижение размерности для визуализации
        plt.figure(figsize=(10, 6))
        plt.title("Выбор оптимального количества кластеров методом локтя")
        plt.xlabel("Количество кластеров")
        plt.ylabel("WCSS (Within-Cluster Sum of Squares)")
        plt.xticks(range(1, 11))
        plt.tight_layout()
        plt.plot(self.__wcss_errors.keys(), self.__wcss_errors.values(), marker='o', label="WCSS")
        wcss_values = list(self.__wcss_errors.values())
        max_val = max(list(self.__wcss_errors.values()))
        for i in range(len(wcss_values) - 1):
            diff = wcss_values[i] - wcss_values[i + 1]
            if wcss_values[i] != 0:
                self.__percentage_error_diff[f"{i + 1}-{i + 2}"] = int(diff * 100 / wcss_values[i])
            else:
                self.__percentage_error_diff[f"{i + 1}-{i + 2}"] = 0
            plt.text(x=i + 2.1, y=wcss_values[i + 1] + 200, s=f"-{int(diff * 100 / wcss_values[i])}%")
            plt.axvline(x=i + 1, color="darkgray", linestyle="--", ymax=int(wcss_values[i] * 100 / max_val) / 100)
        plt.axvline(self.__optimal_num_cluster, color="indianred", label="Оптимальный кластер", linestyle="--")
        plt.legend()
        wcss_buf = io.BytesIO()
        plt.savefig(wcss_buf, format='jpg')
        wcss_buf.seek(0)
        wcss_plot_bytes = wcss_buf.getvalue()
        # Save cluster image in S3
        key=f"{datetime.datetime.now(datetime.UTC).timestamp()}_wcss.jpg"
        await s3_client.upload_file(
            bucket=settings.S3_BUCKETS,
            key=key,
            file=wcss_plot_bytes)
        for item in range(len(self.__percentage_error_diff) - 1):
            proc_diff = list(self.__percentage_error_diff.items())[item][1] - list(self.__percentage_error_diff.items())[item + 1][1]
            if proc_diff > self.__optimality_threshold:
                self.__optimal_num_cluster = int(list(self.__percentage_error_diff.items())[item][0][-1])
                break
            else:
                self.__optimal_num_cluster = 3
        # Постройка кластеров
        pca = PCA(n_components=2)
        pca_df = pca.fit_transform(self.scaler.fit_transform(self.__company[self.__efficiency_columns]))
        pca_df = pd.DataFrame(pca_df)
        kmeans = KMeans(n_clusters=self.__optimal_num_cluster, max_iter=1000, init="k-means++", random_state=42)
        predict = kmeans.fit_predict(pca_df)
        pca_df["cluster_id"] = predict
        self.__efficiency_columns.append("cluster_id")
        self.__company["cluster_id"] = predict
        pca_df["cluster_id"] = pca_df["cluster_id"].apply(lambda x: x + 1)
        pca_df.columns = ["x", "y", "cluster_id"]
        # print([i for i in self.__company.columns if i in ["Показы", "Взвешенные показы", "Клики", "CTR (%)", "wCTR (%)", "Расход (руб.)", "Ср. цена клика (руб.)", "Ср. ставка за клик (руб.)", "Отказы (%)", "Глубина (стр.)", "Прибыль (руб.)"]])
        pca_df[["Пол", "Возраст", 'Показы', 'Взвешенные показы', 'Клики', 'CTR (%)', 'wCTR (%)', 'Расход (руб.)', 'Ср. цена клика (руб.)', 'Ср. ставка за клик (руб.)', 'Отказы (%)', 'Глубина (стр.)', 'Прибыль (руб.)']] = self.__company[["Пол", "Возраст", 'Показы', 'Взвешенные показы', 'Клики', 'CTR (%)', 'wCTR (%)', 'Расход (руб.)', 'Ср. цена клика (руб.)', 'Ср. ставка за клик (руб.)', 'Отказы (%)', 'Глубина (стр.)', 'Прибыль (руб.)']]
        self.__scatter_data = pca_df
        # Визуализация кластеров
        centroids = kmeans.cluster_centers_
        plt.figure(figsize=(10, 6))
        for i in np.unique(predict):
            plt.scatter(pca_df.iloc[predict == i, 0], pca_df.iloc[predict == i, 1], label=f'Кластер {i}')
        plt.scatter(centroids[:, 0], centroids[:, 1], s=200, c='black', marker='^', label='Центры кластеров')
        plt.legend(loc='lower right')
        plt.xlabel('Первая главная компонента')
        plt.ylabel('Вторая главная компонента')
        plt.title('Визуализация кластеров с центроидами')
        plt.tight_layout()
        cluster_buf = io.BytesIO()
        plt.savefig(wcss_buf, format='jpg')
        cluster_buf.seek(0)
        cluster_plot_bytes = wcss_buf.getvalue()
        # Save cluster image in S3
        cluster_key = f"{datetime.datetime.now(datetime.UTC).timestamp()}_clusters.jpg"
        await s3_client.upload_file(
            bucket=settings.S3_BUCKETS,
            key=cluster_key,
            file=cluster_plot_bytes
        )
        self.__cluster_img_link = f"{settings.s3_endpoint_url}/{settings.S3_BUCKETS}/{key}"
        await self.__repository.save_asd_info(
            is_ready=True,
            optimal_clusters=self.__optimal_num_cluster,
            bad_company_segment="foobar",
            cluster_image_link=self.__cluster_img_link
        )
        wcss_buf.close()

    async def __define_bad_segments(self, rejection_threshold: int = 100):
        rejection_result = []
        group = self.__company.query("cluster_id==2").groupby(["Пол", "Возраст"])[
            ["CTR (%)", "Ср. цена клика (руб.)", "Отказы (%)", "Глубина (стр.)", "Расход (руб.)", 'Взвешенные показы',
             'Клики', ]
        ].quantile(.5)
        for i, b in group[group["Отказы (%)"] >= rejection_threshold].index:
            if i != "не определен" or b != "не определен":
                rejection_result.append(f"{i}: {b}")
        self.__bad_company_segments = rejection_result if rejection_result else "не выявленно"

    async def analysis(self):
        await self.__clustering_ads()
        await self.__define_bad_segments()
        # self.__analyze_each_cluster()
        return {
            "optimal_cluster": self.__optimal_num_cluster,
            "cluster_image_ling": self.__cluster_img_link,
            "bad_company_segments": self.__bad_company_segments,
            "scatter_data": self.__scatter_data.to_json()
        }
