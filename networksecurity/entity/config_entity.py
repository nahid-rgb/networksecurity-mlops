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


class DataValidationConfig:
    """
    Create all configuration paths and settings required for data validation.

    This class defines:
    - Where the validated train.csv and test.csv files will be saved.
    - Where the invalid train.csv and test.csv files will be saved.
    - Where the data drift report (report.yaml) will be generated.

    Example:
        Artifacts/
            07_21_2026_18_30_45/
                data_validation/
                    validated/
                        train.csv
                        test.csv
                    invalid/
                        train.csv
                        test.csv
                    drift_report/
                        report.yaml
    """

    def __init__(self, training_pipeline_config: TrainingPipelineConfig):

        # Root folder for data validation
        # Artifacts/07_21_2026_18_30_45/data_validation
        self.data_validation_dir: str = os.path.join(
            training_pipeline_config.artifact_dir,
            training_pipeline.DATA_VALIDATION_DIR_NAME
        )

        # Folder where validated train.csv and test.csv will be stored
        # Artifacts/07_21_2026_18_30_45/data_validation/validated/
        self.valid_data_dir: str = os.path.join(
            self.data_validation_dir,
            training_pipeline.DATA_VALIDATION_VALID_DIR
        )

        # Folder where invalid train.csv and test.csv will be stored
        # Artifacts/07_21_2026_18_30_45/data_validation/invalid/
        self.invalid_data_dir: str = os.path.join(
            self.data_validation_dir,
            training_pipeline.DATA_VALIDATION_INVALID_DIR
        )

        # Path where the validated training dataset will be saved
        # Artifacts/07_21_2026_18_30_45/data_validation/validated/train.csv
        self.valid_train_file_path: str = os.path.join(
            self.valid_data_dir,
            training_pipeline.TRAIN_FILE_NAME
        )

        # Path where the validated testing dataset will be saved
        # Artifacts/07_21_2026_18_30_45/data_validation/validated/test.csv
        self.valid_test_file_path: str = os.path.join(
            self.valid_data_dir,
            training_pipeline.TEST_FILE_NAME
        )

        # Path where the invalid training dataset will be saved
        # Artifacts/07_21_2026_18_30_45/data_validation/invalid/train.csv
        self.invalid_train_file_path: str = os.path.join(
            self.invalid_data_dir,
            training_pipeline.TRAIN_FILE_NAME
        )

        # Path where the invalid testing dataset will be saved
        # Artifacts/07_21_2026_18_30_45/data_validation/invalid/test.csv
        self.invalid_test_file_path: str = os.path.join(
            self.invalid_data_dir,
            training_pipeline.TEST_FILE_NAME
        )
        
        # Path where the data drift report will be generated
        # Artifacts/07_21_2026_18_30_45/data_validation/drift_report/report.yaml
        self.drift_report_file_path: str = os.path.join(
            self.data_validation_dir,
            training_pipeline.DATA_VALIDATION_DRIFT_REPORT_DIR,
            training_pipeline.DATA_VALIDATION_DRIFT_REPORT_FILE_NAME
        )




class DataTransformationConfig:
    """
    Create all configuration paths and settings required for data transformation.

    This class defines:
    - Where the transformed training dataset (.npy) will be saved.
    - Where the transformed testing dataset (.npy) will be saved.
    - Where the preprocessing object (preprocessor.pkl) will be saved.

    Example:
        Artifacts/
            08_03_2026_18_30_45/
                data_transformation/
                    transformed/
                        train.npy
                        test.npy
                    transformed_object/
                        preprocessor.pkl
    """

    def __init__(self, training_pipeline_config: TrainingPipelineConfig):

        # Root folder for data transformation
        # Artifacts/08_03_2026_18_30_45/data_transformation
        self.data_transformation_dir: str = os.path.join(
            training_pipeline_config.artifact_dir,
            training_pipeline.DATA_TRANSFORMATION_DIR_NAME
        )

        # Path where the transformed training dataset will be saved
        # Artifacts/08_03_2026_18_30_45/data_transformation/transformed/train.npy
        self.transformed_train_file_path: str = os.path.join(
            self.data_transformation_dir,
            training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,
            training_pipeline.TRAIN_FILE_NAME.replace("csv", "npy")
        )

        # Path where the transformed testing dataset will be saved
        # Artifacts/08_03_2026_18_30_45/data_transformation/transformed/test.npy
        self.transformed_test_file_path: str = os.path.join(
            self.data_transformation_dir,
            training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,
            training_pipeline.TEST_FILE_NAME.replace("csv", "npy")
        )

        # Path where the fitted preprocessing object will be saved
        # Artifacts/08_03_2026_18_30_45/data_transformation/transformed_object/preprocessor.pkl
        self.transformed_object_file_path: str = os.path.join(
            self.data_transformation_dir,
            training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR,
            training_pipeline.PREPROCESSING_OBJECT_FILE_NAME
        )

        