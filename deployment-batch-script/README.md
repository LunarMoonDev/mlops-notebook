## Requirements
- Model registery server is active or a s3 bucket is live with models uploaded by registry
- Bucket for input batch should exist with data
- Bucket for output batch should also exist

### To do these requirements:
1. Run `docker compose up` in `experiment-tracking` repository
    - This should run a `localstack` and a `mlflow` server
2. Create s3 buckets with `aws s3api create-bucket` command
    - `aws s3api create-bucket --bucket mlops-buckets`
    - `aws s3api create-bucket --bucket nyc-tlc`
    - `aws s3api create-bucket --bucket nyc-duration-prediction`
3. Run `model_linear` from `experiment-tracking` to save a model we can use
    - Ensure that the `Pipenv` is active
4. Copy a parquet file to `nyc-tlc` bucket
    - use command `aws s3 cp ./green_tripdata_2022-02.parquet s3://nyc-tlc/trip-data/`
    - you can download the parquet file from nyc trip data site


For step 3, ensure these environment variables are present
```bash
    export AWS_PROFILE=localstack
    export DEBUG=0
```

## Running the Batch Job
- Go to `deployment-batch-script` and activate `Pipenv` <- first step
- Run Prefect server using `prefect server start`
- In another terminal, repeat the first step
- Run either `test_batch` or `test_score`
    - To run `test_score`, note that it requires parameters on run
    - To run `test_batch`, note that it creates a scheduled job for every 10 minutes

For last step, ensure these environment variables are present
```bash
    export AWS_PROFILE=localstack
    export PREFECT_API_URL=http://127.0.0.1:4200/api
```
