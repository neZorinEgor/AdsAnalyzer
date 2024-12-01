from fastapi import UploadFile
import pandas as pd
from sklearn.model_selection import RandomizedSearchCV


class RegressionUtils:
    @staticmethod
    def validate_dataset(dataframe: UploadFile):
        pass

    @staticmethod
    def to_foram_dataframe(dataset: UploadFile) -> pd.DataFrame:
        """
        Return pd.DataFrame by dataset-file extension.
        """
        dataset_extension = dataset.filename.split(".")[-1].lower()
        if dataset_extension in ["csv"]:
            return pd.read_csv(dataset.file)
        if dataset_extension in ["xlsx", "xlsm", "xlsb", "xltx", "xltm", "xls", "xlt", "xls", "xml", "xml", "xlam", "xla", "xlw", "xlr"]:
            return pd.read_excel(dataset.file)

    @staticmethod
    def search_best_param(x_train, y_train, algorithm) -> dict:
        """
        Search best input algorithm params.
        """
        grid_search = RandomizedSearchCV(
            cv=5,
            n_jobs=1,
            estimator=algorithm(random_state=0, verbosity=-1),
            param_distributions={
                "n_estimators": range(100, 1001, 100),
                "max_depth": range(3, 12, 1),
                "min_samples_split": range(10, 51, 10),
                "min_samples_leaf": range(10, 51, 10)
            }
        )
        grid_search.fit(x_train, y_train)
        return grid_search.best_params_
