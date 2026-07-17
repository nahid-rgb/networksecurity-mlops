# import os 
import sys 
import json

MONGO_DB_URL = "mongodb+srv://phishinguser:Admin123@cluster0.kqxto99.mongodb.net/?appName=Cluster0"
print(MONGO_DB_URL)

import pandas as pd
import pymongo
from networksecurity.exception.exception import NetworkSecurityException

class NetworkDataExtract:
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def csv_tojson_converter(self,file_path):
        try:
            data=pd.read_csv(file_path)
            data.reset_index(drop=True,inplace=True)
            records=list(json.loads(data.T.to_json()).values()) # Convert DataFrame → JSON → Dictionary → List
            return records
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        

    def insert_data_mongodb(self,records,database,collection):
        try:
            # save the function arguments
            db_name = database
            collection_name = collection 
            records_to_insert = records

            # Connect to MongoDB Atlas
            client = pymongo.MongoClient(MONGO_DB_URL)

            # Open (or create) the database
            db = client[db_name]

            # Open (or create) the collection inside that database
            col = db[collection_name]

            # Insert all records into the collection
            col.insert_many(records_to_insert)

            # Return how many records were inserted
            return len(records_to_insert)

        except Exception as e:
            raise NetworkSecurityException(e,sys)    

if __name__ == '__main__':
    FILE_PATH = r"Network_Data\phisingData.csv"    #(r"" treats backslashes as normal characters)
    DATABASE = "NetworkSecurityDB"
    COLLECTION = "phishing_data"
    networkObj = NetworkDataExtract()
    records=networkObj.csv_tojson_converter(file_path=FILE_PATH)
    print(records[:5])     # Show first 5 records
    no_of_records=networkObj.insert_data_mongodb(records,DATABASE,COLLECTION)
    print(no_of_records)

