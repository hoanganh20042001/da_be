from sqlalchemy import Column, String, Boolean, DateTime, Integer

from app.models.model_base import BareBaseModel


class UserHistories(BareBaseModel):
    user_id = Column(String, index=True)
    user_agent = Column(String)
    time = Column(DateTime)
    method = Column(String(20))
    path = Column(String(255))
    status_code = Column(String(5))