from sqlalchemy import Column, String, Boolean, DateTime, Integer

from app.models.model_base import BareBaseModel


class Checks(BareBaseModel):
    patient_id = Column(Integer, index=True)
    user_id = Column(Integer, index=True)
    image_1=Column(String)
    description = Column(String)  
    date= Column(DateTime)
    time=Column(Integer)
    result=Column(Boolean)
    image_2=Column(String)
    status=Column(Boolean, default=False)