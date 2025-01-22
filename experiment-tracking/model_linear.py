import os
import pickle

import mlflow
from sklearn.linear_model import LinearRegression

from utils.df_process import preprocess
from utils.feature_util import (
    data_dict,
    feature_pipeline,
    setup_experiment,
    mlflow_default_logging,
    make_model_pipeline
)

setup_experiment()
data = data_dict(debug=int(os.environ["DEBUG"]))
# mlflow.sklearn.autolog()

def run(build: bool = False):
    with mlflow.start_run():
        # Preprocessing
        X_train, y_train = preprocess(data["train_data"], target=True, filter_target=True)
        X_valid, y_valid = preprocess(data["valid_data"], target=True, filter_target=True)

        # Fit feature pipe
        feature_pipe = feature_pipeline()
        X_train = feature_pipe.fit_transform(X_train)
        X_valid = feature_pipe.transform(X_valid)

        # Fit model
        model = LinearRegression()
        model.fit(X_train, y_train)

        # MLflow logging
        MODEL_TAG = "linear"
        mlflow_default_logging(model, MODEL_TAG, data, X_train, y_train, X_valid, y_valid)


        main_pipeline = make_model_pipeline(feature_pipe, model)
        mlflow.sklearn.log_model(main_pipeline, 'model')

        if(build):
            with open(f"models/{MODEL_TAG}.bin", "wb") as f_out:
                pickle.dump((feature_pipe, model), f_out)
        

if __name__ == "__main__":
    import sys

    if(len(sys.argv) > 1 and sys.argv[1] == "build"):
        run(True)
    else:
        run(False)