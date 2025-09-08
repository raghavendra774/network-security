import sys
import os
from networksecurity.entity.artifact_entity import DataTransformationArtifact, ModelTrainerArtifact
from networksecurity.entity.config_entity import ModelTrainerConfig
from networksecurity.utils.main_utils.utils import save_object, load_numpy_array_data, load_object
from networksecurity.utils.ml_utils.metric.classification_metric import get_classification_metrics

from networksecurity.exception.exception import NetworkSecurityException

from networksecurity.utils.ml_utils.model.estimator import NetworkModel

from networksecurity.utils.main_utils.utils import evaluate_model

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    AdaBoostClassifier,
    GradientBoostingClassifier,
    RandomForestClassifier
)
import mlflow
# import dagshub


# dagshub.init(repo_owner='raghavendra774', repo_name='network-security', mlflow=True)


class ModelTrainer:
    def __init__(self, model_trainer_config: ModelTrainerConfig, data_transformation_artifact: DataTransformationArtifact):
        self.model_trainer_config = model_trainer_config
        self.data_transformation_artifact = data_transformation_artifact

    def track_mlflow(self, best_model, classificationMetric):
        with mlflow.start_run():
            f1_score = classificationMetric.f1_score
            precision_score = classificationMetric.precision_score
            recall_score = classificationMetric.recall_score

            mlflow.log_metric("f1_score", f1_score)
            mlflow.log_metric("precision", precision_score)
            mlflow.log_metric("recall_score", recall_score)

            mlflow.sklearn.log_model(best_model, "model")

    def read_data(self, file_path:str):
        try:
            return load_numpy_array_data(file_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def train_model(self, X_train, y_train, X_test, y_test):

        models = {
            "Random Forest" : RandomForestClassifier(verbose=1),
            "Decision Tree" : DecisionTreeClassifier(),
            "Gradient Boosting" : GradientBoostingClassifier(verbose=1),
            "Logistic Regression" : LogisticRegression(verbose=1),
            "AdaBoost" : AdaBoostClassifier()
        }

        params = {
            "Decision Tree" : {
                "criterion" : ['gini', 'entropy', 'log_loss'],
                # 'splitter' : ['best', 'random'],
                # 'max_features' : ['sqrt', 'log2']
            },
            "Random Forest" : {
                "n_estimators" : [8, 16, 32, 64, 128, 256],
                # "criterion" : ['gini', 'entropy', 'log_loss'],
                # 'max_features' : ['sqrt', 'log2']
            },
            "Gradient Boosting" : {
                "learning_rate" : [.1,.01,.05,.001],
                "subsample" : [0.6, 0.7, 0.75,0.8,0.85,0.9],
                # "loss" : ['log_loss', 'exponential'],
                # "criterion" : ['squared_error', 'friedman_mse'],
                # "max_features" : ['auto', 'sqrt', 'log2'],
                'n_estimators' : [8, 16, 32, 64, 128, 256]
            },
            "Logistic Regression" : {

            },
            "AdaBoost": {
                'learning_rate': [0.1, .01, 0.5,.001],
                'n_estimators' : [7, 16, 32, 64, 128, 256]
            }
        }

        model_report: dict = evaluate_model(X_train, y_train, X_test, X_test, models, params)

        best_model_score = max(sorted(model_report.values()))

        best_model_name = list(model_report.keys())[
            list(model_report.values()).index(best_model_score)
        ]

        best_model = models[best_model_name]

        y_train_predict = best_model.predict(X_train)

        classification_train_metric = get_classification_metrics(y_train, y_train_predict)

        # Track the experiments with mlFlow
        self.track_mlflow(best_model, classification_train_metric)

        y_test_pred = best_model.predict(X_test)

        classification_test_metric = get_classification_metrics(y_test, y_test_pred)

        preProcessor = load_object(file_path=self.data_transformation_artifact.transformed_object_file_path)

        model_dir_path = os.path.dirname(self.model_trainer_config.model_trainer_file_path)

        os.makedirs(model_dir_path, exist_ok=True)

        Network_Model = NetworkModel(preprocessor=preProcessor, model=best_model)

        save_object(self.model_trainer_config. model_trainer_file_path, obj= Network_Model)

        save_object("final_model/model.pkl",best_model)

        model_trainer_artifact = ModelTrainerArtifact(trained_model_file_path=self.model_trainer_config.model_trainer_file_path, train_metric_artifact=classification_train_metric, test_metric_artifact= classification_test_metric)

        return model_trainer_artifact

    def initiate_model_trainer(self):
        try:
            
            train_arr = self.read_data(self.data_transformation_artifact.transformed_train_file_path)

            test_arr = self.read_data(self.data_transformation_artifact.transformed_test_file_path)

            X_train, y_train, X_test, y_test = (
                train_arr[:, :-1],
                train_arr[:, -1],
                test_arr[:, :-1],
                test_arr[:, -1]
            )

            model = self.train_model(X_train, y_train, X_test=X_test, y_test=y_test)



        except Exception as e:
            raise NetworkSecurityException(e, sys)
