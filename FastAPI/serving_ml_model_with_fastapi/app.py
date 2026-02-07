from sre_constants import LITERAL
from fastapi import FastAPI 
from pydantic import BaseModel, Field, computed_field 
from typing import Annotated ,Literal
import pickle
import pandas as pd
 
#  import ml model
with open('model.pkl','rb') as f:
    model = pickle.load(f)


app = FastAPI()

tier_1_cities = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune"]
tier_2_cities = [
"Jaipur", "Chandigarh", "Indore", "Lucknow", "Patna", "Ranchi", "Visakhapatnam", "Coimbatore", "Bhopal", "Nagpur", "Vadodara", "Surat", "Rajkot", "Jodhpur", "Raipur", "Amritsar", "Varanasi", "Agra", "Dehradun", "Mysore", "Jabalpur", "Guwahati", "Thiruvananthapuram", "Ludhiana", "Nashik", "Allahabad", "Udaipur", "Aurangabad", "Hubli", "Belgaum", "Salem", "Vijayawada", "Tiruchirappalli", "Bhavnagar", "Gwalior", "Dhanbad", "Bareilly", "Aligarh", "Gaya", "Kozhikode", "Warangal", "Kolhapur",
                  "Bilaspur", "Jalandhar", "Noida",
                  "Guntur", "Asansol", "Siliguri"
]


#  pydantivc model to validate incomng data

class incoming_data(BaseModel):

    selfage: Annotated[int,Field(..., gt= 1,lt=100)]
    weight:Annotated[float,Field(..., gt=10,description= 'provide your weight')]
    height: Annotated[float , Field(description='provide height in meter ')]
    income_lpa: Annotated[float, Field(description='details about your income in lakhs', gt = .1)]
    smoker: Annotated[bool, Field(description='tell that you are smoker or not', examples=['True', 'False'])]
    city:Annotated[str , Field(...,)]
    occupation: Annotated[Literal['retired', 'unemployed', 'bussiness owner', 'government job','student', 'freelancer','private job'], Field(description='your work occupation' )]


@computed_field
@property
def bmi(self) -> float:
    return round(self.weight/(self.height**2),2)

@computed_field
@property
def age_group(self) -> str:
    if self.age < 25:
        return "young"

    elif self.age < 45:
        return 'adult'

    elif self.age < 60:
        return "middle_aged"

    return 'senior'


@computed_field
@property
def lifestyle_risk(self) -> str:
    if self.row["smoker"] and self.row["bmi"] > 30:
        return "high"
    elif self.row["smoker"] or self.row["bmi"] > 27:
        return "medium"
    else:
        return "low"

@computed_field
@property
def city_tier(city):
  if city in tier_1_cities:
    return 1
  elif city in tier_2_cities:
    return 2

  else:
    return 3
  

@app.post('/predict')

    
