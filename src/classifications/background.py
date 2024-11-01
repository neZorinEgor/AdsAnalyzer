import datetime
from typing import List

import joblib
import pandas as pd
from fastapi import UploadFile, FastAPI
from pydantic import create_model

from src.classifications.mapped import ModelAlgorithm, MODEL_MAP
from src.classifications.model import ClassificationHandlersModel


async def create_clf_handler(
        endpoint_path: str,  # Path to the auth handler
        algorithm: ModelAlgorithm,  # Machine learning algorithm
        dataset: UploadFile,  # Dataset for training the algorithm
        label_name: str,  # Target variable name in the dataset
        app: FastAPI,  # Server instance
        session  # Database session or other session object
):
    # Dataset preprocessing
    df = pd.read_csv(dataset.file)
    df.dropna(inplace=True)
    feature_names = list(df.drop(columns=label_name))
    schema = create_model('schema', **{name: (float, ...) for name in feature_names})
    # Create and supervised algorithm
    model = MODEL_MAP[algorithm](max_iter=1000)
    model.fit(pd.get_dummies(df[feature_names]), df[label_name])
    model_in_file = f"src/weights/{datetime.datetime.now(datetime.UTC)}.sav"
    joblib.dump(model, model_in_file)
    # Save algorithm
    clf_handler = ClassificationHandlersModel()
    clf_handler.endpoint_path = endpoint_path
    clf_handler.model_path = model_in_file
    clf_handler.created_at = datetime.datetime.now(datetime.UTC)
    session.add(clf_handler)
    await session.commit()

    # Create model handler
    async def classification_endpoint(data: List[schema]):
        input_df = pd.DataFrame(data)
        input_df_encoded = pd.get_dummies(input_df, drop_first=True)
        input_df_encoded = input_df_encoded.reindex(columns=model.feature_names_in_, fill_value=0)
        return [
            {
                "predict_class": int(predict),
                "probability": max(probability)
            } for predict, probability in
            zip(model.predict(input_df_encoded), joblib.load(model_in_file).predict_proba(input_df_encoded))]

    app.add_api_route(path=f"/{endpoint_path}", endpoint=classification_endpoint, methods=["POST"], tags=["ML-Routers"])
    app.openapi_schema = None
