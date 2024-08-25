
from pydantic import BaseModel
from typing import List

class Check(BaseModel):
    name: str
    name_E: str
    accuracy: float
    description:str
    reason:str
    expression:str
    advice: str