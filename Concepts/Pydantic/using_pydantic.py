# building pydantic model for patient data validation
from os import name
from pydantic import BaseModel, Field, ValidationError, conint
class Patient(BaseModel):
    name: str 
    age: int







def insert_patient_data(patient: Patient):

    print(patient.name)
    print(patient.age)
    print("Patient data inserted successfully.")


patient_info = {
    "name": "John Doe", 
    "age": 30
}

patient01 = Patient(**patient_info) # unpacking dictionary to match model fields
print(patient01)

insert_patient_data(patient01)
