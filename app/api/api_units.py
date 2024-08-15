import logging
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi_sqlalchemy import db

from app.helpers.exception_handler import CustomException
from app.helpers.login_manager import login_required, PermissionRequired
from app.helpers.paging import Page, PaginationParams, paginate
from app.schemas.sche_base import DataResponse
from app.schemas.sche_units import UnitsItemResponse, UnitsCreateRequest,  UnitsUpdateRequest
from app.services.srv_units import UnitsService
from app.models import Units

logger = logging.getLogger()
router = APIRouter()


@router.get("", dependencies=[Depends(login_required)], response_model=Page[UnitsItemResponse])
def get(params: PaginationParams = Depends()) -> Any:
    """
    API Get list Units
    """
    try:
        _query = db.session.query(Units)
        if params.search_text:
            _query = _query.filter(Units.name.ilike(f"%{params.search_text}%"))
        units = paginate(model=Units, query=_query, params=params)
        return units
    except Exception as e:
        return HTTPException(status_code=400, detail=logger.error(e))


@router.post("", dependencies=[Depends(login_required)], response_model=DataResponse[UnitsItemResponse])
def create(unit_data: UnitsCreateRequest, Units_service: UnitsService = Depends()) -> Any:
    """
    API Create Units
    """
    try:
        new_unit = Units_service.create(unit_data)
        return DataResponse().success_response(data=new_unit)
    except Exception as e:
        raise CustomException(http_code=400, code='400', message=str(e))


@router.get("/{unit_id}", dependencies=[Depends(login_required)], response_model=DataResponse[UnitsItemResponse])
def detail(unit_id: int, Units_service: UnitsService = Depends()) -> Any:
    """
    API get Detail Units
    """
    try:
        return DataResponse().success_response(data=Units_service.get(unit_id))
    except Exception as e:
        raise CustomException(http_code=400, code='400', message=str(e))


@router.put("/{unit_id}", dependencies=[Depends(login_required)],
            response_model=DataResponse[UnitsItemResponse])
def update(unit_id: int, Units_data: UnitsUpdateRequest, Units_service: UnitsService = Depends()) -> Any:
    """
    API update Units
    """
    try:
        updated_Units = Units_service.update(disease_id=unit_id, data=Units_data)
        return DataResponse().success_response(data=updated_Units)
    except Exception as e:
        raise CustomException(http_code=400, code='400', message=str(e))
