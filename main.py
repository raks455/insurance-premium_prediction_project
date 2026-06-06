from fastapi import FastAPI,Path,HTTPException,Query
from typing import List,Dict,Annotated,Optional,Literal
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field,computed_field,field_validator
import json
app=FastAPI()

class Patient(BaseModel):
    id:Annotated[str,Field(...,description="Id of the patient in the DB",example="P001")]
    name:Annotated[str,Field(...,description="Name of the patient",example="Rakshya")]
    city:Annotated[str,Field(...,description="City of the patient",example="Kathmandu")]
    age:Annotated[int,Field(...,gt=0,lt=100,title="name",description="Age of Patient")]
    gender:Annotated[Literal["male","female","others"],Field(...,description="Gender of the patient",example="female")]
    height:Annotated[float,Field(...,gt=0,lt=300,title="Height",description="Height of the patient in cm")]
    weight:Annotated[float,Field(...,gt=0,lt=200,title="Weight",description="Weight of the patient in kg")]
   
    @computed_field
    @property
    def bmi(self)->float:
     bmi=round(self.weight/(self.height)**2,2)
     return bmi
    @computed_field
    @property
    def verdict(self)->str:
      if self.bmi<18:
         return "underweight"
      if self.bmi>25:
         return "overweight"
      return "normal"
class PatientUpdate(BaseModel):
   
    name:Annotated[Optional[str],Field(default=None,description="Name of the patient",example="Rakshya")]
    city:Annotated[Optional[str],Field(default=None,description="City of the patient",example="Kathmandu")]
    age:Annotated[Optional[int],Field(default=None,gt=0,lt=100,title="name",description="Age of Patient")]
    gender:Annotated[Optional[Literal["male","female","others"]],Field(default=None,description="Gender of the patient",example="female")]
    height:Annotated[Optional[float],Field(default=None,gt=0,lt=300,title="Height",description="Height of the patient in cm")]
    weight:Annotated[Optional[float],Field(default=None,gt=0,lt=200,title="Weight",description="Weight of the patient in kg")]
   
def load_data():
   with open("patients.json","r") as f:
    data=json.load(f)
    return data
def save_data(data):
   with open("patients.json","w") as f:
    json.dump(data,f)

    
@app.get("/")
def hello():
   return {"message": "Patient management system API"}

@app.get("/about")
def about():
  return {"message":"A fully functional patient management system"}

@app.get("/view")
def view():
    data=load_data()
    return data
#path parameters
@app.get("/patient/{patient_id}")
def view_patient(patient_id:str=Path(...,description="Id of the patient in the DB",example="P001")):
   data=load_data()
   if patient_id in data:
      return data[patient_id]
   raise HTTPException(status_code=404,detail="Patient not found")

#query parameters
@app.get("/sort")
def sort(sort_by:str=Query(...,description="Sort on the basis of height,weight or bmi"),order:str=Query('asc',description="Sort on ascending or descending order",)):
   valid_fields=["height","weight","bmi"]
   if sort_by not in valid_fields:
      raise HTTPException(status_code=400,detail=f"Invalid field select from {valid_fields}")
   asc_desc=["asc","desc"]
   if order not in asc_desc:
      raise HTTPException(status_code=400,detail=f"Invalid order select from {asc_desc}")
   data=load_data()
   sort_order=True if order=="desc" else False
   sorted_data=sorted(data.values(),key=lambda x:x.get(sort_by),reverse=sort_order)
   return sorted_data

@app.post("/create")
def add_patient(patient:Patient):
   data=load_data()
   if patient.id  in data:
      raise HTTPException(status_code=400,detail="Patient already exists")
   else:
      val=patient.model_dump(exclude="id")
      data[patient.id]=val
      save_data(data)
      return JSONResponse(content={"message":"Patient added successfully"},status_code=201)

@app.put("/update/{patient_id}")
def update_patient(patient_id:str,patient_update:PatientUpdate):
    data=load_data()
    if patient_id not in data:
     raise HTTPException(status=404,detail="patient not found")
    else:
     existing_patient_info=data[patient_id]
     updated_patient_info=patient_update.model_dump(exclude_unset=True)
     for key,value in updated_patient_info.items():
        
      existing_patient_info[key]=value
    existing_patient_info["id"]=patient_id
    patient_pydantic_object=Patient(**existing_patient_info)
    existing_patient_info=patient_pydantic_object.model_dump(exclude="id")
    data[patient_id]=existing_patient_info
    save_data(data)
    return JSONResponse(content={"message":"Patient updated successfully"},status_code=200)

@app.delete("/delete/{patient_id}")
def patient_delete(patient_id:str):
    data=load_data()
    if patient_id not in data:
       raise HTTPException(status=404,detail="Patient not found")
    else:
       del data[patient_id]
       save_data(data)
       return JSONResponse(content={"message":"Patient deleted successfully"},status_code=200)