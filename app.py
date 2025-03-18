from src.my_project.logger import logging
from src.my_project.exception import CustomException
import sys
from src.my_project.components.data_ingestion import DataIngestion


if __name__ == "__main__":
    logging.info("logging has started")
    
    try:
        data_ingestion = DataIngestion()
        data_ingestion.initiate_data_ingestion()
    except Exception as e:
        logging.info("Error occured")
        raise CustomException(e, sys)