import os
import time
from loguru import logger
import pandas as pd
from catboost import CatBoostRegressor
from app.utils.tools import dataValidation, clean_data

def predict(file, model_file):
    try:
        if not os.path.isfile(os.path.join('app/models', model_file)):
            logger.error(f"model file {model_file} does not exist")
            return {"error": f"model file {model_file} does not exist"}
        
        logger.info("loading input data")
        data = pd.read_csv(file.file)

        logger.info("cleaning input data")
        validation = dataValidation(data)

        if not validation[0]:
            if len(validation[1]) == 1 and validation[1][0] == 'trip_duration':
                data = data.drop(["trip_duration"],axis=1)
            else:
                logger.error("data validation failed, columns missing: " + str(validation[1]))
                return {"error": "data validation failed, columns missing: " + str(validation[1])}
        data = clean_data(data)

        logger.info("loading model")
        model = CatBoostRegressor()
        model.load_model(os.path.join('app/models', model_file))
        
        logger.info("making predictions")
        preds = model.predict(data)

        name = f"predictions_{time.time()}.csv"
        logger.info(f"saving predictions to data/{name}")
        df = pd.DataFrame(preds.reshape(-1,1), columns=['preds'])
        df.to_csv(os.path.join('app/data', name), index=False)
        location = 'app/data/'+name
        return {"success": location}

    except Exception as e:
        logger.error(e)
        logger.error("something went wrong")
        return {"error": "something went wrong"}

