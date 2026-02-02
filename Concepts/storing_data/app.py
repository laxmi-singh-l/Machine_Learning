from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, RedirectResponse
import json
import os

app = FastAPI()

DATA_FILE = "data.json"

@app.get("/", response_class=HTMLResponse)
def home():
    with open("index.html") as f:
        return f.read()

@app.post("/submit.html")
def submit(
    name: str ,
    age: int ,
    weight: int ,
    status: str ,
    blood_group: str 
):
    new_data = {
        "name": name,
        "age": age,
        "weight": weight,
        "status": status,
        "blood_group": blood_group
    }


    # agar file exist karti hai
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            all_data = json.load(f)
    else:
        all_data = []

    all_data.append(new_data)

    with open(DATA_FILE, "w") as f:
        json.dump(all_data, f, indent=4)

    return RedirectResponse("/", status_code=303)
