from utils.analytics.data import load_data

@data_source
def data(*args, **kwargs):
    return load_data()