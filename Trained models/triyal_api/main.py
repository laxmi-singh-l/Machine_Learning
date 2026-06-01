from math import e
from fastapi.responses import JSONResponse
from fastapi import FastAPI , HTTPException , Path , Query
from h11 import Data
from matplotlib.font_manager import json_dump
from matplotlib.pylab import det
from numpy import info
from pydantic import BaseModel, Field, computed_field , fields
import json
from typing import Annotated, Optional


app = FastAPI

# class Student(BaseModel):
#
#     id : Annotated[str , Field(..., description="provide your ID ")]
#     name : Annotated[str, Field(..., description="provide your name")]
#     classes : Annotated[str , Field(..., description="...")]
#     section :
