import os
import sys

from networksecurity.exception.exception import NetworkSecurityException 
from networksecurity.logging.logger import logging

from networksecurity.entity.artifact_entity import DataTransformationArtifact,ModelTrainerArtifact
from networksecurity.entity.config_entity import ModelTrainerConfig


from networksecurity.utils.ml_utils.model.estimator import NetworkModel
from networksecurity.utils.main_utils.utils import save_object,load_object
from networksecurity.utils.main_utils.utils import load_numpy_array_data,evaluate_models
from networksecurity.utils.ml_utils.metric.classification_metric import get_classification_score


from sklearn.linear_model import LogisticRegression
from sklearn.metrics import r2_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    AdaBoostClassifier,
    GradientBoostingClassifier,
    RandomForestClassifier,
)

import mlflow 
import dagshub

# Get the DagsHub access token from the .env/environment variables
DAGSHUB_TOKEN = os.getenv("DAGSHUB_TOKEN")

if dagshub_token is None:
    raise ValueError("DAGSHUB_TOKEN is not set in the environment.")

# Connect this project to the DagsHub repository nd enable remote MLflow experiment tracking
dagshub.init(repo_owner='nahid-rgb', repo_name='networksecurity-mlops', mlflow=True, token = DAGSHUB_TOKEN)


class ModelTrainer:
 
    def __init__(self, model_trainer_config:ModelTrainerConfig,
                 data_transformation_artifact:DataTransformationArtifact):

        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact

        except Exception as e:
            raise NetworkSecurityException(e,sys)


    def track_mlflow(self, best_model, classificationmetric, run_name):

        with mlflow.start_run(run_name=run_name):
            f1_score = classificationmetric.f1_score
            precision_score = classificationmetric.precision_score
            recall_score = classificationmetric.recall_score


            mlflow.log_metric("f1_score",f1_score)
            mlflow.log_metric("precision",precision_score)
            mlflow.log_metric("recall_score",recall_score)
            mlflow.sklearn.log_model(best_model,"model")



    def train_model(self, X_train, y_train, X_test, y_test):

        models = {
            "Random Forest": RandomForestClassifier(verbose=1),
            "Decision Tree": DecisionTreeClassifier(),
            "Gradient Boosting": GradientBoostingClassifier(verbose=1),
            "Logistic Regression": LogisticRegression(verbose=1),
            "AdaBoost": AdaBoostClassifier(),
        }

        params = {
            "Decision Tree" :{
                'criterion' : ['gini', 'entropy', 'log_loss'],
                # 'splitter':['best','random'],
                # 'max_features':['sqrt','log2'],
            },

            "Random Forest":{
                # 'criterion':['gini', 'entropy', 'log_loss'],
                # 'max_features':['sqrt','log2',None],
                'n_estimators': [8,16,32,128,256]
            },

            "Gradient Boosting":{
                # 'loss':['log_loss', 'exponential'],
                'learning_rate':[.1,.01,.05,.001],
                'subsample':[0.6,0.7,0.75,0.85,0.9],
                # 'criterion':['squared_error', 'friedman_mse'],
                # 'max_features':['auto','sqrt','log2'],
                'n_estimators': [8,16,32,64,128,256]
            },

            "Logistic Regression":{},

            "AdaBoost":{
                'learning_rate':[.1,.01,.001],
                'n_estimators': [8,16,32,64,128,256]
            }
        }

        model_report: dict = evaluate_models( X_train=X_train,y_train=y_train,X_test=X_test,
                                             y_test=y_test,models=models,param=params)
        

        # Get the model with the highest test score
        best_model_name = max(model_report, key=model_report.get)
        best_model_score = model_report[best_model_name]

        # Get the trained model corresponding to the best-performing model name
        best_model = models[best_model_name]

        # Predict on training data
        y_train_pred = best_model.predict(X_train)

        classification_train_metric = get_classification_score(y_true=y_train,y_pred=y_train_pred)

        # Track the experiements with mlflow
        self.track_mlflow(best_model, classification_train_metric, run_name="Training Metrics")

        y_test_pred = best_model.predict(X_test)
        classification_test_metric = get_classification_score(y_true=y_test,y_pred=y_test_pred)

        # Track the experiements with mlflow
        self.track_mlflow(best_model, classification_test_metric , run_name="Testing Metrics")


        # Load the saved preprocessing object (KNNImputer pipeline)
        preprocessor = load_object(file_path=self.data_transformation_artifact.transformed_object_file_path)

        # Get the directory where the trained model will be saved, Create the directory if it doesn't already exist
        # Artifacts/08_06_2026_11_58_09/model_trainer/trained_model/
        model_dir_path = os.path.dirname(self.model_trainer_config.trained_model_file_path)
        os.makedirs(model_dir_path,exist_ok=True)

        # Create a single object containing both the preprocessor and trained model
        network_model = NetworkModel(preprocessor=preprocessor, model=best_model)
        # Save the combined NetworkModel object for future prediction/deployment
        # Artifacts/08_06_2026_11_58_09/model_trainer/trained_model/model.pkl
        save_object(self.model_trainer_config.trained_model_file_path, obj=network_model)

        # Model pusher
        save_object("final_model/model.pkl",best_model)

        # Model Trainer Artifact
        model_trainer_artifact = ModelTrainerArtifact(
            trained_model_file_path = self.model_trainer_config.trained_model_file_path,
            train_metric_artifact = classification_train_metric,
            test_metric_artifact=classification_test_metric


        )
        logging.info(f"Model trainer artifact: {model_trainer_artifact}")
        return model_trainer_artifact

    def initiate_model_trainer(self) -> ModelTrainerArtifact:

        try:
            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            test_file_path = self.data_transformation_artifact.transformed_test_file_path

            # Loading training and testing arrays
            train_arr = load_numpy_array_data(train_file_path)
            test_arr = load_numpy_array_data(test_file_path)

            X_train, y_train, X_test, y_test = (
                train_arr[:, :-1],
                train_arr[:, -1],
                test_arr[:, :-1],
                test_arr[:, -1]
            )

            model_trainer_artifact = self.train_model(X_train,y_train,X_test,y_test)
            return model_trainer_artifact
                
        except Exception as e:
            raise NetworkSecurityException(e,sys)