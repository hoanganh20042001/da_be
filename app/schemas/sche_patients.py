from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr



class PatientsBase(BaseModel):
    full_name: Optional[str] = None
    identification: Optional[str] = None
    phone_number: Optional[str] = None
    is_active: Optional[bool] = True

    class Config:
        orm_mode = True


class PatientsItemResponse(PatientsBase):
    id: int
    full_name: str
    resident: str
    home_town: str
    medical_history: str = 'Không'
    identification: str
    blood_group: Optional[str]
    phone_number: str
    sex: bool
    is_active: bool
    height:int
    weight:int
    date_birth: Optional[datetime]
    deleted: bool
    # unit_name: str


class PatientsCreateRequest(PatientsBase):
    full_name: str
    resident: str
    home_town: str
    medical_history: str
    identification: str
    blood_group: str
    phone_number: str
    sex: bool= True
    is_active: bool =True
    height:int
    weight:int
    date_birth: Optional[datetime]
    deleted: bool=False


class PatientsUpdateRequest(BaseModel):
    full_name: str
    resident: str
    home_town: str
    medical_history: str
    identification: str
    blood_group: str
    phone_number: str
    sex: bool
    is_active: bool =True
    height:int
    weight:int
    date_birth: Optional[datetime]
    deleted: bool=False
