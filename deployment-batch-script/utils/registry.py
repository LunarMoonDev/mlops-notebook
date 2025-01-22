import mlflow

def load_model(run_id):
    """Loads the model from model registery"""
    logged_model = f's3://mlflow-buckets/{run_id}/artifacts/model'
    model = mlflow.pyfunc.load_model(logged_model)
    return model