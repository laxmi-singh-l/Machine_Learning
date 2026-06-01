from operator import gt
from fastapi import FastAPI
from pydantic import BaseModel, Field, computed_field
from typing import Literal , Annotated
import pickle
import pandas as pd
from starlette.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

# ----------------------------------------
# import ml model (load safely and provide helpful error if sklearn is missing)
# ----------------------------------------
model = None
try:
    with open("pridict_model.pkl", "rb") as f:
        model = pickle.load(f)
except ModuleNotFoundError as e:
    model = None
    missing = getattr(e, "name", str(e))
    print(f"Model load failed: missing module {missing}. Install scikit-learn in the environment.")
except Exception as e:
    model = None
    print("Model load failed:", e)


app = FastAPI()

tier_1_cities = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune"]
tier_2_cities = [
"Jaipur", "Chandigarh", "Indore", "Lucknow", "Patna", "Ranchi", "Visakhapatnam", "Coimbatore", "Bhopal", "Nagpur", "Vadodara", "Surat", "Rajkot", "Jodhpur", "Raipur", "Amritsar", "Varanasi", "Agra", "Dehradun", "Mysore", "Jabalpur", "Guwahati", "Thiruvananthapuram", "Ludhiana", "Nashik", "Allahabad", "Udaipur", "Aurangabad", "Hubli", "Belgaum", "Salem", "Vijayawada", "Tiruchirappalli", "Bhavnagar", "Gwalior", "Dhanbad", "Bareilly", "Aligarh", "Gaya", "Kozhikode", "Warangal", "Kolhapur",
                  "Bilaspur", "Jalandhar", "Noida",
                  "Guntur", "Asansol", "Siliguri"
]


# pydantic model to validate incoming data

class UserInput(BaseModel):
    age:Annotated[int, Field(..., gt=1, description="Age in years")]
    weight:Annotated[float, Field(..., gt=0, description="Weight in kg")]
    height:Annotated[float, Field(..., gt=0, description="Height in m")]
    income_lpa: Annotated[float , Field(..., gt=0, description="Income in lpa")]
    smoker:Annotated[bool, Field(..., description="Smoker or not")]
    city:Annotated[str, Field(..., min_length=1, description="City")]
    occupation: Annotated[Literal['retired', 'unemployed', 'business owner', 'government job', 'student', 'freelancer', 'private job'], Field(..., description='your work occupation')]
# using literal-> for giving options

    @computed_field
    def bmi(self) -> float:
        return round(self.weight / (self.height ** 2), 2)

    @computed_field
    def age_group(self) -> str:
        if self.age < 25:
            return "young"
        elif self.age < 45:
            return 'adult'
        elif self.age < 60:
            return "middle_aged"
        return 'senior'

    @computed_field
    def lifestyle_risk(self) -> str:
        if self.smoker and self.bmi > 30:
            return "high"
        elif self.smoker or self.bmi > 27:
            return "medium"
        else:
            return "low"
        

    @computed_field
    
    def city_tier(self) -> int:
        if self.city in tier_1_cities:
            return 1
        elif self.city in tier_2_cities:
            return 2
        else:
            return 3




# with the help of this we can allow all origins to access our API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # frontend origin
    allow_credentials=True,
    allow_methods=["*"],   # allows OPTIONS
    allow_headers=["*"],
)


@app.post("/predict")
async def predict(data: UserInput):


    # input that will be going to model
    input_df = pd.DataFrame([{
        'bmi': data.bmi,
        'age_group': data.age_group,
        'income_lpa': data.income_lpa,
        'city_tier': data.city_tier,
        'occupation': data.occupation

    }])
    if model is None:
        return JSONResponse(
            status_code=500,
            content={
                "error": "Model not loaded. Ensure scikit-learn is installed in the environment (pip install scikit-learn)."
            },
        )

    raw_pred = model.predict(input_df)[0]
    try:
        # convert numpy types to native python types if needed
        pred = raw_pred.item()
    except Exception:
        pred = raw_pred

    return JSONResponse(status_code=200, content={"prediction": pred})
