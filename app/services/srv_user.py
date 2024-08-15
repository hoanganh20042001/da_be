import jwt

from typing import Optional
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from fastapi_sqlalchemy import db
from pydantic import ValidationError
from starlette import status

from app.models import User
from app.core.config import settings
from app.core.security import verify_password, get_password_hash
from app.schemas.sche_token import TokenPayload
from app.schemas.sche_user import UserCreateRequest, UserUpdateMeRequest, UserUpdateRequest, UserRegisterRequest


class UserService(object):
    __instance = None

    def __init__(self) -> None:
        pass

    reusable_oauth2 = HTTPBearer(
        scheme_name='Authorization'
    )

    @staticmethod
    def authenticate(*, email: str, password: str) -> Optional[User]:
        """
        Check username and password is correct.
        Return object User if correct, else return None
        """
        user = db.session.query(User).filter_by(email=email).first()
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    @staticmethod
    def get_current_user(http_authorization_credentials=Depends(reusable_oauth2)) -> User:
        """
        Decode JWT token to get user_id => return User info from DB query
        """
        try:
            payload = jwt.decode(
                http_authorization_credentials.credentials, settings.SECRET_KEY,
                algorithms=[settings.SECURITY_ALGORITHM]
            )
            token_data = TokenPayload(**payload)
        except (jwt.PyJWTError, ValidationError):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Could not validate credentials",
            )
        user = db.session.query(User).get(token_data.user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    @staticmethod
    def register_user(data: UserRegisterRequest):
        exist_user = db.session.query(User).filter(User.email == data.email).first()
        if exist_user:
            raise Exception('Email already exists')
        register_user = User(
            full_name=data.full_name,
            email=data.email,
            hashed_password=get_password_hash(data.password),
            is_active=True,
            role=data.role.value,
            date_birth=data.date_birth,
            unit_id=data.unit_id,
            phone_number=data.phone_number,
            rank=data.rank,
            position=data.position
        )
        db.session.add(register_user)
        db.session.commit()
        return register_user

    @staticmethod
    def create_user(data: UserCreateRequest):
        exist_user = db.session.query(User).filter(User.email == data.email).first()
        if exist_user:
            raise Exception('Email already exists')
        new_user = User(
            full_name=data.full_name,
            email=data.email,
            hashed_password=get_password_hash(data.password),
            is_active=data.is_active,
            role=data.role.value,
            date_birth=data.date_birth,
            unit_id=data.unit_id,
            phone_number=data.phone_number,
            rank=data.rank,
            position=data.position
        )
        db.session.add(new_user)
        db.session.commit()
        return new_user

    @staticmethod
    def update_me(data: UserUpdateMeRequest, current_user: User):
        if data.email is not None:
            exist_user = db.session.query(User).filter(
                User.email == data.email, User.id != current_user.id).first()
            if exist_user:
                raise Exception('Email already exists')
        current_user.full_name = current_user.full_name if data.full_name is None else data.full_name
        current_user.email = current_user.email if data.email is None else data.email
        current_user.hashed_password = current_user.hashed_password if data.password is None else get_password_hash(
            data.password)
        current_user.date_birth = current_user.date_birth  if data.date_birth  is None else data.date_birth 
        current_user.sex = current_user.sex if data.sex is None else data.sex
        current_user.unit_id = current_user.unit_id if data.unit_id is None else data.unit_id
        current_user.rank = current_user.rank if data.rank is None else data.rank
        current_user.position = current_user.position if data.position is None else data.position
        db.session.commit()
        return current_user

    @staticmethod
    def update(user_id: int, data: UserUpdateRequest):
        user = db.session.query(User).get(user_id)
        if user is None:
            raise Exception('User not exists')
        user.full_name = user.full_name if data.full_name is None else data.full_name
        user.email = user.email if data.email is None else data.email
        user.hashed_password = user.hashed_password if data.password is None else get_password_hash(
            data.password)
        user.is_active = user.is_active if data.is_active is None else data.is_active
        user.role = user.role if data.role is None else data.role.value
        user.date_birth = user.date_birth  if data.date_birth  is None else data.date_birth 
        user.sex = user.sex if data.sex is None else data.sex
        user.unit_id = user.unit_id if data.unit_id is None else data.unit_id
        user.rank = user.rank if data.rank is None else data.rank
        user.position = user.position if data.position is None else data.position
        db.session.commit()
        return user

    @staticmethod
    def get(user_id):
        exist_user = db.session.query(User).get(user_id)
        if exist_user is None:
            raise Exception('User not exists')
        return exist_user
