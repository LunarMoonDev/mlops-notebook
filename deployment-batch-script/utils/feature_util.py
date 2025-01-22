import time
from pathlib import Path

import functools
from toolz import compose
import pandas as pd

from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import FunctionTransformer
from sklearn.feature_extraction import DictVectorizer

def data_dict(data_path: str) -> pd.DataFrame:
    data = pd.read_parquet(data_path, storage_options=dict(profile='localstack'))

    return {
        "data": data,
        "data_path": data_path
    }

def convert_to_dict(df):
    return df.to_dict(orient="records")

def preprocessor_with_transform(df, transform: tuple = ()):
    return compose(*transform[::-1])(df)

def feature_pipeline(transforms: tuple = ()):
    preprocessor = functools.partial(preprocessor_with_transform, transform=transforms)
    
    return make_pipeline(
        FunctionTransformer(preprocessor),
        FunctionTransformer(convert_to_dict),
        DictVectorizer(),
    )