from sqlalchemy import Column, String, Boolean, DateTime, Integer

from app.models.model_base import BareBaseModel


class User(BareBaseModel):
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String(255))
    is_active = Column(Boolean, default=True)
    role_id = Column(String, default='S')  
    last_login = Column(DateTime)
    date_birth = Column(DateTime)
    unit_id = Column(Integer)
    rank = Column(String)
    position = Column(String)
    phone_number = Column(String(10), index=True)
    sex=Column(Boolean, default=True)
    deleted=Column(Boolean, default=False)