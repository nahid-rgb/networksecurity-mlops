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