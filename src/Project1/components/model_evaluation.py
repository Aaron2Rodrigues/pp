import os
import pandas as pd
import mlflow
import mlflow.sklearn
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from urllib.parse import urlparse
import numpy as np 
import joblib
from src.Project1.utils.common import  save_json
from pathlib import Path
from src.Project1.entity.entity_config import ModelEvaluationconfig
import os 
os.environ["MLFLOW_TRACKING_URI"] = "https://dagshub.com/chrisaaronrodrigues/Project1.mlflow"
os.environ["MLFLOW_TRACKING_USERNAME"] = "chrisaaronrodrigues"
os.environ["MLFLOW_TRACKING_PASSWORD"] = "4e63aec22cb3ab3730e936a0b62c1e93dc8c3229"


class ModelEvaluation:
    def __init__(self, config: ModelEvaluationconfig):
        self.config = config

    def eval_metrics(self, actual, pred):
        rmse = np.sqrt(mean_squared_error(actual, pred))
        r2 = r2_score(actual, pred)
        mae = mean_absolute_error(actual, pred)
        return rmse, r2, mae
    
    def log_into_mlflow(self):

        test_data = pd.read_csv(self.config.test_data_path)
        model = joblib.load(self.config.model_path)

        test_X = test_data.drop(self.config.target_column, axis=1)
        test_y = test_data[self.config.target_column]

        mlflow.set_registry_uri(self.config.mlflow_uri)
        tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme

        with mlflow.start_run():

            predicted_qualities = model.predict(test_X)
            (rmse, r2, mae) = self.eval_metrics(test_y, predicted_qualities)
            
            scores = {"rmse": rmse, "r2": r2, "mae": mae}
            save_json(path =Path(self.config.metric_file_name), data = scores)

            mlflow.log_params(self.config.all_params)

            mlflow.log_metric("rmse", rmse)
            mlflow.log_metric("r2", r2)
            mlflow.log_metric("mae", mae)
  
            if tracking_url_type_store != "file":
                mlflow.sklearn.log_model(model, "model", registered_model_name = "ElasticNet")
            else:
                mlflow.sklearn.log_model(model, "model")
   