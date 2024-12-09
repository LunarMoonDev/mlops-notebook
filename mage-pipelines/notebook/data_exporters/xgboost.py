from typing import Dict, Tuple, Union

from pandas import Series
from scipy.sparse._csr import csr_matrix
from xgboost import Booster
from sklearn.base import BaseEstimator

from utils.models.xgboost import build_data, fit_model

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_decorator

@data_exporter
def train(
    training_set: Dict[str, Union[Series, csr_matrix]],
    settings: Tuple[
        Dict[str, Union[bool, float, int, str]],
        csr_matrix,
        Series,
    ],
    **kwargs,
) -> Tuple[Booster, BaseEstimator]:
    hyperparameters, X, y = settings

    # for debugging purposes
    if kwargs.get('max_depth'):
        hyperparameters['max_depth'] = int(kwargs.get('max_depth'))

    model = fit_model(
        build_data(X, y),
        hyperparameters,
        verbose_eval=kwargs.get('verbose_eval', 100)
    )

    vectorizer = training_set['build'][6]
    return model, vectorizer