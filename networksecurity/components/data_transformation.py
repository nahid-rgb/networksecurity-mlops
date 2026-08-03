import sys
import os
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

from networksecurity.constant.training_pipeline import TARGET_COLUMN
from networksecurity.constant.training_pipeline import DATA_TRANSFORMATION_IMPUTER_PARAMS

from networksecurity.entity.artifact_entity import (
    DataTransformationArtifact,
    DataValidationArtifact
)

from networksecurity.entity.config_entity import DataTransformationConfig
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.utils.main_utils.utils import save_numpy_array_data, save_object


class DataTransformation:

    def __init__(self, data_validation_artifact: DataValidationArtifact,
                 data_transformation_config: DataTransformationConfig):

        try:
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = data_transformation_config
        except Exception as e:
            raise NetworkSecurityException(e, sys)


    @staticmethod
    def read_data(file_path: str) -> pd.DataFrame:
        """
        Read a CSV file and return it as a Pandas DataFrame.
        """
        try:
            return pd.read_csv(file_path)

        except Exception as e:
            raise NetworkSecurityException(e, sys)


    @staticmethod
    def get_data_transformer_object() -> Pipeline:
        """
        Create and return the preprocessing pipeline.

        Currently, the pipeline contains only a KNNImputer
        to replace missing values in the dataset.

        Returns:
            Pipeline: A Scikit-learn Pipeline object.
        """

        logging.info("Initializing the data transformation pipeline.")

        try:
            imputer: KNNImputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            logging.info(f"Initialized KNNImputer with parameters: {DATA_TRANSFORMATION_IMPUTER_PARAMS}")

            processor: Pipeline = Pipeline([("imputer", imputer)])
            return processor

        except Exception as e:
            raise NetworkSecurityException(e, sys)


    def initiate_data_transformation(self) -> DataTransformationArtifact:

        logging.info("Entered initiate_data_transformation method of DataTransformation class")

        try:
            logging.info("Starting data transformation")

            train_df = DataTransformation.read_data(
                self.data_validation_artifact.valid_train_file_path
            )

            test_df = DataTransformation.read_data(
                self.data_validation_artifact.valid_test_file_path
            )

            # Training dataframe
            input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN])
            target_feature_train_df = train_df[TARGET_COLUMN]
            target_feature_train_df = target_feature_train_df.replace(-1, 0)

            # Testing dataframe
            input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN])
            target_feature_test_df = test_df[TARGET_COLUMN]
            target_feature_test_df = target_feature_test_df.replace(-1, 0)

            preprocessor = self.get_data_transformer_object()

            # Fit the preprocessing pipeline on the training data
            preprocessor_object = preprocessor.fit(input_feature_train_df)

            # Transform the training and testing input features
            transformed_input_train_feature = preprocessor_object.transform(input_feature_train_df)
            transformed_input_test_feature = preprocessor_object.transform(input_feature_test_df)

            # Combine transformed input features with the target column
            train_arr = np.c_[transformed_input_train_feature, np.array(target_feature_train_df)]
            test_arr = np.c_[transformed_input_test_feature, np.array(target_feature_test_df)]

            # Save transformed NumPy arrays
            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path, array=train_arr)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path,array=test_arr)

            # Save the fitted preprocessing pipeline
            save_object(self.data_transformation_config.transformed_object_file_path,preprocessor_object)
            # Save another copy for prediction/deployment
            save_object("final_model/preprocessor.pkl",preprocessor_object,)

            data_transformation_artifact = DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path,
            )

            return data_transformation_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)