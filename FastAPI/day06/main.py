from math import e
from fastapi.responses import JSONResponse
from fastapi import FastAPI , HTTPException , Path , Query
from h11 import Data
from matplotlib.font_manager import json_dump
from pydantic import BaseModel, Field, computed_field , fields
import json
from typing import Annotated



app = FastAPI()

class Patient(BaseModel):


    id : Annotated[str, Field(..., description="ID of the patient", examples=['P001', 'P002'])]
    name : Annotated[str, Field(..., min_length=2, max_length=50, description="Name of the patient", examples=['John Doe', 'Jane Smith'])]
    age : Annotated[int , Field(..., description="Age of patient", examples=[20, 40])]
    blood_group : Annotated[str, Field(..., description="Blood group of patient", examples=["A+", "B-", "O+"])]
    status: Annotated[str, Field(..., description="situation of patient")]
    # for bmi we can't directly get bmi so we are using computed_field()
    # @computed_field
    # @property
    # def bmi(self) -> float:
    #     bmi = round(self.weight/(self.height**2),2)

    # for verdict
    # @computed_field
    # @property
    # def verdict(self) -> str:

    #     if self.bmi < 18.5:
    #         return "underwaight"
    #     elif self.bmi < 25:
    #         return "normal"
    #     elif self.bmi < 30:
    #         return "normal"
    #     else:
    #         return "obese"


def load_data():
    with open("patients.json", "r") as f:
        data =  json.load(f)

    return data



def save_data(data : dict):
    with open("patients.json" , "w") as f:
        json.dump(data, f)


@app.get("/")
def hello():
    return "hello this is a report fiel of patients"

@app.get("/patients/{id}")
def view_patient(id: str = Path(..., title="The ID of the patient to get", description="This is the unique identifier for each patient", example=1)):
    data = load_data()

    if id in data:
        return data[id]


    raise HTTPException(status_code=404 , detail="patient not found")


@app.get("/patients/{id}/status")
def view_patient_status(id: str):
    data = load_data()

    if id in data:
        return {"status": data[id]["status"]}

    return {"error": "patient not found"}



@app.get("/patients/{id}/name")
def view_patient_name(id : str):
    data = load_data()

    if id in data:
        return {"name": data[id]["name"]}

    return {"error" : "patient not found"}


@app.get('/sort')
def sort_patients(sort_by: str = Query(..., description='sort on the basis of height ,  weight or bmi'), order: str = Query('asc' , description='sort in asc or desc order')):

    valid_fields = ['age','weight','bmi']
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400 , detail=f'Invalid field select from {valid_fields}')

    if order not in ['asc','desc']:
        raise HTTPException(status_code=400, detail='Invalid order select between asc and desc')

    data =load_data()

    sort_order = True if order=='desc' else False

    # showing data so that it sort
    # DBMS sorting code " sorted(my_dict.values(), key = lambda x:x.get('height', 0), reverse = true)"
    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by,0), reverse=sort_order)
    return sorted_data




@app.post("/create", status_code=201)
def create_patient(patient: Patient):
    # load existing data
    data = load_data()

    # check if the patent already exist or not
    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient already exists")

    # nwe patient add to database
     # .model_dump() -> convert pydantic object into dictionary

    data[patient.id] = patient.model_dump(exclude={"id"})

    # again save data  into json file
    save_data(data)

    return {"message": "Patient created successfully"}

