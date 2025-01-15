FROM python:3.10-slim

RUN pip install mlflow==2.12.1
RUN pip install boto3

EXPOSE 5000