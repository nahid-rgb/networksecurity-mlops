import sys
import os

import certifi
ca = certifi.where()  # Gets the location of trusted SSL certificates so Python can securely connect to MongoDB


from dotenv import load_dotenv
load_dotenv()  # Load variables from the .env file

mongo_db_url = os.getenv("MONGO_DB_URL")  # Get MongoDB URL from .env
# print(mongo_db_url)  # Prints the URL to verify that the MongoDB connection string was loaded correctly


import pymongo

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from networksecurity.pipeline.training_pipeline import TrainingPipeline  # Imports the complete ML training pipeline that will be triggered by the API


from fastapi.middleware.cors import CORSMiddleware  # Provides CORS support so a frontend from another origin can communicate with this API
from fastapi import FastAPI, File, UploadFile, Request  # FastAPI creates the API; File and UploadFile will handle uploaded files later
from uvicorn import run as app_run  # Uvicorn starts the FastAPI application and listens for incoming HTTP requests

from fastapi.responses import Response  # Used to send a response message back to the client
from starlette.responses import RedirectResponse  # Used to redirect the user from one URL to another


import pandas as pd   


from networksecurity.utils.main_utils.utils import load_object  # Used later to load saved model/preprocessor
from networksecurity.utils.ml_utils.model.estimator import NetworkModel   # Used later for prediction


client = pymongo.MongoClient(
    mongo_db_url,
    tlsCAFile=ca
)   # Creates a connection between Python and MongoDB Atlas using the MongoDB URL and SSL certificate


from networksecurity.constant.training_pipeline import DATA_INGESTION_COLLECTION_NAME
from networksecurity.constant.training_pipeline import DATA_INGESTION_DATABASE_NAME


database = client[DATA_INGESTION_DATABASE_NAME]  # Select the MongoDB database

collection = database[DATA_INGESTION_COLLECTION_NAME]   # Select the MongoDB collection


app = FastAPI()  # Creates the FastAPI application 


origins = ["*"]  # Allows requests from any frontend origin; useful during development


app.add_middleware(
    CORSMiddleware,  # Adds CORS handling to the FastAPI application
    allow_origins=origins,  # Allows requests coming from the origins listed above
    allow_credentials=True,  # Allows credentials such as authentication information to be included in requests
    allow_methods=["*"],  # Allows all HTTP methods such as GET, POST, PUT, and DELETE
    allow_headers=["*"],  # Allows the client to send any HTTP headers
)

from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="templates") # Creates a Jinja2 template object that loads HTML files from the templates folder

# Creates the root GET endpoint (/) and redirects visitors to FastAPI's /docs API documentation
@app.get("/", tags = ["authentication"])
async def index():
    return RedirectResponse(url="/docs")

# Creates the /train GET endpoint that triggers the complete ML training pipeline when requested
@app.get("/train")
async def train_route():
    try:
        train_pipeline = TrainingPipeline()
        train_pipeline.run_pipeline()
        return Response("Training is successful")
    except Exception as e:
        raise NetworkSecurityException(e,sys)

# Creates the /predict POST endpoint that receives an uploaded CSV file and generates predictions
@app.post("/predict")
async def predict_route(request: Request, file:UploadFile = File(...)): # ... means This field is required.
    try:
        df = pd.read_csv(file.file)
        preprocessor = load_object("final_model/preprocessor.pkl")
        final_model = load_object("final_model/model.pkl")

        network_model = NetworkModel(preprocessor = preprocessor, model = final_model)
        print(df.iloc[0])

        y_pred = network_model.predict(df)
        print(y_pred)
    
        df['predicted_column'] = y_pred
        os.makedirs("prediction_output" , exist_ok=True)
        df.to_csv('prediction_output/output.csv')

        # Render results as an HTML table in the browser
        table_html = df.to_html(classes='table table-striped')
        return templates.TemplateResponse(request=request,name="index.html",context={"table": table_html})
    
    except Exception as e:
        raise NetworkSecurityException(e,sys)

# Entry point: starts the Uvicorn server and runs the FastAPI application on port 8000
if __name__ == "__main__":
    
    # Use Render's PORT if it provides one.
    # If PORT does not exist, use 8000 for local testing.
    app_run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))


# uvicorn app:app --reload
# Starts the Uvicorn server for the FastAPI app in app.py and automatically reloads it when the code changes
