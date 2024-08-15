
from pydantic import BaseModel
from sqlalchemy import Column, String, Boolean, DateTime, Integer, Float
from typing import List
from app.models.model_base import BareBaseModel

class Prediction(BaseModel):
    label: int
    bbox: List[float]
    accuracy: float

class PredictionsResponse(BaseModel):
    predictions: List[Prediction]
    detected_image_path: str


class Results(BareBaseModel):
    check_id = Column(Integer)
    disease_id = Column(Integer)
    description = Column(String)  
    location= Column(String)
    content=Column(String)
    image=Column(String)
    accuracy=Column(Float)
   