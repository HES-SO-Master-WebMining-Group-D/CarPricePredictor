from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import pandas as pd

app = FastAPI()

with open('models/xgbr_price_predictor.pkl', 'rb') as f:
    model = pickle.load(f)
with open('src/assets/feature_names.pkl', 'rb') as f:
    feature_names = pickle.load(f)


class PredictionRequest(BaseModel):
    input_data: dict


@app.post('/predict')
def predict(request: PredictionRequest):
    input_df = pd.DataFrame([request.input_data])
    input_df = pd.get_dummies(input_df).reindex(columns=feature_names, fill_value=0)
    prediction = model.predict(input_df)[0]
    return {"prediction": float(prediction)}
