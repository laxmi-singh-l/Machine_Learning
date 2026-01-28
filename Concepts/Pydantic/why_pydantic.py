# TYPE VALID_MODULE_NAMEATION WITHOUT PYDANTIC
def insert_patient_data(name : str, age : int):

    if type(name) == str and type(age) == int:
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
