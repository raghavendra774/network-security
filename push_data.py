import os
import sys
import json

from dotenv import load_dotenv
import certifi
import pandas as pd
import numpy as np
import pymongo
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging


load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")

ca = certifi.where()

class NetworkDataExtract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def csv_to_json_converter(self, file_path):
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)
            records = json.loads(data.to_json(orient='records'))
            return records

        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def insert_data_mongodb(self, records, database, collection):
        try:
            self.database = database
            self.collection = collection
            self.records = records

            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            self.database = self.mongo_client[self.database]

            self.collection = self.database[self.collection]

            self.collection.insert_many(self.records) 

            return(len(self.records))

        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
if __name__ == "__main__":
    FILE_PATH = 'Network_Data\phisingData.csv'

    DATABASE = 'NetworkDB'

    COLLECTION = 'NetworkTB'

    networkObj = NetworkDataExtract()

    json_records = networkObj.csv_to_json_converter(file_path=FILE_PATH)

    no_of_records = networkObj.insert_data_mongodb(records=json_records, database=DATABASE, collection=COLLECTION)

    print(no_of_records)



