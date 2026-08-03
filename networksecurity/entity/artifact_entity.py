from dataclasses import dataclass


@dataclass
class DataIngestionArtifact:
    """
    Store the paths of train.csv and test.csv.
    """
    trained_file_path: str
    test_file_path: str


@dataclass
class DataValidationArtifact:
    """
    Store the output produced after the data validation stage.

    This artifact contains:
    - Validation status.
    - Paths to the validated train and test datasets.
    - Paths to the invalid train and test datasets (if any).
    - Path to the data drift report.
    """

    validation_status: bool
    valid_train_file_path: str
    valid_test_file_path: str
    invalid_train_file_path: str
    invalid_test_file_path: str
    drift_report_file_path: str


@dataclass
class DataTransformationArtifact:
    """
    Store the output produced after the data transformation stage.

    This artifact contains:
    - Path to the saved preprocessing object (preprocessor.pkl).
    - Path to the transformed training dataset (train.npy).
    - Path to the transformed testing dataset (test.npy).
    """
    
    transformed_object_file_path: str
    transformed_train_file_path: str
    transformed_test_file_path: str
