from enum import Enum

from sklearn.ensemble import GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression


class ModelAlgorithm(str, Enum):
    LOGISTIC_REGRESSION = "logistic_regression"
    BOOST = "boost"


# Определяем зависимости моделей от значения enum
MODEL_MAP = {
    ModelAlgorithm.LOGISTIC_REGRESSION: LogisticRegression,
    ModelAlgorithm.BOOST: GradientBoostingClassifier,
}
