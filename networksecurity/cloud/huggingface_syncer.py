import sys
from huggingface_hub import upload_folder
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging


class HuggingFaceSync:

    def upload_folder_to_huggingface(self, local_folder, repository_folder):

        """Uploads a local folder to the Hugging Face model repository."""

        # Authentication is handled by authenticate_huggingface().
        # It loads the Hugging Face token from the .env file and authenticates
        # the application before upload_folder() sends files to the repository.

        try:
            logging.info(f"Uploading '{local_folder}' to Hugging Face at '{repository_folder}'")
            upload_folder(
                folder_path=local_folder,
                path_in_repo=repository_folder,
                repo_id="mahfujurrahman/networksecurity-mlops-model",
                repo_type="model"
            )
            logging.info("Upload to Hugging Face completed successfully")

        except Exception as e:
            raise NetworkSecurityException(e, sys)