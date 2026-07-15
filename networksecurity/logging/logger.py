import logging
import os
from datetime import datetime

LOG_FILE_NAME = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
# name of the log file e.g. "07_03_2026_14_32_55.log"

LOG_FOLDER_PATH = os.path.join(os.getcwd(), "logs", LOG_FILE_NAME)
# full path to the folder that will contain the log file
# e.g. "D:/ML_Project/logs/07_03_2026_14_32_55.log"


os.makedirs(LOG_FOLDER_PATH,exist_ok=True)
# creates the folder on disk if it does not already exist


LOG_FILE_PATH = os.path.join(LOG_FOLDER_PATH, LOG_FILE_NAME)
# full path to the actual log file inside the folder
# e.g. "D:/ML_Project/logs/07_03_2026_14_32_55.log/07_03_2026_14_32_55.log"


logging.basicConfig(
    filename=LOG_FILE_PATH,
    # write all logs to this file instead of the terminal
    # e.g. "D:/ML_Project/logs/07_03_2026_14_32_55.log/07_03_2026_14_32_55.log"


    format = "[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    # defines how every log line looks when written to the file
    #
    # %(asctime)s   → timestamp          e.g. 2026-07-03 14:32:55,123
    # %(lineno)d    → line number        e.g. 47          (d = integer)
    # %(name)s      → logger name        e.g. root        (s = string)
    # %(levelname)s → severity level     e.g. INFO / ERROR / WARNING
    # %(message)s   → your log message   e.g. "Data ingestion started"
    #
    # output: [ 2026-07-03 14:32:55,123 ] 47 root - INFO - Data ingestion started


    level  = logging.INFO,
    # minimum severity level to record:
    
    # DEBUG    = 10  → ignored (below INFO)
    # INFO     = 20  → recorded ← set to this
    # WARNING  = 30  → recorded
    # ERROR    = 40  → recorded
    # CRITICAL = 50  → recorded
)

