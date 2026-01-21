from fastapi import FastAPI
import json

app = FastAPI()

def load_data():
    with open("patients.json","r") as f:
        data = json.load(f)
    return data
# define endpoint
@app.get("/")
def hello():
    return {'message':'patient management API'}
# To run the application, use the command:
# uvicorn main:app --reload


@app.get('/about')
def about():
    return {'message': 'A fully funtional API to manage your patient records'}


# end point
@app.get('/view')
def view():
    data =load_data()
    load_data()


    return data
