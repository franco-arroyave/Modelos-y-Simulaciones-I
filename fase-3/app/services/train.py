import time
from loguru import logger
import pandas as pd
from catboost import CatBoostRegressor
from app.utils.tools import dataValidation, clean_data

h_param={'learning_rate': 0.097249166106368,
             'depth': 10,
             'l2_leaf_reg': 0.9191504373151137,
             'iterations': 1000}

def train(file=None):
    if file is None:
        return {"error": "no file provided"}
    try:
        data_file = file.file
        logger.info("loading train data")
        data_train=pd.read_csv(data_file)
        validation = dataValidation(data_train)
        if not validation[0]:
            logger.error("data validation failed, columns missing: " + str(validation[1]))
            return {"error": "data validation failed, columns missing: " + str(validation[1])}
        logger.info("cleaning data")
        data_train = clean_data(data_train)
        model=CatBoostRegressor(**h_param,verbose=0)
        X=data_train.drop(["trip_duration"],axis=1)
        y=data_train["trip_duration"]
        logger.info("fitting model")
        model.fit(X,y)
        name = f"model_{time.time()}.cbm"
        model.save_model(f"app/models/{name}")
        logger.info(f"saving model to {name}")
        return {"success": name}
    except Exception as e:
        logger.error(e)
        logger.error("something went wrong")
        return {"error": "something went wrong"}