import os
import sys
from src.my_project.logger import logging
from src.my_project.exception import CustomException
import pandas as pd
from dotenv import load_dotenv
import pymysql

import pickle
import numpy as np


load_dotenv()

host = os.getenv('host')
user = os.getenv('user')
password = os.getenv('password')
db = os.getenv('database')


def read_sql_data():
    logging.info('Reading from mysql DB')
    try:
        mydb = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=db
        )
        logging.info('Connected to mysql DB', mydb)
        
        df = pd.read_sql_query('SELECT * FROM students', mydb)
        print(df.head())
        
        return df
        
        
    except Exception as e:
        raise CustomException(e, sys)
    
def save_object(file_path, obj):
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)
    except Exception as e:
        raise CustomException(e, sys)