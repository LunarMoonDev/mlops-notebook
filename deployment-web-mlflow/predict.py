import pickle
import pandas as pd

import mlflow

from flask import Flask, request, jsonify


# external variables
EXPERIMENT_NAME = "nyc-green-taxi-v2"
ARTIFACT_URI = "s3://mlflow-buckets"
TRACKING_URI = "http://localhost:5000"
RUN_ID = '981be9a447314f579079507e32328d57'

logged_model = f'runs:/{RUN_ID}/linear_pipeline'
mlflow.set_tracking_uri(TRACKING_URI)
mlflow.set_experiment(EXPERIMENT_NAME)

model = mlflow.pyfunc.load_model(logged_model)

def predict(ride):
    # turn it into df first
    ride_df = pd.DataFrame(ride)
    preds = model.predict(ride_df)
    return preds

app = Flask('duration-prediction')

@app.route('/predict', methods=['POST'])
def predict_endpoint():
    ride = request.get_json()
    pred = predict(ride)

    return jsonify({'duration': float(pred[0])})

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9696)