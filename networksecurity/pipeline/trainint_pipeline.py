import os
import sys

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.model_trainer import ModelTrainer

from networksecurity.entity.config_entity import (
    TrainingPipelineConfig,
    DataIngestionConfig,
    DataValidationConfig,
    DataTransmationConfig,
    ModelTrainerConfig
)

from networksecurity.entity.artifact_entity import (
    DataIngestionArtifact,
    DataValidationArtifact,
    DataTransformationArtifact,
    ModelTrainerArtifact
)

class TrainingPipelien:
    def __init__(self):
        self.trainingPipelineConfig = TrainingPipelineConfig()
        
    def startDataIngestion(self):
        try:
            self.dataIngestionConfig = DataIngestionConfig(self.trainingPipelineConfig)
            logging.info("start DataIngestion")
            data_ingestion = DataIngestion(data_ingestion_config=self.dataIngestionConfig)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info(f"Data Ingestion complete and artifact : {data_ingestion_artifact}")
            return data_ingestion_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def startDataValidation(self, data_ingestion_artifact: DataIngestionArtifact):
        try:
            data_validation_config = DataValidationConfig(self.trainingPipelineConfig)
            data_validation = DataValidation(data_ingestion_artifact, data_validation_config)
            data_validation_artifact = data_validation.initiate_data_validation()
            return data_validation_config

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def startDataTransformation(self, data_Validation_artifact: DataValidationArtifact):
        try:
            data_transformation_config = DataTransmationConfig(self.trainingPipelineConfig)
            data_transformation = DataTransformation(data_validation_artifact=data_Validation_artifact, data_transformation_config=data_transformation_config)  
            data_transformation_artifact = data_transformation.initiate_data_transformation()
            return data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def startModelTrainer(self, data_transformation_artifact: DataTransformationArtifact):
        try:
            model_trainer_config = ModelTrainerConfig(self.trainingPipelineConfig)
            model_trainer = ModelTrainer(
                data_transformation_artifact=data_transformation_artifact,
                model_trainer_config=model_trainer_config
            )
            model_trainer_artifact = model_trainer.initiate_model_trainer()
            return model_trainer_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def runPipeline(self):
        try:
            data_ingestion_artifact = self.startDataIngestion()
            data_validation_artifact = self.startDataValidation(data_ingestion_artifact)
            data_transformation_artifact = self.startDataTransformation(data_validation_artifact)
            model_trainer_artifact = self.startModelTrainer(data_transformation_artifact)
            return model_trainer_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)