from fastapi import UploadFile

import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, GridSearchCV, RandomizedSearchCV
from lightgbm import LGBMRegressor

from src.auth.dependency import AuthDependency
from src.auth.schemas import UserTokenPayloadSchema
from src.auth.service import celery


class RegressionService:
    def __init__(self):
        pass

    @staticmethod
    @celery.task
    def create_regression_model(
            endpoint_path: str,
            label_name: str,
            dataset: UploadFile,
    ):
        # Dataset preprocessing
        data_frame = pd.read_csv(dataset.file)
        data_frame.dropna(inplace=True)
        data_frame = pd.get_dummies(data_frame)
        features_names = list(data_frame)
        data_frame = pd.DataFrame(StandardScaler().fit_transform(data_frame), columns=features_names)
        X = data_frame[[i for i in features_names if i != label_name]]
        y = data_frame[label_name]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
        # Search best params
        grid_search = RandomizedSearchCV(
            cv=5,
            n_jobs=1,
            estimator=LGBMRegressor(random_state=0, verbosity=-1),
            param_distributions={
                "n_estimators": range(100, 1001, 100),
                "max_depth": range(3, 12, 1),
                "min_samples_split": range(10, 51, 10),
                "min_samples_leaf": range(10, 51, 10)
            }
        )
        grid_search.fit(X_train, y_train)
        return grid_search.best_params_