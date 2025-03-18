### Requirements:
- ensure `AWS_PROFILE` env var exists (value: `localstack`)
- ensure `DEBUG` env var exists (value: `0`)

### Run the mlflow server with localstack via docker
```bash
docker compose up
```
- create bucket with the following command:
`aws s3 mb s3://mlflow-buckets`

### Run models
- make sure you are in pipenv shell inside this notebook
- run one of the models ex: `python -m model_linear`