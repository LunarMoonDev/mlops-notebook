### Requirements:
- ensure `AWS_PROFILE` env var exists
- ensure `DEBUG` env var exists

### Run the mlflow server with localstack via docker
```bash
docker compose up
```

### Run models
- make sure you are in pipenv shell inside this notebook
- run one of the models ex: `python -m model_linear`