from fastapi import FastAPI , Path , HTTPException, Query
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


# where we are recieving patient id as path parameter
# using path function for validation and documentation
# ..., means required parameter
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


# the path funvtion in fastapi is used to providee metadata , validation rules ,and documetation hints for path parameters in API endpoints
# title : A brief title for the path parameter
# description : A detailed description of the path parameter
# example : An example value for the path parameter
# ge: int = Path(..., title="The ID of the patient to get", description="This is the unique identifier for each patient", example=1)
# ge : greater than or equal to
# le : less than or equal to
# gt : greater than
# lt : less than than
# max_length : maximum length of the string
# min_length : minimum length of the string
# regex : regular expression to validate the string

# using path function for validation and documentation

@app.get("/patients/{id}/name")
def view_patient_name(id : str):
    data = load_data()

    if id in data:
        return {"name": data[id]["name"]}
    
    return {"error" : "patient not found"}
  

# FOR 404 not found error , for generating this mesage we need a custom class "HTTPException"
# order is optional parameter
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
