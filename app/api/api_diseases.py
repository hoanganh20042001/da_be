import logging
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi_sqlalchemy import db

from app.helpers.exception_handler import CustomException
from app.helpers.login_manager import login_required, PermissionRequired
from app.helpers.paging import Page, PaginationParams, paginate
from app.schemas.sche_base import DataResponse
from app.schemas.sche_diseases import DiseasesItemResponse, DiseasesCreateRequest,  DiseasesUpdateRequest
from app.services.srv_diseases import DiseasesService
from app.models import Diseases

logger = logging.getLogger()
router = APIRouter()


@router.get("", dependencies=[Depends(login_required)], response_model=Page[DiseasesItemResponse])
def get(params: PaginationParams = Depends()) -> Any:
    """
    API Get list Diseases
    """
    try:
        _query = db.session.query(Diseases)
        if params.search_text:
            _query = _query.filter(Diseases.name.ilike(f"%{params.search_text}%"))
        diseases = paginate(model=Diseases, query=_query, params=params)
        return diseases
    except Exception as e:
        return HTTPException(status_code=400, detail=logger.error(e))


@router.post("", dependencies=[Depends(login_required)], response_model=DataResponse[DiseasesItemResponse])
def create(disease_data: DiseasesCreateRequest, Diseases_service: DiseasesService = Depends()) -> Any:
    """
    API Create Diseases
    """
    try:
        new_disease = Diseases_service.create(disease_data)
        return DataResponse().success_response(data=new_disease)
    except Exception as e:
        raise CustomException(http_code=400, code='400', message=str(e))


@router.get("/{disease_id}", dependencies=[Depends(login_required)], response_model=DataResponse[DiseasesItemResponse])
def detail(disease_id: int, Diseases_service: DiseasesService = Depends()) -> Any:
    """
    API get Detail Diseases
    """
    try:
        return DataResponse().success_response(data=Diseases_service.get(disease_id))
    except Exception as e:
        raise CustomException(http_code=400, code='400', message=str(e))


@router.put("/{disease_id}", dependencies=[Depends(login_required)],
            response_model=DataResponse[DiseasesItemResponse])
def update(disease_id: int, Diseases_data: DiseasesUpdateRequest, Diseases_service: DiseasesService = Depends()) -> Any:
    """
    API update Diseases
    """
    try:
        updated_Diseases = Diseases_service.update(disease_id=disease_id, data=Diseases_data)
        return DataResponse().success_response(data=updated_Diseases)
    except Exception as e:
        raise CustomException(http_code=400, code='400', message=str(e))
