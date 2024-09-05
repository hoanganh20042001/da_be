from sqlalchemy import Column, String, Boolean, DateTime, Integer

from app.models.model_base import BareBaseModel


class Units(BareBaseModel):
    name = Column(String, index=True)
    symbol = Column(String)
    description = Column(String)  
    unit_father_id=Column(Integer)
   
