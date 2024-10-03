import datetime
from typing import List

import joblib
import pandas as pd
from fastapi import UploadFile, FastAPI
from pydantic import create_model

from src.ml.mapped import ModelAlgorithm, MODEL_MAP


def create_clf_handler(
        endpoint_path: str,          # Путь до обработчика пользователя
        algorithm: ModelAlgorithm,   # Алгоритм машинного обучения
        dataset: UploadFile,         # Данные, на которых обучается алгоритм
        label_name: str,             # Имя целевой переменной в dataset,
        app: FastAPI                 # Экземпляр сервера
):
    # print(dataset.file.closed)
    # Обработка данных
    df = pd.read_csv(dataset.file)
    df.dropna(inplace=True)
    feature_names = list(df.drop(columns=label_name))
    schema = create_model('schema', **{name: (float, ...) for name in feature_names})

    # Создание алгоритма и его обучение
    model = MODEL_MAP[algorithm](max_iter=1000)
    model.fit(pd.get_dummies(df[feature_names]), df[label_name])
    model_in_file = f"src/weights/{datetime.datetime.now(datetime.UTC)}.sav"
    joblib.dump(model, model_in_file)

    # Обработчик, который будет создан клиентом
    def classification_endpoint(data: List[schema]):
        input_df = pd.DataFrame(data)
        input_df_encoded = pd.get_dummies(input_df, drop_first=True)
        input_df_encoded = input_df_encoded.reindex(columns=model.feature_names_in_, fill_value=0)
        return [
            {
                "predict_class": int(predict),
                "probability": max(probability)
            } for predict, probability in zip(model.predict(input_df_encoded), joblib.load(model_in_file).predict_proba(input_df_encoded))]
    app.add_api_route(path=f"/{endpoint_path}", endpoint=classification_endpoint, methods=["POST"], tags=["ML-Routers"])
    app.openapi_schema = None
