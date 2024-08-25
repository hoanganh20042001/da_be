import logging
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi_sqlalchemy import db

from app.helpers.exception_handler import CustomException
from app.helpers.login_manager import login_required, PermissionRequired
from app.helpers.paging import Page, PaginationParams, paginate
from app.schemas.sche_base import DataResponse
from app.schemas.sche_patients import PatientsItemResponse, PatientsCreateRequest,  PatientsUpdateRequest
from app.services.srv_patients import PatientsService
from app.models import Patients

logger = logging.getLogger()
router = APIRouter()


@router.get("", dependencies=[Depends(login_required)], response_model=Page[PatientsItemResponse])
def get(params: PaginationParams = Depends()) -> Any:
    """
    API Get list Patients
    """
    try:
        _query = db.session.query(Patients)
        if params.search_text:
            _query = _query.filter(Patients.full_name.ilike(f"%{params.search_text}%"))
        Patientss = paginate(model=Patients, query=_query, params=params)
        return Patientss
    except Exception as e:
        return HTTPException(status_code=400, detail=logger.error(e))


@router.post("", dependencies=[Depends(login_required)], response_model=DataResponse[PatientsItemResponse])
def create(patient_data: PatientsCreateRequest, patients_service: PatientsService = Depends()) -> Any:
    """
    API Create Patients
    """
    try:
        new_patient = patients_service.create(patient_data)
        return DataResponse().success_response(data=new_patient)
    except Exception as e:
        raise CustomException(http_code=400, code='400', message=str(e))


@router.get("/{patient_id}", dependencies=[Depends(login_required)], response_model=DataResponse[PatientsItemResponse])
def detail(patient_id: int, patients_service: PatientsService = Depends()) -> Any:
    """
    API get Detail Patients
    """
    try:
        return DataResponse().success_response(data=patients_service.get(patient_id))
    except Exception as e:
        raise CustomException(http_code=400, code='400', message=str(e))


@router.put("/{patient_id}", dependencies=[Depends(login_required)],
            response_model=DataResponse[PatientsItemResponse])
def update(patient_id: int, patients_data: PatientsUpdateRequest, patients_service: PatientsService = Depends()) -> Any:
    """
    API update Patients
    """
    try:
        updated_Patients = patients_service.update(patient_id=patient_id, data=patients_data)
        return DataResponse().success_response(data=updated_Patients)
    except Exception as e:
        raise CustomException(http_code=400, code='400', message=str(e))


@router.delete("/{patient_id}", dependencies=[Depends(PermissionRequired('A'))],
            response_model=DataResponse[PatientsItemResponse])
def delete(patient_id: int, patient_service: PatientsService = Depends()) -> Any:
    """
    API update User
    """
    try:
        delete_patient = patient_service.delete(id=patient_id)
        return DataResponse().success_response(data=delete_patient)
    except Exception as e:
        raise CustomException(http_code=400, code='400', message=str(e))
    
@router.get("/get_by_cccd/{cccd}", dependencies=[Depends(login_required)], response_model=DataResponse[PatientsItemResponse])
def getByCccd(cccd: str, patients_service: PatientsService = Depends()) -> Any:
    """
    API get Detail Patients
    """
    try:
        logger.info(cccd)
        return DataResponse().success_response(data=patients_service.getByCccd(cccd))
    except Exception as e:
        raise CustomException(http_code=400, code='400', message=str(e))
