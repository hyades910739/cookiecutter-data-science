import os

import pandas as pd
from mlflow.client import MlflowClient
from mlflow.entities.experiment import Experiment


def setup_env(config: dict):
    assert config["MLFLOW_TRACKING_URI"] is not None
    os.environ["MLFLOW_TRACKING_URI"] = config["MLFLOW_TRACKING_URI"]
    os.environ["MLFLOW_TRACKING_USERNAME"] = config.get("MLFLOW_TRACKING_USERNAME", None)
    os.environ["MLFLOW_TRACKING_PASSWORD"] = config.get("MLFLOW_TRACKING_PASSWORD", None)


def get_or_create_experiment(exp_name) -> Experiment:
    client = MlflowClient()
    exp = client.get_experiment_by_name(exp_name)
    if not exp:
        client.create_experiment(exp_name)
        exp = client.get_experiment_by_name(exp_name)
    return exp
