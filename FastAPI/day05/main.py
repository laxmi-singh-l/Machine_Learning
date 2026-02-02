from math import e
from re import I
from fastapi import FastAPI , HTTPException , Path
from h11 import Data
from pydantic import BaseModel, Field , fields
import json
from typing import Annotated





app = FastAPI()

class Patient(BaseModel):


    id: Annotated[str, Field(..., description="ID of the patient", examples=['P001', 'P002'])]
    name : Annotated[str, Field(..., min_length=2, max_length=50, description="Name of the patient", examples=['John Doe', 'Jane Smith'])]
    age : Annotated[int , Field(..., description="Age of patient", examples=[20, 40])]
    blood_group : Annotated[str, Field(..., description="Blood group of patient", examples=["A+", "B-", "O+"])]
    status: Annotated[str, Field(..., description="situation of patient")]



def load_data():
    with open("patients.json", "r") as f:
        data =  json.load(f)

    return data    


@app.get("/")
def hello():
    return {"message": "patient management API"}



def insert_patient_data(patient: Patient):
    print(patient.id)


    print(patient.name)
    print(patient.age)
    print(patient.blood_group)
    print(patient.status)

    print("Patient data inserted successfully.")



patient_info = {    
   "id" : "P001",
   "name": "laxmi singh",
   "age": 20,
   "blood_group": "o+",
   "status" : "healing"
        

        
    } 


@app.get("/view")
def view():
    return load_data()


@app.get("/patients/{id}")
def view_info(id : Annotated[str, Field(..., description="Give your id number")]):
    data = load_data()

    if id in data:
        return data[id]
    
    raise HTTPException(status_code=404, detail="Patient is not found")

@app.get("/patient/{id}/status")
def view_status(id : Annotated[str, Field(..., description="condition of patients")]):
    data = load_data()

    if id in data:
        return {"status" : data[id]["status"]}
    
    
    return {"error" : "details not found"}


@app.get("/patients/{id}/name")
def view_name(id : str):
    data = load_data()

    if id in data:
        return
