# from dotenv import load_dotenv
# import os

# load_dotenv()

# huggingface_token = os.getenv("HUGGINGFACE_TOKEN")

# print("Token loaded:", huggingface_token is not None)


import os 
from dotenv import load_dotenv # Allows Python to read variables from the .env file

load_dotenv() # It reads .env file and loads its variables into the environment.

from huggingface_hub import login, upload_file , delete_file # Imports Hugging Face login and file upload functions

huggingface_token = os.getenv("HUGGINGFACE_TOKEN")

login(token = huggingface_token)  # Authenticates this Python program with Hugging Face using the token
# print("Hugging Face authentication successful!")

with open("hf_test.txt", mode="w") as file_obj:
    file_obj.write("This is a test file for Hugging Face upload.")

upload_file(
    path_or_fileobj = "hf_test.txt",
    path_in_repo = "hf_test.txt",
    repo_id="mahfujurrahman/networksecurity-mlops-model",
    repo_type="model"

)

print("Hugging Face authentication and upload successful!")

delete_file(
    path_in_repo="hf_test.txt",
    repo_id="mahfujurrahman/networksecurity-mlops-model",
    repo_type="model"
)

print("Test file deleted from Hugging Face!")

