from datetime import datetime
import os
from networksecurity.constant import training_pipeline


class TrainingPipelineConfig:
    """
    Create the main configuration for the training pipeline.
    This class creates a unique artifact folder using the current timestamp.
    Example:
        Artifacts/
            07_21_2026_18_30_45/
    """

    def __init__(self, timestamp=None):

        # If no timestamp is provided, use the current date & time
        if timestamp is None:
            timestamp = datetime.now()

        self.timestamp = timestamp.strftime("%m_%d_%Y_%H_%M_%S")
        self.pipeline_name = training_pipeline.PIPELINE_NAME
        self.artifact_name = training_pipeline.ARTIFACT_DIR
        self.artifact_dir = os.path.join(self.artifact_name, self.timestamp)


class DataIngestionConfig:
    """
    Create all configuration paths and settings required for data ingestion.

    This class defines:
    - Where the feature store CSV will be saved.
    - Where the train.csv and test.csv files will be saved.
    - MongoDB database and collection names.
    - Train-test split ratio.

    Example:
        Artifacts/
            07_21_2026_18_30_45/
                data_ingestion/
                    feature_store/
                        phisingData.csv
                    ingested/
                        train.csv
                        test.csv
    """

    def __init__(self, training_pipeline_config: TrainingPipelineConfig):

        # Root folder for data ingestion
        # Artifacts/07_18_2026_12_30_45/data_ingestion
        self.data_ingestion_dir: str = os.path.join(
            training_pipeline_config.artifact_dir,
            training_pipeline.DATA_INGESTION_DIR_NAME
        )

        # Path where the complete dataset from MongoDB will be saved
        # Artifacts/07_18_2026_12_30_45/data_ingestion/feature_store/phisingData.csv
        self.feature_store_file_path: str = os.path.join(
            self.data_ingestion_dir,
            training_pipeline.DATA_INGESTION_FEATURE_STORE_DIR,
            training_pipeline.FILE_NAME
        )

        # Path where the training dataset will be saved
        # Artifacts/07_18_2026_12_30_45/data_ingestion/ingested/train.csv
        self.training_file_path: str = os.path.join(
            self.data_ingestion_dir,
            training_pipeline.DATA_INGESTION_INGESTED_DIR,
            training_pipeline.TRAIN_FILE_NAME
        )

        # Path where the testing dataset will be saved
        # Artifacts/07_18_2026_12_30_45/data_ingestion/ingested/test.csv
        self.testing_file_path: str = os.path.join(
            self.data_ingestion_dir,
            training_pipeline.DATA_INGESTION_INGESTED_DIR,
            training_pipeline.TEST_FILE_NAME
        )

        self.train_test_split_ratio: float = training_pipeline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATION
        self.collection_name: str = training_pipeline.DATA_INGESTION_COLLECTION_NAME
        self.database_name: str = training_pipeline.DATA_INGESTION_DATABASE_NAME