# Many more uses of Field function in Pydantic models

import email
from email.policy import strict
from unittest.util import _MAX_LENGTH
from pydantic import BaseModel, Field, EmailStr, AnyUrl , AnyHttpUrl, ValidationError
from typing import List , Dict , Optional, Annotated

class Patient(BaseModel):
    name: Annotated[str, Field(max_length=50 , title="Name of patients", description="Give name in 50 characters", examples =["laxmi","jane"])]
    age: int = Field(..., ge=0, le=110) # age must be between 0 and 110
    weight : Annotated[float, Field(gt = 0, description="Weight in kilograms" , strict=True)] #weight must be greater than 0
    married : Annotated[bool, Field(default=None, description= "Marital status of the patient")] = False
    allergies : Annotated[ Optional[list[str]],Field(max_length=5, description="List of allergies (max 5)")] = None
    contact_details : Annotated[dict[int, str], Field(description="Contact details with phone number as key")]
    email : EmailStr
    url : AnyUrl
    # website : Optional[AnyHttpUrl] = None
# field function is used to provide additional validation and metadata for model fields and to attach mata data to fields


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
        "phone" : "123-456-6785"
        

        
    } 

}




patient01 = Patient(**patient_info) 
print(patient01)   
insert_patient_data(patient01)

# Taking input from user for patient data

n = int(input("Total patients: "))
patients = {}


for i in range(7):
    pid = input("Patient ID: ")
    patients[pid] = {
        "name": str(input("Name: ")),
        "age": int(input("Age: ")),
        "weight": float(input("Weight: ")),
        "married": bool(input("Status: ")),
        "allergies": list(input("Allergies (comma separated): ").split(",")),
        "contact_details": {
            "phone": int(input("Phone: "))
        },
        "email": input("Email: "),
        "url": input("URL: ")

    }

print(patients)
