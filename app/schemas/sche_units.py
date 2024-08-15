from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr



class UnitsBase(BaseModel):
    name: Optional[str] = None

    class Config:
        orm_mode = True


class UnitsItemResponse(UnitsBase):
    id: int
    name: str
    symbol:str
    description:str

class UnitsCreateRequest(UnitsBase):
    name: str
    symbol:str
    description:str



class UnitsUpdateRequest(BaseModel):
    name: Optional[str]
    symbol:Optional[str]
    description:Optional[str]
