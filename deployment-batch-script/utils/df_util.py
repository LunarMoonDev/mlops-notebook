import uuid
from config import config

def create_target_column(df):
    "Create target column"
    df[config.TARGET] = df.lpep_dropoff_datetime - df.lpep_pickup_datetime
    df[config.TARGET] = df[config.TARGET].dt.total_seconds() / 60
    return df

def filter_ride_duration(df):
    """Filter rides with target outliers"""
    mask = (df[config.TARGET] >= config.TARGET_MIN) & (df[config.TARGET] <= config.TARGET_MAX)
    return df[mask]

def generate_uuid(length: int):
    """Generate unique ids for each record"""
    ride_ids = []
    for i in range(length):
        ride_ids.append(str(uuid.uuid4()))
    
    return ride_ids