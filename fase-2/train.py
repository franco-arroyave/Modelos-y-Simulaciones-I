import os
import math
import time
import argparse
from loguru import logger
import pandas as pd
from catboost import CatBoostRegressor
from tools import dataValidation, clean_data

h_param={'learning_rate': 0.097249166106368,
             'depth': 10,
             'l2_leaf_reg': 0.9191504373151137,
             'iterations': 1000}

def __main__():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_file', required=True, type=str, help='a csv file with train data')

    args = parser.parse_args()

    data_file  = args.data_file

    if os.path.exists(os.path.join('data', data_file)):

        logger.info("loading train data")

        data_train=pd.read_csv(os.path.join('data', data_file))
        validation = dataValidation(data_train)
        if not validation[0]:
            logger.error("data validation failed, columns missing: " + str(validation[1]))
            exit(-1)

        logger.info("cleaning data")
        data_train = clean_data(data_train)
        model=CatBoostRegressor(**h_param,verbose=0)
        X=data_train.drop(["trip_duration"],axis=1)
        y=data_train["trip_duration"]
        logger.info("fitting model")
        model.fit(X,y)
        name = f"models/model_{time.time()}.cbm"
        model.save_model(name)
        logger.info(f"saving model to {name}")

    else:
        logger.error(f"file {data_file} doesn't exist")
        exit()

if __name__ == "__main__":
    __main__()

#python train.py --data_file train.csv