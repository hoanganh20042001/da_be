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


class ChecksService(object):
    __instance = None

    def __init__(self) -> None:
        pass

    reusable_oauth2 = HTTPBearer(
        scheme_name='Authorization'
    )

    @staticmethod
    def get(check_id):
        exist_disease = db.session.query(Diseases).join(Checks).filter(Checks.id == check_id).first()
        if exist_disease is None:
            raise Exception('disease not exists')
        return exist_disease
    
    @staticmethod
    def update(check_id):
        exist_disease = db.session.query(Diseases).join(Checks).filter(Checks.id == check_id).first()
        if exist_disease is None:
            raise Exception('disease not exists')
        return exist_disease
    