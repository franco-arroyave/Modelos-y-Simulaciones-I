import os
import time
import argparse
from loguru import logger
import pandas as pd
from catboost import CatBoostRegressor
from tools import dataValidation, clean_data

parser = argparse.ArgumentParser()
parser.add_argument('--data_file', required=True, type=str, help='a csv file with input data (no targets)')
parser.add_argument('--model_file', required=True, type=str, help='a pkl file with a model already stored (see train.py)')

args = parser.parse_args()

model_file = args.model_file
data_file = args.data_file

if not os.path.isfile(os.path.join('models', model_file)):
    logger.error(f"model file {model_file} does not exist")
    exit(-1)

if not os.path.isfile(os.path.join('data', data_file)):
    logger.error(f"input file {data_file} does not exist")
    exit(-1)
    
logger.info("loading input data")
data = pd.read_csv(os.path.join('data', data_file))

logger.info("cleaning input data")
validation = dataValidation(data)
if not validation[0]:
    if len(validation[1]) == 1 and validation[1][0] == 'trip_duration':
        data = data.drop(["trip_duration"],axis=1)
    else:
        logger.error("data validation failed, columns missing: " + str(validation[1]))
        exit(-1)
data = clean_data(data)

logger.info("loading model")
model = CatBoostRegressor()
model.load_model(os.path.join('models', model_file))
    
logger.info("making predictions")
preds = model.predict(data)
name = f"predictions_{time.time()}.csv"
logger.info(f"saving predictions to data/{name}")
pd.DataFrame(preds.reshape(-1,1), columns=['preds']).to_csv(os.path.join('data', name), index=False)

#python predict.py --data_file train.csv --model_file model.cbm