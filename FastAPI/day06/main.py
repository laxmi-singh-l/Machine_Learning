from math import e
from fastapi.responses import JSONResponse
from fastapi import FastAPI , HTTPException , Path
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


# @app.post('/create')
# def create_patient(patient: Patient):

#     # load existing data
#     data = load_data()

#     # check if the ptient already exists
#     if patient.id in data:
#         raise HTTPException(status_code=400, detail='patient alrady exits')

#     # new patient add to the database
#     # .model_dump() -> convert pydantic object into dictionary
#     data[patient.id] = patient.model_dump(exclude=["id"])

#     # again save into json file
#     save_data(data)
#     return JSONResponse(status_code=201 , content={"message": " patient created succesfully"})


@app.post("/create", status_code=201)
def create_patient(patient: Patient):
    data = load_data()

    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient already exists")

    data[patient.id] = patient.model_dump(exclude={"id"})
    save_data(data)

    return {"message": "Patient created successfully"}
