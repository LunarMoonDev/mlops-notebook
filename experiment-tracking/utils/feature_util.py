import time
from pathlib import Path

import mlflow
import pandas as pd
import functools
from toolz import compose

from sklearn.metrics import mean_squared_error
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import FunctionTransformer
from sklearn.feature_extraction import DictVectorizer
from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator

from utils.df_util import plot_duration_histograms
from config import config

ROOT_DIR = Path(__file__).parents[1]
DATA_DIR = ROOT_DIR / "data"
EXPERIMENT_NAME = "nyc-green-taxi-v2"
ARTIFACT_URI = "s3://mlflow-buckets"
TRACKING_URI = "http://localhost:5000"

def setup_experiment():
    mlflow.set_tracking_uri(TRACKING_URI)

    try:
        experiment = mlflow.get_experiment_by_name(EXPERIMENT_NAME)
        experiment_id = experiment.experiment_id
    except AttributeError:
        experiment_id = mlflow.create_experiment(EXPERIMENT_NAME, ARTIFACT_URI)

    mlflow.set_experiment(EXPERIMENT_NAME)

def data_dict(debug=False):
    train_data_path = DATA_DIR / "green_tripdata_2021-01.parquet"
    valid_data_path = DATA_DIR / "green_tripdata_2021-02.parquet"
    train_data = pd.read_parquet(train_data_path)
    valid_data = pd.read_parquet(valid_data_path)

    return {
        "train_data": train_data if not debug else train_data[:100],
        "valid_data": valid_data if not debug else valid_data[:100],
        "train_data_path": train_data_path,
        "valid_data_path": valid_data_path,
    }

def add_pudo_column(df):
    df["PU_DO"] = df["PULocationID"] + "_" + df["DOLocationID"]
    return df

def feature_selector(df):
    if "PU_DO" in df.columns:
        df = df[["PU_DO"] + config.NUM_FEATURES]
    return df

def convert_to_dict(df):
    return df.to_dict(orient="records")

def preprocessor_with_transform(df, transform: tuple = ()):
    return compose(*transform[::-1])(df)

def feature_pipeline(transforms: tuple = ()):
    preprocessor = functools.partial(preprocessor_with_transform, transform=transforms)
    
    return make_pipeline(
        FunctionTransformer(preprocessor),
        FunctionTransformer(convert_to_dict),
        DictVectorizer(),
    )

def make_model_pipeline(pipeline: Pipeline, model: BaseEstimator) -> Pipeline:
    return make_pipeline(pipeline, model)

def mlflow_default_logging(model, model_tag, data, X_train, y_train, X_valid, y_valid):
    # Predict time
    start_time = time.time()
    yp_train = model.predict(X_train)
    yp_valid = model.predict(X_valid)
    elapsed = time.time() - start_time
    N = len(yp_train) + len(yp_valid)
    predict_time = elapsed / N

    # Metrics
    rmse_train = mean_squared_error(y_train, yp_train, squared=False)
    rmse_valid = mean_squared_error(y_valid, yp_valid, squared=False)

    # Plot
    fig = plot_duration_histograms(y_train, yp_train, y_valid, yp_valid)

    # MLFlow logging
    mlflow.set_tag("model", model_tag)

    mlflow.log_param("train_data_path", data["train_data_path"])
    mlflow.log_param("valid_data_path", data["valid_data_path"])

    mlflow.log_metric("rmse_train", rmse_train)
    mlflow.log_metric("rmse_valid", rmse_valid)
    mlflow.log_metric("predict_time", predict_time)

    mlflow.log_figure(fig, "plot.svg")

    return {"rmse_train": rmse_train, "rmse_valid": rmse_valid}