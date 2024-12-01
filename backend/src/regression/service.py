from fastapi import UploadFile

import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from lightgbm import LGBMRegressor
from warnings import filterwarnings

from src.auth.dependency import AuthDependency
from src.auth.schemas import UserTokenPayloadSchema
from src.auth.service import celery
from src.regression.utils import RegressionUtils
from src.settings import settings

filterwarnings("ignore")


class RegressionService:
    @staticmethod
    @celery.task
    def create_regression_model(
            endpoint_path: str,
            label_name: str,
            dataset: UploadFile,
            algorithm=settings.ml.base_regression_algorithm
    ):
        # Dataset preprocessing
        data_frame = RegressionUtils.to_foram_dataframe(dataset)
        data_frame.dropna(inplace=True)
        data_frame = pd.get_dummies(data_frame)
        features_names = list(data_frame)
        data_frame = pd.DataFrame(StandardScaler().fit_transform(data_frame), columns=features_names)
        X = data_frame[[i for i in features_names if i != label_name]]
        y = data_frame[label_name]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
        # Search best params
        best_params = RegressionUtils.search_best_param(X_train, y_train, algorithm)
        algo = algorithm(**best_params)
        algo.fit(X_train, y_train)
        return algo.predict(X_test)
