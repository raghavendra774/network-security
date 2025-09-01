import os
import sys
import pandas as pd
import numpy as np
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact
from sklearn.model_selection import train_test_split
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")

class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def export_collection_as_dataframe(self):
        try:
            database_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name
            self.mongo_client = MongoClient(MONGO_DB_URL, server_api = ServerApi('1'))
            collection = self.mongo_client[database_name][collection_name]
            df = pd.DataFrame(list(collection.find()))
            if "_id" in df.columns.to_list():
                df = df.drop(columns=["_id"], axis=1)
            df.replace({"na":np.nan}, inplace=True)
            return df
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def initiate_data_ingestion(self):
        try:
            dataframe = self.export_collection_as_dataframe()
            dataframe = self.export_data_into_feature_store(dataframe)
            self.split_data_as_train_test(dataframe)

            data_ingestion_artifact = DataIngestionArtifact(trained_file_path = self.data_ingestion_config.training_file_path, tested_file_path = self.data_ingestion_config.testing_file_path)

            return data_ingestion_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def export_data_into_feature_store(self, dataframe:pd.DataFrame):
        try:
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path, exist_ok=True)
            dataframe.to_csv(feature_store_file_path, index=False, header=True)
            return dataframe
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def split_data_as_train_test(self, dataframe: pd.DataFrame):
        try:
            train_set, test_set = train_test_split(dataframe, test_size=self.data_ingestion_config.train_test_split_ration)

            train_set = pd.DataFrame(train_set)
            test_set = pd.DataFrame(test_set)
            
            logging.info("Performed train test split on dataframe")

            logging.info(
                "Exited split_data_as_train_test methos of Data_Ingestion class"
            )
            
            os.makedirs(os.path.dirname(self.data_ingestion_config.training_file_path), exist_ok=True)

            os.makedirs(os.path.dirname(self.data_ingestion_config.testing_file_path), exist_ok=True)

            logging.info("exporting ")

            test_set.to_csv(
                self.data_ingestion_config.testing_file_path, index=False, header=True
            )

            train_set.to_csv(
                self.data_ingestion_config.training_file_path, index = False, header = True
            )

            



        except Exception as e:
            raise NetworkSecurityException(e, sys)
