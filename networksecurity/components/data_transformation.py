import os
import sys
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline
from networksecurity.entity.config_entity import DataTransmationConfig
from networksecurity.entity.artifact_entity import DataValidationArtifact, DataTransformationArtifact
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.constants.training_pipeline import TARGET_COLUMN, DATA_TRANSFORMATION_IMPUTER_PARAMS
from networksecurity.utils.main_utils.utils import save_numpy_array_data, save_object

class DataTransformation:
    def __init__(self,data_validation_artifact : DataValidationArtifact, data_transformation_config: DataTransmationConfig):
        try:
            self.data_transformation_config : DataTransmationConfig = data_transformation_config
            self.data_validation_artifact : DataValidationArtifact = data_validation_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    @staticmethod
    def read_data(file_path : str) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def get_data_transformer_obj(self) -> Pipeline:
        logging.info(
            "Entered get data_transformer_obj method of transformation class"
        )
        try:
            imputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            logging.info("initialized KNN Imputer")
            processor: Pipeline = Pipeline([
                ("imputer",imputer)
            ])
            return processor
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def initiate_data_transformation(self) -> DataTransformationArtifact:
        try:
            train_df = DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)

            test_df = DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)

            input_features_train_df = train_df.drop(columns=[TARGET_COLUMN], axis=1)

            target_feature_train_df = np.array(train_df[TARGET_COLUMN].map({-1:0, 1:1})).reshape(-1,1)

            input_features_test_df = test_df.drop(columns=[TARGET_COLUMN], axis=1)

            target_feature_test_df = np.array(test_df[TARGET_COLUMN].map({-1:0, 1:1})).reshape(-1,1)

            preprocessor = self.get_data_transformer_obj()

            preprocessor_obj = preprocessor.fit(input_features_train_df)

            transformed_input_train_feature = preprocessor_obj.transform(input_features_train_df)

            transformed_input_test_feature = preprocessor_obj.transform(input_features_test_df)

            train_arr = np.concatenate([transformed_input_train_feature, (target_feature_train_df)], axis=1)

            test_arr = np.concatenate([transformed_input_test_feature, (target_feature_test_df)], axis=1)

            save_numpy_array_data(self.data_transformation_config.data_transformation_train_file_path, train_arr)

            save_numpy_array_data(self.data_transformation_config.data_transformation_test_file_path, test_arr)

            save_object(self.data_transformation_config.data_transformed_object_file_path, preprocessor_obj)

            data_transformation_artifact = DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.data_transformed_object_file_path,
                transformed_test_file_path=self.data_transformation_config.data_transformation_test_file_path,
                transformed_train_file_path=self.data_transformation_config.data_transformation_train_file_path
            )

            return data_transformation_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)

