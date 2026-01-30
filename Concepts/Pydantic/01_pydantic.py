from unittest.util import _MAX_LENGTH
from pydantic import BaseModel, Field, EmailStr, AnyUrl , AnyHttpUrl, ValidationError
from typing import List , Dict , Optional

class Patient(BaseModel):
    name: str 
    age: int = Field(..., ge=0, le=110) 
     # age must be between 0 and 110
    weight : float
    married : Optional[bool] = False
    allergies : Optional[list[str]] = None = Field(max_length = 5)
    contact_details : dict[str, str]
    email : EmailStr
    url : AnyUrl
    website : Optional[AnyHttpUrl] = None



def insert_patient_data(patient: Patient):

    print(patient.name)
    print(patient.age)
    print("Patient data inserted successfully.")


patient_info = {    
    "name": "John Doe", 
    "email" : "laxmisingh@gmail.com",
    "url" : "https://www.example.com",
    "age": 30,
    "weight": 70.5,
    "married" : False,
    "allergies" : ["pollen","nuts"],
    "contact_details" : {
        "phone" : "123-456-6785",
    }



}


patient01 = Patient(**patient_info) 
print(patient01)   
insert_patient_data(patient01)
