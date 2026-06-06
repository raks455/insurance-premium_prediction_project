from pydantic import BaseModel,EmailStr,AnyUrl,Field,field_validator,model_validator,computed_field
from typing import List,Dict,Optional,Annotated

class Address(BaseModel):
    city:Annotated[str,Field(max_length=10,title="name of city",default="kathmandu")]
    houseNo:Annotated[int,Field(gt=0,title="House Number",Description="Mention here your description")]
class Patient(BaseModel):
    name:Annotated[str,Field(max_length=10,title="name of patient",description="give name of patient in ${max_length} characters",examples=["rakshya"])]
    linkedin_url:AnyUrl
    email:Annotated[Optional[EmailStr],Field(default="example@gmail.com",title="your email",description="give me your email")]
    age:Optional[int]=None
    weight:Annotated[float,Field(gt=0,lt=200,description="weight of patient in kg",strict=True)]
    height:Annotated[float,Field(gt=0,lt=300,description="height of patient in cm",strict=True)]
    married:Annotated[bool,Field(default=None,description="whether patient is married or not")]
    allergies:Annotated[Optional[List[str]],Field(default=None,description="List your allergies if any")]
    contact_details:Dict[str,str]
    address:Address
    
    @field_validator("email")
    @classmethod 
    def email_validator(cls,value):
        valid_domains=["hdfc.com","icici.com"]
        domain_name=value.split('@')[-1]
        if(domain_name not in valid_domains):
           raise ValueError("Not in valid domains")
        return value
        
    @field_validator("name",mode="after")
    @classmethod
    def transform_name(cls,value):
        return value.upper()
    @field_validator("age",mode='after')
    @classmethod
    def check_age(cls,value):
        if 0<value<100:
            
            return value
        else:
            raise ValueError("age should be between 0 and 100")
    @model_validator(mode='after')
    def validate_contact_method(cls,model):
        if model.age>60 and 'emergency' not in model.contact_details:
            raise ValueError("emeergency number required for age >60")
        return model
    
    @computed_field
    @property
    def bmi(self)->float:
        bmi=round(self.weight/(self.height)**2,2)
        return bmi
def insert(patient:Patient):
    print(patient.name)
    print(patient.email)
    print(patient.age)
    print(patient.bmi)
    print(patient.weight)
    print(patient.allergies)
    print(patient.linkedin_url)
    print(patient.address)
    print(patient.contact_details)
    print(patient.married)
    print("inserted")
address_dict={"city":"kathmandu","houseNo":1}
adress1=Address(**address_dict)
patient_info={"name":"rakshya","age":"30","height":2,"weight":23,"married":True,"contact_details":{"emergency":"9702053456"},"linkedin_url":"htp:www","address":adress1}

patient_1=Patient(**patient_info)
print(patient_1)
print(type(patient_1))
temp=patient_1.model_dump_json(exclude_unset=True)
print(temp)
print(type(temp))

