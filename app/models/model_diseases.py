from sqlalchemy import Column, String, Boolean, DateTime, Integer

from app.models.model_base import BareBaseModel


class Diseases(BareBaseModel):
    name = Column(String, index=True)
    name_E = Column(String, index=True)
    symbol = Column(String)
    description = Column(String)  
    reason = Column(String)
    expression= Column(String)
    advice=Column(String)
