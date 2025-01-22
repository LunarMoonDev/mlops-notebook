import pandas as pd

from datetime import datetime
from dateutil.relativedelta import relativedelta

from prefect import task, flow

from utils.registry import load_model
from utils.df_process import preprocess
from utils.feature_util import data_dict

def save_results(df, y_pred, run_id, output_file):
    """Creates a output dataframe accustomed according to downstream"""
    df_result = pd.DataFrame()
    df_result['ride_id'] = df['ride_id']
    df_result['lpep_pickup_datetime'] = df['lpep_pickup_datetime']
    df_result['PULocationID'] = df['PULocationID']
    df_result['DOLocationID'] = df['DOLocationID']
    df_result['actual_duration'] = df['duration']
    df_result['predicted_duration'] = y_pred
    df_result['diff'] = df_result['actual_duration'] - df_result['predicted_duration']
    df_result['model_version'] = run_id

    df_result.to_parquet(output_file, index=False, storage_options=dict(profile='localstack'))

@task
def apply_model(input_file, run_id, output_file):
    # reads the input parquet as dataframe
    input_dict = data_dict(input_file)
    # preprocesses the raw data to features and targets
    dicts, _, data = preprocess(input_dict['data'], target=True, filter_target=True)
    # loads the model from s3 bucket with the given run_id
    model = load_model(run_id)
    # predicts with the model pipeline. feature selection is included in pipeline
    y_pred = model.predict(dicts)
    # saves the datafram as parquet to output destination
    save_results(data, y_pred, run_id, output_file)
    # returns where it's saved
    return output_file

def get_paths(run_date, taxi_type, run_id):
    prev_month = run_date - relativedelta(months=1)
    year = prev_month.year
    month = prev_month.month 

    input_file = f's3://nyc-tlc/trip-data/{taxi_type}_tripdata_{year:04d}-{month:02d}.parquet'
    output_file = f's3://nyc-duration-prediction/{taxi_type}/{year:04d}/{month:02d}/{run_id}.parquet'

    return input_file, output_file

@flow
def ride_duration_prediction(
        taxi_type: str,
        run_id: str,
        run_date: datetime = None):
    input_file, output_file = get_paths(run_date, taxi_type, run_id)

    apply_model(
        input_file=input_file,
        run_id=run_id,
        output_file=output_file
    )

@flow
def test_ride_duration_prediction():
    taxi_type = 'green'
    run_id = '4c86306c61d94c48966e3dd8ed7c57cd'
    run_date = datetime(year=2022, month=2, day=1)

    input_file, output_file = get_paths(run_date, taxi_type, run_id)

    apply_model(
        input_file=input_file,
        run_id=run_id,
        output_file=output_file
    )
