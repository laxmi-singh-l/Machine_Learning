from fastapi import FastAPI , Path
import json

app = FastAPI()

def load_data():
    with open("patients.json", "r") as f:
        return json.load(f)

@app.get("/")
def hello():
    return {"message": "patient management API"}

@app.get("/about")
def about():
    return {"message": "A fully functional API to manage your patient records"}

@app.get("/view")
def view():
    return load_data()

@app.get("/patients/{id}")
def view_patient(id: str):
    data = load_data()

    if id in data:
        return data[id]

    return {"error": "patient not found"}


@app.get("/patients/{id}/status")
def view_patient_status(id: str):
    data = load_data()

    if id in data:
        return {"status": data[id]["status"]}

    return {"error": "patient not found"}
