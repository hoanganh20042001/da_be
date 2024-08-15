
from pydantic import BaseModel
from typing import List

class Prediction(BaseModel):
    label: int
    bbox: List[float]
    accuracy: float

class PredictionsResponse(BaseModel):
    predictions: List[Prediction]
    detected_image_path: str
