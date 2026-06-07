from pydantic import BaseModel,Field
from typing import Dict

class PredictionResponse(BaseModel):
     predicted_category:str=Field(...,title="Predicted Category",
     description="The predicted category of the insurance premium",example="High"
     )
     confidence:float=Field(...,title="Confidence",
     description="The confidence level of the predicted category",example=0.8)
     class_probabilities:Dict[str,float]=Field(...,title="Class Probabilities",
     description="The probabilities of each class",example={"A":0.5,"B":0.5})