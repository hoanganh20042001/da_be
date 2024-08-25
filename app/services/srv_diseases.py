import jwt
from datetime import datetime
from typing import Optional
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from fastapi_sqlalchemy import db
from pydantic import ValidationError
from starlette import status

from app.models import Diseases
from app.models import Checks
from app.core.config import settings
from app.schemas.sche_token import TokenPayload
from app.schemas.sche_diseases import DiseasesCreateRequest,DiseasesItemResponse,DiseasesUpdateRequest


class DiseasesService(object):
    __instance = None

    def __init__(self) -> None:
        pass

    reusable_oauth2 = HTTPBearer(
        scheme_name='Authorization'
    )


    @staticmethod
    def create(data: DiseasesCreateRequest):
        exist_disease = db.session.query(Diseases).filter(Diseases.name == data.name).first()
        if exist_disease:
            raise Exception('name already exists')
        new_disease = Diseases(
           name=data.name,
           name_E=data.name_E,
           symbol=data.symbol,
           description=data.description,
           reason=data.reason, 
           expression=data.expression,
           advice=data.advice
        )
        db.session.add(new_disease)
        db.session.commit()
        return new_disease


    @staticmethod
    def update(disease_id: int, data: DiseasesUpdateRequest):
        disease = db.session.query(Diseases).get(disease_id)
        if disease is None:
            raise Exception('disease not exists')
        disease.name = disease.name if data.name is None else data.name
        disease.name_E = disease.name_E if data.name_E is None else data.name_E
        disease.symbol = disease.symbol if data.symbol is None else data.symbol
        disease.description = disease.description if data.description is None else data.description
        disease.reason = disease.reasonn if data.reason is None else data.reason
        disease.expression = disease.expression if data.expression is None else data.expression
        disease.advice = disease.advice if data.advice is None else data.advice
        db.session.commit()
        return disease

    @staticmethod
    def get(disease_id):
        exist_disease = db.session.query(Diseases).get(disease_id)
        if exist_disease is None:
            raise Exception('disease not exists')
        return exist_disease

    @staticmethod
    def getByCheckId(check_id):
        exist_disease = db.session.query(Diseases).join(Checks).filter(Checks.id == check_id).first()
        if exist_disease is None:
            raise Exception('disease not exists')
        return exist_disease