import os

import mlflow
from sklearn.ensemble import (
    ExtraTreesRegressor,
    RandomForestRegressor,
    GradientBoostingRegressor,
)

from utils.df_process import preprocess
from utils.feature_util import (
    data_dict,
    feature_pipeline,
    setup_experiment,
    mlflow_default_logging,
)

setup_experiment()
mlflow.sklearn.autolog()
data = data_dict(debug=int(os.environ["DEBUG"]))

def run(model_class):
    with mlflow.start_run():
        # Preprocessing
        train = data["train_data"]
        valid = data["valid_data"]
        X_train, y_train = preprocess(train, target=True, filter_target=True)
        X_valid, y_valid = preprocess(valid, target=True, filter_target=True)

        # Fit feature pipe
        feature_pipe = feature_pipeline()
        X_train = feature_pipe.fit_transform(X_train)
        X_valid = feature_pipe.transform(X_valid)

        # Fit model
        model = model_class(verbose=1)
        model.fit(X_train, y_train)

        # MLFLow logging (default + feature pipe)
        MODEL_TAG = model_class.__name__
        args = [model, MODEL_TAG, data, X_train, y_train, X_valid, y_valid]
        mlflow_default_logging(*args)
        mlflow.sklearn.log_model(feature_pipe, "feature_pipe")

if __name__ == "__main__":
    for model_class in [
        ExtraTreesRegressor,
        GradientBoostingRegressor,
        RandomForestRegressor,
    ]:
        run(model_class)