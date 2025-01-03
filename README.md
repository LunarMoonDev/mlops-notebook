# mlops-notebook
This repository will contain experiments, notes, and source codes of practices and lessons I learned from MLOps bootcamp. It's targeted to practices that I find good and best for MLOps.


## Running MLflow

```bash
mlflow server -h 127.0.0.1 -p 5001 --backend-store-uri=sqlite:///mlflow.db --default-artifact-root=./artifacts
```

To run each model scripts. Simply run them via terminal with python under venv!


## Runnine MageAI

```bash
docker compose up
```

mage-ai will get exposed to port 6789 and it will get binded to localhost!
