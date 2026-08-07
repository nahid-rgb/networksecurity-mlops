import yaml
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import os, sys
import numpy as np
#import dill
import pickle

from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV


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



def save_numpy_array_data(file_path: str, array: np.ndarray) -> None:
    """
    Save a NumPy array to a .npy file.

    Args:
        file_path (str): Path where the array will be saved.
        array (np.ndarray): NumPy array to save.
    """

    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, mode="wb") as file_obj:
            np.save(file_obj, array)

    except Exception as e:
        raise NetworkSecurityException(e, sys)



def load_numpy_array_data(file_path: str) -> np.ndarray:
    """
    Load a NumPy array from a .npy file.

    Args:
        file_path (str): Path of the NumPy (.npy) file.

    Returns:
        np.ndarray: Loaded NumPy array.
    """

    try:
        with open(file_path, "rb") as file_obj:
            return np.load(file_obj)

    except Exception as e:
        raise NetworkSecurityException(e, sys) 


    
def save_object(file_path: str, obj: object) -> None:
    """
    Save a Python object as a pickle (.pkl) file.

    Args:
        file_path (str): Path where the object will be saved.
        obj (object): Python object to save.
    """

    try:
        logging.info(f"Saving object to: {file_path}")

        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, mode="wb") as file_obj:
            pickle.dump(obj, file_obj)

        logging.info("Object saved successfully.")

    except Exception as e:
        raise NetworkSecurityException(e, sys)



def load_object(file_path: str) -> object:
    """
    Load a saved Python object from a pickle (.pkl) file.

    Args:
        file_path (str): Path of the pickle file.

    Returns:
        object: The loaded Python object.
    """

    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        with open(file_path, "rb") as file_obj:
            return pickle.load(file_obj)

    except Exception as e:
        raise NetworkSecurityException(e, sys)



def evaluate_models(X_train, y_train, X_test, y_test, models, param):
    """
    Train multiple models using GridSearchCV, evaluate them,
    and return the test R² score of each model.

    Args:
        X_train: Training features.
        y_train: Training target.
        X_test: Testing features.
        y_test: Testing target.
        models (dict): Dictionary containing model names and model objects.
        param (dict): Dictionary containing hyperparameter grids for each model.

    Returns:
      dict: Dictionary containing each model name and its corresponding test R² score.
    """
    try:
        model_performance = {}

        for model_name, model in models.items():

            # Hyperparameters for the current model
            parameters = param[model_name]

            # Initialize GridSearchCV
            grid_search = GridSearchCV(estimator=model,param_grid=parameters, cv=3)
        
            # Try all hyperparameter combinations using cross-validation and store the results
            grid_search.fit(X_train, y_train)

            # Update the model with the best hyperparameters found
            model.set_params(**grid_search.best_params_)

            # Train the final model on the full training dataset
            model.fit(X_train, y_train)

            # Predictions
            y_train_pred = model.predict(X_train)
            y_test_pred = model.predict(X_test)

            # Model performance
            train_model_score = r2_score(y_train, y_train_pred)
            test_model_score = r2_score(y_test, y_test_pred)

            model_performance[model_name] = test_model_score

        return model_performance

    except Exception as e:
        raise NetworkSecurityException(e, sys)