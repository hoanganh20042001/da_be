from sqlalchemy import Column, String, Boolean, DateTime, Integer

from app.models.model_base import BareBaseModel


class Patients(BareBaseModel):
    full_name = Column(String, index=True)
    phone_number = Column(String(10), unique=True, index=True)
    resident = Column(String(255))
    home_town = Column(String(255))
    medical_history = Column(String)
    is_active = Column(Boolean, default=True)
    sex= Column(Boolean, default=True)
    identification = Column(String(12))
    blood_group=Column(String(3))
    height=Column(Integer)
    weight=Column(Integer)
    date_birth=Column(DateTime)
    unit_id = Column(Integer)
    rank = Column(String)