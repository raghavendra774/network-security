from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
import sys
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig, DataValidationConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig

if __name__ == "__main__":
    try:
        trainingPipelineConfig = TrainingPipelineConfig()
        dataIngestionConfig = DataIngestionConfig(trainingPipelineConfig)
        dataIngestion = DataIngestion(dataIngestionConfig)
        logging.info("Initiate the data ingestion")

        dataIngestionArtifact = dataIngestion.initiate_data_ingestion()
        logging.info("Data Initilization completed")
        data_validation_config = DataValidationConfig(trainingPipelineConfig)
        data_validation = DataValidation(dataIngestionArtifact, data_validation_config)
        logging.info("initiate data validation")
        data_validation_artifact = data_validation.initiate_data_validation()
        print(dataIngestionConfig)
        logging.info("initiate the data validation")

    except Exception as e:
        raise NetworkSecurityException(e, sys)

