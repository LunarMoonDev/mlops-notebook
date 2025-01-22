from pathlib import Path

from pydantic import BaseModel
from strictyaml import load

# Project directories
PACKAGE_ROOT = Path(__file__).resolve().parents[1]
ROOT = PACKAGE_ROOT.parent
CONFIG_FILE_PATH = PACKAGE_ROOT / "properties" / "config.yaml"

# Load core config object
class Config(BaseModel):
    RANDOM_STATE: int
    TARGET_MIN: int
    TARGET_MAX: int
    TARGET: str
    RECORD_ID: str
    FEATURES: list[str]
    NUM_FEATURES: list[str]
    CAT_FEATURES: list[str]

with open(CONFIG_FILE_PATH, "r") as f:
    config_file = f.read()

config = Config(**load(config_file).data)