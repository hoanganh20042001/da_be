
from pydantic import BaseModel
from typing import List
from typing import Optional
class Check(BaseModel):
    name: str
    name_E: str
    accuracy: float
    description:str
    reason:str
    expression:str
    advice: str
    
class CheckUpdateRequest(BaseModel):
    description: str
    result: Optional[bool] = True