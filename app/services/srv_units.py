import jwt
from datetime import datetime
from typing import Optional
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from fastapi_sqlalchemy import db
from pydantic import ValidationError
from starlette import status

from app.models import Units
from app.core.config import settings
from app.schemas.sche_token import TokenPayload
from app.schemas.sche_units import UnitsCreateRequest,UnitsItemResponse,UnitsUpdateRequest


class UnitsService(object):
    __instance = None

    def __init__(self) -> None:
        pass

    reusable_oauth2 = HTTPBearer(
        scheme_name='Authorization'
    )


    @staticmethod
    def create(data: UnitsCreateRequest):
        exist_disease = db.session.query(Units).filter(Units.name == data.name).first()
        if exist_disease:
            raise Exception('name already exists')
        new_disease = Units(
           name=data.name,
           symbol=data.symbol,
           description=data.description

        )
        db.session.add(new_disease)
        db.session.commit()
        return new_disease


    @staticmethod
    def update(disease_id: int, data: UnitsUpdateRequest):
        disease = db.session.query(Units).get(disease_id)
        if disease is None:
            raise Exception('disease not exists')
        disease.name = disease.name if data.name is None else data.name
        disease.symbol = disease.symbol if data.symbol is None else data.symbol
        disease.description = disease.description if data.description is None else data.description

        db.session.commit()
        return disease

    @staticmethod
    def get(disease_id):
        exist_disease = db.session.query(Units).get(disease_id)
        if exist_disease is None:
            raise Exception('disease not exists')
        return exist_disease
