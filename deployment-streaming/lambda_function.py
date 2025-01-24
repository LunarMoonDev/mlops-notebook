import os
import json
import boto3
import base64

import pandas as pd
import mlflow

PREDICTIONS_STREAM_NAME = os.getenv('PREDICTIONS_STREAM_NAME', 'ride_predictions')
RUN_ID = os.getenv('RUN_ID')
TEST_RUN = os.getenv('TEST_RUN', 'False') == 'True'

kinesis_client = boto3.client('kinesis')
logged_model = f's3://mlflow-buckets/{RUN_ID}/artifacts/model'
model = mlflow.pyfunc.load_model(logged_model)

def prepare_features(ride):
    features = {}
    features['trip_distance'] = ride['trip_distance']
    features['PULocationID'] = ride['PULocationID']
    features['DOLocationID'] = ride['DOLocationID']

    return pd.DataFrame([features])

def predict(features):
    pred = model.predict(features)
    return float(pred[0])

def lambda_handler(event, context):
    prediction_events = []

    for record in event['Records']:
        encoded_data = record['kinesis']['data']
        decoded_data = base64.b64decode(encoded_data).decode('utf-8')
        ride_event = json.loads(decoded_data)

        ride = ride_event['ride']
        ride_id = ride_event['ride_id']

        features = prepare_features(ride)
        prediction = predict(features)

        prediction_event = {
            'model': 'ride_duration_prediction_model',
            'run_id': RUN_ID,
            'prediction': {
                'ride_duration': prediction,
                'ride_id': ride_id
            }
        }

        if not TEST_RUN:
            kinesis_client.put_record(
                StreamName=PREDICTIONS_STREAM_NAME,
                Data=json.dumps(prediction_event),
                PartitionKey=str(ride_id)
            )

        prediction_events.append(prediction_event)

    return {
        'predictions': prediction_events
    }