import os
import sys
from src.my_project.logger import logging
from src.my_project.exception import CustomException
import pandas as pd
from dotenv import load_dotenv
import pymysql


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