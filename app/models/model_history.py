from sqlalchemy import Column, String, Boolean, DateTime, Integer

from app.models.model_base import BareBaseModel


class CheckItemResponse(BareBaseModel):
    id: int
    full_name: str
    date: str
    time: str
    unit: str

    class Config:
        orm_mode = True