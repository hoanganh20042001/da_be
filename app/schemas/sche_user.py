from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr

from app.helpers.enums import UserRole


class UserBase(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True

    class Config:
        orm_mode = True


class UserItemResponse(UserBase):
    id: int
    full_name: str
    email: EmailStr
    is_active: bool
    role_id: str
    last_login: Optional[datetime]
    phone_number:Optional[str]
    rank: Optional[str]
    position: Optional[str]
    unit_id :Optional[int]
    date_birth: Optional[datetime]
    sex: Optional[bool]
    

class UserCreateRequest(UserBase):
    full_name: Optional[str]
    password: str
    email: EmailStr
    is_active: bool = True
    role_id: UserRole = UserRole.STAFF
    phone_number:str
    rank: str
    position: str
    unit_id :int
    date_birth: datetime
    sex: bool
    deleted:bool=False

class UserRegisterRequest(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    role_id: UserRole = UserRole.STAFF
    phone_number:str
    rank: str
    position: str
    unit_id :int
    date_birth: datetime
    sex: bool
    
class UserUpdateMeRequest(BaseModel):
    full_name: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]
    phone_number:Optional[str]
    rank: Optional[str]
    position: Optional[str]
    unit_id :Optional[int]
    date_birth: Optional[datetime]
    sex: Optional[bool] 

class UserUpdateRequest(BaseModel):
    full_name: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]
    is_active: Optional[bool] = True
    role_id: Optional[UserRole]
    phone_number:Optional[str]
    rank: Optional[str]
    position: Optional[str]
    unit_id :Optional[int]
    date_birth: Optional[datetime]
    sex: Optional[bool] 
    deleted: Optional[bool] 