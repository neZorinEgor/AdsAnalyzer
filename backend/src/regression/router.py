from fastapi import APIRouter, UploadFile, File, Depends, status

from src.auth.dependency import AuthDependency
from src.auth.schemas import UserTokenPayloadSchema
from src.regression.schemas import MessageResponse
from src.regression.service import RegressionService
from src.regression.utils import RegressionUtils

router = APIRouter(prefix="/ml/regression", tags=["Regression"])


@router.post(path="/create", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
def create_regression_model(
        endpoint_path: str,
        label_name: str,
        dataset: UploadFile = File(...),
        # user_credentials: UserTokenPayloadSchema = Depends(AuthDependency.get_current_user)
):
    """
    Automatically validate the dataset and initiate the training algorithm in the background.

    :param endpoint_path: The endpoint path where the trained model will be available.
    :param label_name: The name of the target variable to predict.
    :param dataset: The dataset file for training the regression model.
    :return: A response message indicating that the algorithm is being trained.
    :rtype: MessageResponse
    :raises ValueError: If the dataset fails validation.
    """
    RegressionUtils.validate_dataset(dataset)
    result = RegressionService.create_regression_model(endpoint_path, label_name, dataset)
    print(result)
    return MessageResponse(
        status=201,
        message="Algorithm is being trained in the background."
    )
