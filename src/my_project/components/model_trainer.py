import sys
import os
from dataclasses import dataclass

from catboost import CatBoostRegressor
from sklearn.ensemble import (
    RandomForestRegressor,
    GradientBoostingRegressor,
    AdaBoostRegressor,
)

from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsRegressor
from xgboost import XGBRegressor
from sklearn.tree import DecisionTreeRegressor

from src.my_project.logger import logging
from src.my_project.exception import CustomException
from src.my_project.utils import (
    save_object,
    evaluate_models,
)


@dataclass
class ModelTrainerConfig:
    trained_model_filepath = os.path.join("artifacts", "trained_model.pkl")


class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def initiate_model_trainer(self, train_arr, test_arr):
        try:
            logging.info("Initiating Model Trainer")
            logging.info("Split Train and Test Data")
            X_train,y_train,X_test,y_test=(
                train_arr[:,:-1],
                train_arr[:,-1],
                test_arr[:,:-1],
                test_arr[:,-1]
            )
            logging.info("Model Training Started")
            models = {
                "Linear Regression":LinearRegression(),
                "Random Forest":RandomForestRegressor(),
                "Gradient Boosting":GradientBoostingRegressor(),
                "Decision Tree":DecisionTreeRegressor(),
                "XGBRegressor":XGBRegressor(),
                "CatBoosting Regressor":CatBoostRegressor(verbose = False),
                "AdaBoost Regressor":AdaBoostRegressor(),
            }
            
            
            params={
                "Decision Tree": {
                    'criterion':['squared_error', 'friedman_mse', 'absolute_error', 'poisson'],
                    # 'splitter':['best','random'],
                    # 'max_features':['sqrt','log2'],
                },
                "Random Forest":{
                    # 'criterion':['squared_error', 'friedman_mse', 'absolute_error', 'poisson'],
                    # 'max_features':['sqrt','log2',None],
                    'n_estimators': [8,16,32,64,128,256]
                },
                "Gradient Boosting":{
                    # 'loss':['squared_error', 'huber', 'absolute_error', 'quantile'],
                    'learning_rate':[.1,.01,.05,.001],
                    'subsample':[0.6,0.7,0.75,0.8,0.85,0.9],
                    # 'criterion':['squared_error', 'friedman_mse'],
                    # 'max_features':['auto','sqrt','log2'],
                    'n_estimators': [8,16,32,64,128,256]
                },
                "Linear Regression":{},
                "XGBRegressor":{
                    'learning_rate':[.1,.01,.05,.001],
                    'n_estimators': [8,16,32,64,128,256]
                },
                "CatBoosting Regressor":{
                    'depth': [6,8,10],
                    'learning_rate': [0.01, 0.05, 0.1],
                    'iterations': [30, 50, 100]
                },
                "AdaBoost Regressor":{
                    'learning_rate':[.1,.01,0.5,.001],
                    # 'loss':['linear','square','exponential'],
                    'n_estimators': [8,16,32,64,128,256]
                }
                
            }
            
            model_report:dict = evaluate_models(X_train, y_train, X_test, y_test, models, params)
            logging.info("Model Training Completed")
            best_model_score = max(sorted(model_report.values()))
            
            best_model_name = [k for k, v in model_report.items() if v == best_model_score][0]
            
            if best_model_score < 0.6:
                raise CustomException("No best Model Found", sys)
            
            logging.info(f"Best Model Found, Model Name: {best_model_name} , Model Score: {best_model_score}")
            logging.info("Saving Best Model") 
            
            best_model = models[best_model_name]
            
            save_object(file_path=self.model_trainer_config.trained_model_filepath, obj = best_model)
            logging.info("Model Saved Successfully")
            
            predicted = best_model.predict(X_test)
            r2 = r2_score(y_test, predicted)
            
            return r2
            
        except Exception as e:
            raise CustomException(e, sys)