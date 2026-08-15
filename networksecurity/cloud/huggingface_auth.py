import os

from dotenv import load_dotenv  # Allows Python to read variables from the .env file
from huggingface_hub import login  # Imports Hugging Face's login function


def authenticate_huggingface():
    """Authenticates the application with Hugging Face using the token from .env."""

    load_dotenv()  # Reads the .env file and loads its variables into the environment

    huggingface_token = os.getenv("HUGGINGFACE_TOKEN")
    # Gets the Hugging Face access token from the HUGGINGFACE_TOKEN variable in .env

    if huggingface_token is None:
        # Checks whether the token was actually found in the .env file
        raise ValueError("HUGGINGFACE_TOKEN is not set in the .env file.")

    login(token=huggingface_token)
    # Authenticates this Python application with Hugging Face using the token
    # Hugging Face saves the credentials locally, so upload_folder() can use them later