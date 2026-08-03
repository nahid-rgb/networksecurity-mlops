import yaml
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import os, sys
import numpy as np
#import dill
import pickle


def read_yaml_file(file_path: str) -> dict:
    """
    Read a YAML file and return its contents as a Python dictionary.
    """
    try:
        with open(file_path, mode="rb") as yaml_file:
            # Read the YAML file and convert it into a Python dictionary
            return yaml.safe_load(yaml_file)

    except Exception as e:
        raise NetworkSecurityException(e, sys)


def write_yaml_file(file_path: str, content: object, replace: bool = False) -> None:
    """
    Write the given Python object into a YAML file.

    Args:
        file_path: Location where the YAML file will be created.
        content: Python object (dictionary, list, etc.) to write into the YAML file.
        replace: If True, delete the existing file before writing a new one.
    """
    try:
        # Delete the existing YAML file if replace=True
        if replace is True and os.path.exists(file_path):
            os.remove(file_path)

        # Create the parent directory if it does not exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Write the Python object into a YAML file
        with open(file_path, mode="w") as file:
            yaml.dump(content, file)

    except Exception as e:
        raise NetworkSecurityException(e, sys)