from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr



class DiseasesBase(BaseModel):
    name: Optional[str] = None
    name_E: Optional[str] = None

    class Config:
        orm_mode = True


class DiseasesItemResponse(DiseasesBase):
    id: int
    name: str
    name_E: str
    symbol:str
    description:str

class DiseasesCreateRequest(DiseasesBase):
    name: str
    name_E: str
    symbol:str
    description:str



class DiseasesUpdateRequest(BaseModel):
    name: Optional[str]
    name_E: Optional[str]
    symbol:Optional[str]
    description:Optional[str]
