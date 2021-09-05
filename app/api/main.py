import joblib, json
from typing import List

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from pydantic import BaseModel

app = FastAPI()

base_dir = 'api'

with open(base_dir + '/' + 'meta.json', 'r') as fp:
    meta = json.load(fp)

model = joblib.load(base_dir + '/' + 'model/model.joblib')

class FeatureSet(BaseModel):
    x1: float
    x2: float
    x3: float

    class Config:
        schema_extra = {
            "example": {
                "x1": 0.81,
                "x2": 1.21,
                "x3": 0.05
            }
        }

@app.get("/about_model")
async def about_model():
    return meta

@app.post("/predict")
async def predict(features: List[FeatureSet]):
    feature_list = [list(d.dict().values()) for d in features]
    preds = {"prediction": model.predict(feature_list).tolist()}
    return preds

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=f"{meta['model_name']} Model API",
        version="1.0.0",
        description="Schema for model scoring endpoint",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi