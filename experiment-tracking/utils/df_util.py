import seaborn as sns
import matplotlib.pyplot as plt

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

def plot_duration_histograms(y_train, yp_train, y_valid, yp_valid):
    """Plot true and prediction distributions of ride duration."""

    # fmt: off
    fig, ax = plt.subplots(1, 2, figsize=(8, 4))
    pred_config = dict(label='pred', color='C0', stat='density', kde='True')
    true_config = dict(label='true', color='C1', stat='density', kde='True')
    
    ax[0].set_title("train")
    sns.histplot(yp_train, ax=ax[0], **pred_config)
    sns.histplot(y_train, ax=ax[0], **true_config)

    ax[1].set_title("valid")
    sns.histplot(yp_valid, ax=ax[1], **pred_config)
    sns.histplot(y_train, ax=ax[1], **true_config)

    ax[0].legend()
    ax[1].legend()
    fig.tight_layout()

    return fig