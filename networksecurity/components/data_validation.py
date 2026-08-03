from networksecurity.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.constant.training_pipeline import SCHEMA_FILE_PATH

# Kolmogorov-Smirnov Test (KS Test)
# Used to detect data drift between train and test datasets.
from scipy.stats import ks_2samp

import pandas as pd
import os, sys
from networksecurity.utils.main_utils.utils import read_yaml_file, write_yaml_file


class DataValidation:

    def __init__(self, data_ingestion_artifact: DataIngestionArtifact,
                 data_validation_config: DataValidationConfig):

        try:
            self.data_ingestion_artifact = data_ingestion_artifact  # Stores the Data Ingestion output (train.csv and test.csv paths)
            self.data_validation_config = data_validation_config    # Stores all paths required during data validation
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)  # Read schema.yaml once and keep it in memory for validation

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
        

    def validate_number_of_columns(self, dataframe: pd.DataFrame) -> bool:
        """
        Check whether the DataFrame contains the expected number of columns.
        """
        try:
            number_of_columns = len(self._schema_config)
            logging.info(f"Required number of columns: {number_of_columns}")
            logging.info(f"DataFrame has columns: {len(dataframe.columns)}")

            if len(dataframe.columns) == number_of_columns:
                return True

            return False

        except Exception as e:
            raise NetworkSecurityException(e, sys)
        

    def validate_numerical_columns(self, dataframe: pd.DataFrame) -> bool:
        """
        Check whether all required numerical columns exist in the DataFrame.
        """
        try:
            numerical_columns = self._schema_config["numerical_columns"]
            logging.info(f"Required numerical columns: {numerical_columns}")
            logging.info(f"DataFrame columns: {list(dataframe.columns)}")

            for column in numerical_columns:
                if column not in dataframe.columns:
                    return False

            return True

        except Exception as e:
            raise NetworkSecurityException(e, sys)
        

    def detect_dataset_drift(self, base_df: pd.DataFrame, current_df: pd.DataFrame, threshold=0.05) -> bool:
        """
        Compare the training and testing datasets using the KS test
        to detect data drift and generate a drift report.
        """
        try:
            status = True
            report = {}

            # Compare every column in the training and testing datasets
            for column in base_df.columns:

                d1 = base_df[column]
                d2 = current_df[column]

                # Perform the Kolmogorov-Smirnov (KS) test
                is_same_dist = ks_2samp(d1, d2)
                if threshold <= is_same_dist.pvalue:
                    is_found = False
                else:
                    is_found = True
                    status = False

                # Store the p-value and drift status for each column
                report.update({
                    column: {
                        "p_value": float(is_same_dist.pvalue),
                        "drift_status": is_found
                    }
                })

            drift_report_file_path = self.data_validation_config.drift_report_file_path

            # Create the drift report directory if it does not exist
            dir_path = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path, exist_ok=True)

            write_yaml_file(file_path=drift_report_file_path, content=report, replace=False)

            return status

        except Exception as e:
            raise NetworkSecurityException(e, sys)


    def initiate_data_validation(self) -> DataValidationArtifact:

        try:
            train_file_path = self.data_ingestion_artifact.trained_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            # Read the train and test datasets
            train_dataframe = DataValidation.read_data(train_file_path)
            test_dataframe = DataValidation.read_data(test_file_path)

            # Validate the number of columns in the training and testing datasets
            status = self.validate_number_of_columns(train_dataframe)
            if status is False:
                error_message = "Train dataframe does not contain all required columns.\n"
            status = self.validate_number_of_columns(test_dataframe)
            if status is False:
                error_message = "Test dataframe does not contain all required columns.\n"

            # Validate the numerical columns in the training and testing datasets
            status = self.validate_numerical_columns(train_dataframe)
            if status is False:
                error_message = "Train dataframe does not contain all required numerical columns.\n"
            status = self.validate_numerical_columns(test_dataframe)
            if status is False:
                error_message = "Test dataframe does not contain all required numerical columns.\n"

            # Check data drift
            status = self.detect_dataset_drift(base_df=train_dataframe, current_df=test_dataframe)

            dir_path = os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path, exist_ok=True)

            train_dataframe.to_csv(
                self.data_validation_config.valid_train_file_path,
                index=False,
                header=True
            )

            test_dataframe.to_csv(
                self.data_validation_config.valid_test_file_path,
                index=False,
                header=True
            )

            data_validation_artifact = DataValidationArtifact(
                validation_status=status,
                valid_train_file_path=self.data_validation_config.valid_train_file_path,
                valid_test_file_path=self.data_validation_config.valid_test_file_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path
            )

            return data_validation_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)