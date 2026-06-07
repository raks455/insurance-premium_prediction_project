from fastapi import FastAPI
from fastapi.responses import JSONResponse
import pandas as pd
from model.predict import model,predict_output,MODEL_VERSION
from schema.user_input import UserInput
from schema.prediction_response import PredictionResponse
app=FastAPI()


@app.get("/")
def home():
    return {"message":"Insurance Premium Predicition API"} 

@app.get("/health")
def health():
   return{
       "status":"OK",
       "version":MODEL_VERSION,
       "model_loaded":model is not None
       
   } 
      
@app.post("/predict",response_model=PredictionResponse)
def predict_premium(data:UserInput):
  user_input =  {
        'bmi':data.bmi,
        'age_group':data.age_group,
        'lifestyle_risk':data.lifestyle_risk,
        'city_tier':data.city_tier,
        'occupation':data.occupation,
        'income_lpa':data.income_lpa,
        
    }
  try:
   prediction = predict_output(user_input)
   return JSONResponse(status_code=200,content={"response":prediction})
  except Exception as e:
   return JSONResponse(status_code=500,content={"error":str(e)})
      