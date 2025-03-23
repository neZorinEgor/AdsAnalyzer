import datetime
import time
from typing import Type
from warnings import filterwarnings

import shap
import requests
import matplotlib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from lightgbm import LGBMClassifier
from imblearn.under_sampling import RandomUnderSampler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.metrics import classification_report

from src.analysis.core import IAnalysisRepository, IFileStorage
from src.analysis.schemas import Message
from src.config import settings

matplotlib.use("agg")
filterwarnings("ignore")


class AnalysisService:
    __wcss: dict = {}                  # Сумма внутрикластерных расстояний
    __percentage_error_diff = {}       # Процентные изменения WCSS
    __optimality_threshold: int = 20   # Порог разници процентного прироста для определения оптимального колличества кластеров
    __optimal_num_cluster: int = 3     # Оптимальное количество кластеров
    __efficiency_columns: list = ["Показы", "Взвешенные показы", "Клики", "CTR (%)", "wCTR (%)", "Расход (руб.)", "Ср. цена клика (руб.)", "Ср. ставка за клик (руб.)", "Отказы (%)", "Глубина (стр.)", "Прибыль (руб.)",]
    __cluster_img: np.ndarray
    __wcss_img: np.ndarray

    # Dependency Inversion & Injection
    def __init__(
            self,
            repository: Type[IAnalysisRepository],
            filestorage: Type[IFileStorage]
    ):
        self.__repository = repository()
        self.__filestorage = filestorage()

    def __preprocessing_company_dataframe(self, company_df: pd.DataFrame) -> pd.DataFrame:
        company_df.replace({',': '.'}, regex=True, inplace=True)
        company_df.replace({'--': -1}, regex=False, inplace=True)
        ignored_cols = ["№ Группы"]
        for col in company_df.columns:
            try:
                if col in ignored_cols:
                    continue
                isinstance(float(company_df[col][0]), float)
                company_df[col] = company_df[col].astype("float64")
            except ValueError:
                continue
        return company_df

    async def __download_report_from_yandex(self, report_id: int, token: str, report_name: str) -> pd.DataFrame | None:
        headers = {
            'Authorization': f'Bearer {token}',
            'Accept-Language': f'en',
            'processingMode': "offline",
            'returnMoneyInMicros': "true",
            'skipReportSummary': "true",
            'skipReportHeader': "true",
            'skipColumnHeader': "true",
        }
        payload = {
            "params": {
                "SelectionCriteria": {
                    "Filter": [{
                        "Field": "CampaignId",
                        "Operator": "EQUALS",
                        "Values": [f"{report_id}"]
                    }],
                    "DateFrom": "2023-09-22",
                    "DateTo": "2025-03-06",
                },
                "FieldNames": [
                    "Date",  # Дата
                    "AdGroupName",  # Группа
                    "AdGroupId",  # № Группы
                    "AdId",  # № Объявления
                    "AdNetworkType",  # Тип площадки
                    "TargetingLocationName",  # Регион таргетинга
                    "LocationOfPresenceName",  # Регион местонахождения
                    "Gender",  # Пол
                    "IncomeGrade",  # Уровень платежеспособности
                    "Age",  # Возраст
                    "MobilePlatform",  # Версия ОС устройства
                    "Impressions",  # Показы
                    "WeightedImpressions",  # Взвешенные показы
                    "Clicks",  # Клики
                    "Ctr",  # CTR (%)
                    "WeightedCtr",  # wCTR (%)
                    "Cost",  # Расход (руб.)
                    "AvgCpc",  # Ср. цена клика (руб.)
                    "AvgEffectiveBid",  # Ср. ставка за клик (руб.)
                    "BounceRate",  # Отказы (%)
                    "AvgPageviews",  # Глубина (стр.)
                    "GoalsRoi",  # Рентабельность
                    "Profit"  # Прибыль (руб.)
                ],
                "ReportName": f"{report_name}",
                "ReportType": "AD_PERFORMANCE_REPORT",
                "DateRangeType": "CUSTOM_DATE",
                "Format": "TSV",
                "IncludeVAT": "YES",
            }
        }
        response = requests.post(url=settings.REPORT_SERVICE_URL, headers=headers, json=payload)
        if response.status_code == 200:
            lines = response.text.rstrip().split("\n")
            data_dict = {
                "Дата": [],  # Date
                "Группа": [],  # AdGroupName
                "№ Группы": [],  # AdGroupId
                "№ Объявления": [],  # AdId
                "Тип площадки": [],  # AdNetworkType
                "Регион таргетинга": [],  # TargetingLocationName
                "Регион местонахождения": [],  # LocationOfPresenceName
                "Пол": [],  # Gender
                "Уровень платежеспособности": [],  # IncomeGrade
                "Возраст": [],  # Age
                "Версия ОС устройства": [],  # MobilePlatform
                "Показы": [],  # Impressions
                "Взвешенные показы": [],  # WeightedImpressions
                "Клики": [],  # Clicks
                "CTR (%)": [],  # Ctr
                "wCTR (%)": [],  # WeightedCtr
                "Расход (руб.)": [],  # Cost
                "Ср. цена клика (руб.)": [],  # AvgCpc
                "Ср. ставка за клик (руб.)": [],  # AvgEffectiveBid
                "Отказы (%)": [],  # BounceRate
                "Глубина (стр.)": [],  # AvgPageviews
                "Рентабельность": [],  # GoalsRoi
                "Прибыль (руб.)": []  # Profit
            }
            # Заполняем словарь данными из ответа
            for line in lines:
                values = line.split("\t")  # Разделяем по табуляции
                data_dict["Дата"].append(values[0])
                data_dict["Группа"].append(values[1])
                data_dict["№ Группы"].append(values[2])
                data_dict["№ Объявления"].append(values[3])
                data_dict["Тип площадки"].append(values[4])
                data_dict["Регион таргетинга"].append(values[5])
                data_dict["Регион местонахождения"].append(values[6])
                data_dict["Пол"].append(values[7])
                data_dict["Уровень платежеспособности"].append(values[8])
                data_dict["Возраст"].append(values[9])
                data_dict["Версия ОС устройства"].append(values[10])
                data_dict["Показы"].append(values[11])
                data_dict["Взвешенные показы"].append(values[12])
                data_dict["Клики"].append(values[13])
                data_dict["CTR (%)"].append(values[14])
                data_dict["wCTR (%)"].append(values[15])
                data_dict["Расход (руб.)"].append(values[16])
                data_dict["Ср. цена клика (руб.)"].append(values[17])
                data_dict["Ср. ставка за клик (руб.)"].append(values[18])
                data_dict["Отказы (%)"].append(values[19])
                data_dict["Глубина (стр.)"].append(values[20])
                data_dict["Рентабельность"].append(values[21])
                data_dict["Прибыль (руб.)"].append(values[22])
            return pd.DataFrame(data_dict)[["Показы", "Взвешенные показы", "Клики", "CTR (%)", "wCTR (%)", "Расход (руб.)", "Ср. цена клика (руб.)", "Ср. ставка за клик (руб.)", "Отказы (%)", "Глубина (стр.)", "Прибыль (руб.)"]]
        elif response.status_code == 202 or response.status_code == 201:
            time.sleep(5)
            print("рекурсия")
            return await self.__download_report_from_yandex(report_id=report_id, token=token, report_name=report_name)
        else:
            print(response.text)
            return None

    def __cluster_advertising_company(self, company_df: pd.DataFrame):
        print("start clustering")
        if "cluster_id" in self.__efficiency_columns:
            self.__efficiency_columns.remove("cluster_id")

        X = pd.get_dummies(company_df[self.__efficiency_columns])
        times = {}

        for i in range(1, 11):
            kmeans = KMeans(n_clusters=i, max_iter=100, init="k-means++", random_state=42)
            start_time = time.time()
            self.__wcss[i] = kmeans.fit(X).inertia_
            times[i] = time.time() - start_time

        plt.figure(figsize=(10, 6))
        plt.title("Выбор оптимального количества кластеров методом локтя")
        # Ось WCSS
        ax1 = plt.gca()
        ax1.set_xlabel("Количество кластеров")
        ax1.set_ylabel("WCSS", color="blue")
        ax1.plot(self.__wcss.keys(), self.__wcss.values(), marker='o', label="WCSS", color="blue")
        ax1.tick_params(axis='y', labelcolor="blue")
        # Ось времени выполнения
        ax2 = ax1.twinx()
        ax2.set_ylabel("Время обучения (сек)")
        ax2.plot(times.keys(), times.values(), marker='s', linestyle='dashed', color="red", label="Время обучения")
        ax2.tick_params(axis='y', labelcolor="red")
        plt.xticks(range(1, 11))
        plt.axvline(self.__optimal_num_cluster, color="indianred", linestyle="--", label="Оптимальный кластер")
        fig = plt.gcf()
        fig.canvas.draw()
        self.__wcss_img = np.array(fig.canvas.renderer.buffer_rgba())
        plt.close()
        for item in range(len(self.__percentage_error_diff)-1):
            proc_diff = list(self.__percentage_error_diff.items())[item][1]-list(self.__percentage_error_diff.items())[item+1][1]
            if proc_diff>self.__optimality_threshold:
                self.__optimal_num_cluster=int(list(self.__percentage_error_diff.items())[item][0][-1])
                break
            else:
                self.__optimal_num_cluster=3
        # Постройка кластеров
        pca = PCA(n_components=2)
        pca_df = pca.fit_transform(StandardScaler().fit_transform(company_df[self.__efficiency_columns]))
        pca_df = pd.DataFrame(pca_df)
        kmeans = KMeans(n_clusters=self.__optimal_num_cluster, max_iter=1000, init="k-means++", random_state=42)
        predict = kmeans.fit_predict(pca_df)
        self.__efficiency_columns.append("cluster_id")
        company_df["cluster_id"]=predict
        # Визуализация кластров
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
        fig = plt.gcf()
        fig.canvas.draw()
        self.__cluster_img = np.array(plt.gcf().canvas.renderer.buffer_rgba())
        plt.close()
        return company_df[self.__efficiency_columns].copy()

    def __interpret_clusters(self, clustered_df: pd.DataFrame) -> None:
        print("Light gradient boost start kill my intel...")
        sampler = RandomUnderSampler()
        X_resample, y_resample = sampler.fit_resample(
            X=pd.get_dummies(clustered_df[self.__efficiency_columns]),
            y=clustered_df["cluster_id"],
        )
        X_train, X_test, y_train, y_test = train_test_split(X_resample, y_resample)
        grid = GridSearchCV(
            estimator=LGBMClassifier(random_state=42),
            param_grid={
                "random_state": [42],
                "verbose": [-1],
                "n_jobs": [3],
                "n_estimators": range(100, 501, 100),
                "max_depth": range(1, 6, 1),
                "min_samples_split": range(10, 51, 10),
                "min_samples_leaf": range(10, 51, 10),
            },
            cv=5,
            n_jobs=-1,
        )
        grid.fit(X_train, y_train)
        estimator = LGBMClassifier(**grid.best_params_)
        estimator.fit(X_train, y_train)
        y_pred = estimator.predict(X_test)
        print(classification_report(y_pred=y_pred, y_true=y_test))
        explainer = shap.TreeExplainer(estimator)
        shap_values = explainer.shap_values(X_test)

    async def kill_cpu_and_gpu_by_ml(self, message: Message) -> None:
        """
        Automatically analysis ads-company.

        :param message: message from kafka with user token and uuid
        :return: `None`
        """
        company_df = await self.__download_report_from_yandex(
            report_id=message.report_id,
            token=message.yandex_id_token,
            report_name=message.report_name   # f"{datetime.datetime.now(datetime.UTC)}"
        )
        if company_df is None:
            # If the report cannot be generated online, an error is returned.
            await self.__repository.update_company_report_info(report_id=message.report_id, info="Error: report cannot be generated online.")
            print("ошибка")
            return
        company_df = self.__preprocessing_company_dataframe(company_df=company_df)
        company_df = self.__cluster_advertising_company(company_df=company_df)
        self.__interpret_clusters(clustered_df=company_df)   # by-by, cpu
