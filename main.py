from networksecurity.components.data_ingestion import DataIngestion
import sys
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig

if __name__ == "__main__":
    try:
        trainingPipelineConfig = TrainingPipelineConfig()
        dataIngestionConfig = DataIngestionConfig(trainingPipelineConfig)
        dataIngestion = DataIngestion(dataIngestionConfig)
        logging.info("Initiate the data ingestion")
        dataIngestionArtifact = dataIngestion.initiate_data_ingestion()

        print(dataIngestionConfig)

    except Exception as e:
        raise NetworkSecurityException(e, sys)

