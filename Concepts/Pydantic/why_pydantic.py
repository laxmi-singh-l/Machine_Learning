# TYPE VALID_MODULE_NAMEATION WITHOUT PYDANTIC
from math import e
from typing import Type


def insert_patient_data(name : str, age : int):

    if type(name) == str and type(age) == int:
        if age < 0 or age > 110:
            raise ValueError("age must be between 0 and 110")
        else:
                  
            print(name)
            print(age)
            print("Patient data inserted successfully.")


    else:
        raise TypeError("name must be a string")

    # print(name)
    # print(age)

    # Here would be the logic to insert patient data into a database
# Example usage
insert_patient_data("John Doe", '30')

# in this case we are not validating the types of the inputs, which could lead to issues later on.
# This function lacks type validation, which can lead to runtime errors if incorrect types are passed.
# For example, passing a string for age instead of an integer would not raise an error here.
# A better approach would be to use a library like Pydantic to enforce type validation. 
def updated_patient_data(name : str, age : int):
    
    if name == str and age == int:
        if age < 0 or age > 110:
            raise ValueError("age must be between 0 and 110") 
        else:
            print(name)
            print(age)
            print("Patient data updatedsuccessfully.")

    else:
        raise TypeError("name must be a string and age must be an integer")        
