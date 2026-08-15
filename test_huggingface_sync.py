# from networksecurity.cloud.huggingface_syncer import HuggingFaceSync

# huggingface_sync = HuggingFaceSync()

# huggingface_sync.upload_folder_to_huggingface(
#     local_folder="hf_upload_test",
#     repository_folder="test_upload"
# )

# print("Hugging Face folder upload successful!")


# # Delete the test file from the Hugging Face repository
# delete_file(
#     path_in_repo="test_upload/test.txt",
#     repo_id="mahfujurrahman/networksecurity-mlops-model",
#     repo_type="model",
#     token=huggingface_token
# )

# print("Test file deleted from Hugging Face successfully!")

from dotenv import load_dotenv
from huggingface_hub import delete_file
import os

load_dotenv()

huggingface_token = os.getenv("HUGGINGFACE_TOKEN")

# Delete the test file from the Hugging Face repository
delete_file(
    path_in_repo="test_upload/test.txt",
    repo_id="mahfujurrahman/networksecurity-mlops-model",
    repo_type="model",
    token=huggingface_token
)

print("Test file deleted from Hugging Face successfully!")