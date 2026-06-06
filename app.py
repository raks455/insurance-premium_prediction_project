from fastapi import FastAPI
from pydantic import BaseModel, Field,computed_field
from fastapi.responses import JSONResponse
import pandas as pd
from typing import Literal,Annotated
import pickle

with open("model.pkl","rb") as f:
    model=pickle.load(f)

app=FastAPI()
tier_1_cities = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune"]
tier_2_cities = [
    "Jaipur", "Chandigarh", "Indore", "Lucknow", "Patna", "Ranchi", "Visakhapatnam", "Coimbatore",
    "Bhopal", "Nagpur", "Vadodara", "Surat", "Rajkot", "Jodhpur", "Raipur", "Amritsar", "Varanasi",
    "Agra", "Dehradun", "Mysore", "Jabalpur", "Guwahati", "Thiruvananthapuram", "Ludhiana", "Nashik",
    "Allahabad", "Udaipur", "Aurangabad", "Hubli", "Belgaum", "Salem", "Vijayawada", "Tiruchirappalli",
    "Bhavnagar", "Gwalior", "Dhanbad", "Bareilly", "Aligarh", "Gaya", "Kozhikode", "Warangal",
    "Kolhapur", "Bilaspur", "Jalandhar", "Noida", "Guntur", "Asansol", "Siliguri"
]
class UserInput(BaseModel):
    age:Annotated[int,Field(...,gt=0,lt=100)]
    height:Annotated[float,Field(...,gt=0,lt=2.5)]
    weight:Annotated[float,Field(...,gt=0)]
    income_lpa:Annotated[float,Field(...,gt=0)]
    smoker:Annotated[bool,Field(...)]
    city:Annotated[str,Field(...)]
    occupation:Annotated[Literal['private_job','government','self-employed','unemployed','retired','freelancer','student'],Field(...)]
    
    @computed_field
    @property 
    def bmi(self)->float:
        bmi=round(self.weight/(self.height)**2,2)
        return bmi
    
    @computed_field
    @property
    def lifestyle_risk(self)->str:
          if self.smoker and self.bmi > 30:
           return "high"
          elif self.smoker or self.bmi > 27:
           return "medium"
          else:
           return "low"
     
    @computed_field
    @property
    def age_group(self)->str:
        if self.age < 25:
         return "young"
        elif self.age < 45:
         return "adult"
        elif self.age < 60:
         return "middle_aged"
        return "senior"
    
    @computed_field
    @property
    def city_tier(self)->int:
        if self.city in tier_1_cities:
            return 1
        elif self.city in tier_2_cities:
            return 2
        else:
            return 3
        
@app.post("/predict")
def predict_premium(data:UserInput):
  input_df =  pd.DataFrame([{
        'bmi':data.bmi,
        'age_group':data.age_group,
        'lifestyle_risk':data.lifestyle_risk,
        'city_tier':data.city_tier,
        'occupation':data.occupation,
        'income_lpa':data.income_lpa,
        
    }])
  prediction = model.predict(input_df)[0]
  return JSONResponse(status_code=200,content={"predicted category":prediction})