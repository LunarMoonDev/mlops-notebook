FROM python:3.9.21-slim

ENV PATH="/root/.cargo/bin:$PATH"

RUN pip install -U pip
RUN pip install pipenv

WORKDIR /app

COPY Pipfile ./
COPY Pipfile.lock ./

RUN pipenv install --system --deploy

COPY model_linear.py ./
COPY model_linear_pudo.py ./
COPY model_trees.py ./
COPY model_xgboost_optuna.py ./

COPY config/ ./config/
COPY data/ ./data/
COPY models/ ./models/
COPY properties/ ./properties/
COPY utils/ ./utils/