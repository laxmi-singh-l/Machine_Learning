from xmlrpc.client import boolean
from fastapi.responses import JSONResponse
from fastapi import FastAPI
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal
from pathlib import Path
import pickle
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware
# load ML model (safe)

with open('modell.pkl', 'rb') as f:
        model = pickle.load(f)


# pip uninstall scikit-learn -y
# pip install scikit-learn==1.6.1

app = FastAPI()

tier_1_cities = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune"]
tier_2_cities = [
"Jaipur", "Chandigarh", "Indore", "Lucknow", "Patna", "Ranchi", "Visakhapatnam", "Coimbatore", "Bhopal", "Nagpur", "Vadodara", "Surat", "Rajkot", "Jodhpur", "Raipur", "Amritsar", "Varanasi", "Agra", "Dehradun", "Mysore", "Jabalpur", "Guwahati", "Thiruvananthapuram", "Ludhiana", "Nashik", "Allahabad", "Udaipur", "Aurangabad", "Hubli", "Belgaum", "Salem", "Vijayawada", "Tiruchirappalli", "Bhavnagar", "Gwalior", "Dhanbad", "Bareilly", "Aligarh", "Gaya", "Kozhikode", "Warangal", "Kolhapur",
                  "Bilaspur", "Jalandhar", "Noida",
                  "Guntur", "Asansol", "Siliguri"
]


#  pydantivc model to validate incomng data

class incoming_data(BaseModel):

    age: Annotated[int, Field(..., gt=1, lt=100)]
    weight: Annotated[int, Field(..., description='provide your weight')]
    height: Annotated[float, Field(..., description='provide height in meter')]
    income_lpa: Annotated[int, Field(..., description='details about your income in lakhs')]
    smoker: Annotated[bool, Field(..., description='tell that you are smoker or not')]
    city: Annotated[str, Field(...)]
    occupation: Annotated[Literal['retired', 'unemployed', 'bussiness owner', 'government job', 'student', 'freelancer', 'private job'], Field(..., description='your work occupation')]

    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight / (self.height ** 2), 2)

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
        if self.smoker and self.bmi > 30:
            return "high"
        elif self.smoker or self.bmi > 27:
            return "medium"
        else:
            return "low"

    @computed_field
    @property
    def city_tier(self) -> int:
        if self.city in tier_1_cities:
            return 1
        elif self.city in tier_2_cities:
            return 2
        else:
            return 3
        


        

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # frontend origin
    allow_credentials=True,
    allow_methods=["*"],   # allows OPTIONS
    allow_headers=["*"],
)

      

@app.post('/predict')
def predict_premium(data : incoming_data):
    input_df = pd.DataFrame([{
        'bmi': data.bmi,
        'age_group': data.age_group,
        'lifestyle_risk': data.lifestyle_risk,
        'city_tier': data.city_tier,
        'income_lpa': data.income_lpa,
        'occupation': data.occupation,
    }])

    if model is None:
        return JSONResponse(status_code=500, content={'error': 'model.pkl not found or failed to load'})

    prediction = model.predict(input_df)[0]

    return JSONResponse(status_code=200, content={'predicted_category': prediction})
    
      