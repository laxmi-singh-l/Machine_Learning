from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Annotated
import json
import os

app = FastAPI()

DATA_FILE = "patients.json"


class Patient(BaseModel):
    id: Annotated[str, Field(..., examples=["P001", "P002"])]
    name: Annotated[str, Field(..., min_length=2, max_length=50)]
    age: Annotated[int, Field(..., ge=0, le=120)]
    blood_group: Annotated[str, Field(..., examples=["A+", "B-", "O+"])]
    status: Annotated[str, Field(..., examples=["Stable", "Critical"])]


def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_data(data: dict):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


@app.get("/")
def hello():
    return {"message": "Patient report system running"}


@app.post("/create", status_code=201)
def create_patient(patient: Patient):
    data = load_data()

    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient already exists")

    data[patient.id] = patient.model_dump(exclude={"id"})
    save_data(data)

    return {"message": "Patient created successfully"}
