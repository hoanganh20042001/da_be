import jwt
from datetime import datetime
from typing import Optional
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from fastapi_sqlalchemy import db
from pydantic import ValidationError
from starlette import status

from app.models import Patients
from app.core.config import settings
from app.core.security import verify_password, get_password_hash
from app.schemas.sche_token import TokenPayload
from app.schemas.sche_patients import PatientsCreateRequest,PatientsItemResponse,PatientsUpdateRequest


class PatientsService(object):
    __instance = None

    def __init__(self) -> None:
        pass

    reusable_oauth2 = HTTPBearer(
        scheme_name='Authorization'
    )

    # @staticmethod
    # def authenticate(*, email: str, password: str) -> Optional[User]:
    #     """
    #     Check username and password is correct.
    #     Return object User if correct, else return None
    #     """
    #     user = db.session.query(User).filter_by(email=email).first()
    #     if not user:
    #         return None
    #     if not verify_password(password, user.hashed_password):
    #         return None
    #     return user

    # @staticmethod
    # def get_current_user(http_authorization_credentials=Depends(reusable_oauth2)) -> User:
    #     """
    #     Decode JWT token to get user_id => return User info from DB query
    #     """
    #     try:
    #         payload = jwt.decode(
    #             http_authorization_credentials.credentials, settings.SECRET_KEY,
    #             algorithms=[settings.SECURITY_ALGORITHM]
    #         )
    #         token_data = TokenPayload(**payload)
    #     except (jwt.PyJWTError, ValidationError):
    #         raise HTTPException(
    #             status_code=status.HTTP_403_FORBIDDEN,
    #             detail=f"Could not validate credentials",
    #         )
    #     user = db.session.query(User).get(token_data.user_id)
    #     if not user:
    #         raise HTTPException(status_code=404, detail="User not found")
    #     return user

    @staticmethod
    def create(data: PatientsCreateRequest):
        exist_patient = db.session.query(Patients).filter(Patients.identification == data.identification).first()
        if exist_patient:
            raise Exception('Identification already exists')
        new_patient = Patients(
            full_name=data.full_name,
            phone_number=data.phone_number,
            resident=data.resident,
            is_active=data.is_active,
            home_town=data.home_town,
            medical_history=data.medical_history,
            sex=data.sex,
            identification=data.identification,
            blood_group=data.blood_group,
            height=data.height,
            weight=data.weight,
            date_birth=data.date_birth

        )
        db.session.add(new_patient)
        db.session.commit()
        return new_patient

    # @staticmethod
    # def update_me(data: UserUpdateMeRequest, current_user: User):
    #     if data.email is not None:
    #         exist_user = db.session.query(User).filter(
    #             User.email == data.email, User.id != current_user.id).first()
    #         if exist_user:
    #             raise Exception('Email already exists')
    #     current_user.full_name = current_user.full_name if data.full_name is None else data.full_name
    #     current_user.email = current_user.email if data.email is None else data.email
    #     current_user.hashed_password = current_user.hashed_password if data.password is None else get_password_hash(
    #         data.password)
    #     db.session.commit()
    #     return current_user

    @staticmethod
    def update(patient_id: int, data: PatientsUpdateRequest):
        patient = db.session.query(Patients).get(patient_id)
        if patient is None:
            raise Exception('patient not exists')
        patient.full_name = patient.full_name if data.full_name is None else data.full_name
        patient.home_town = patient.home_town if data.home_town is None else data.home_town
        patient.resident= patient.resident if data.resident is None else data.resident
        patient.medical_history = patient.medical_history if data.medical_history is None else data.medical_history
        patient.sex = patient.sex if data.sex is None else data.sex
        patient.blood_group = patient.blood_group if data.blood_group is None else data.blood_group
        patient.height = patient.height if data.height is None else data.height
        patient.weight = patient.weight if data.weight is None else data.weight
        patient.phone_number = patient.phone_number if data.phone_number is None else data.phone_number
        patient.date_birth = patient.date_birth if data.date_birth is None else data.date_birth
        patient.is_active = patient.is_active if data.is_active is None else data.is_active
        db.session.commit()
        return patient

    @staticmethod
    def get(patient_id):
        exist_patient = db.session.query(Patients).get(patient_id)
        if exist_patient is None:
            raise Exception('patient not exists')
        return exist_patient
