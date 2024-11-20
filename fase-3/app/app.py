import os
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import pandas as pd
from app.services import predict, train
from loguru import logger

app = FastAPI()

model_name = "model.cbm"

@app.post("/predict")
async def prediction(file: UploadFile = File(...)):
    output = predict.predict(file, model_name)
    if 'error' in output:
        return output
    return FileResponse(output['success'], media_type="application/octet-stream", filename=str.replace(output['success'], "app/data/", ""))

@app.post("/train")
async def train_model(file: UploadFile = File(...)):
    global model_name
    output = train.train(file)
    for k, v in output.items():
        if k == "success":
            model_name = v
    return output

@app.post("/setModel")
async def setModel(name: str = "model.cbm"):
    global model_name
    model_name = name
    return {"model": model_name}

@app.get("/models")
async def getModels():
    try:
        models = os.listdir("app/models")
        return {"actual": model_name, "models": models}
    except:
        return {"models": []}