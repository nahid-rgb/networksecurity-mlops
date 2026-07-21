from dataclasses import dataclass


@dataclass
class DataIngestionArtifact:
    """
    Store the paths of train.csv and test.csv.
    """
    trained_file_path: str
    test_file_path: str