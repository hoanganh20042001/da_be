import logging
from typing import Any, Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi_sqlalchemy import db
from sqlalchemy import func, or_, and_
import math
from app.helpers.exception_handler import CustomException
from app.helpers.login_manager import login_required, PermissionRequired
from app.helpers.paging import Page, PaginationParams, paginate, MetadataSchema
from app.schemas.sche_base import DataResponse
from app.schemas.sche_patients import PatientsItemResponse, PatientsCreateRequest,  PatientsUpdateRequest
from app.services.srv_patients import PatientsService
from app.models import Patients, Units, Checks

logger = logging.getLogger()
router = APIRouter()


@router.get("",
            # dependencies=[Depends(login_required)],
            response_model=Any)
def get(status: Optional[int]=0,params: PaginationParams = Depends()) -> Any:
    """
    API Get list Patients
    """
    try:
        subquery = (
        db.session.query(
            Checks.patient_id,
            func.max(Checks.time).label('latest_time')
        )
        .group_by(Checks.patient_id)
        .subquery()
        )
        _query =( db.session.query(Patients, Units, Checks)
        .outerjoin(Units, Patients.unit_id == Units.id)
        .outerjoin(subquery, subquery.c.patient_id == Patients.id)
        .outerjoin(Checks, and_(Checks.patient_id == Patients.id, Checks.time == subquery.c.latest_time)))
        
        if status == 1:
            _query = _query.filter(Checks.result != None)  # Trường hợp có kết quả
        elif status == 2:
            _query = _query.filter(or_(Checks == None, Checks.result == None))  # Không có kiểm tra hoặc chưa có kết quả
        elif status == 3:
            _query = _query.filter(and_(Checks != None, Checks.result == False))  # Có bảng Checks và kết quả False (âm tính)
        elif status == 4:
            _query = _query.filter(and_(Checks != None, Checks.result == True))

        if params.search_text:
            _query = _query.filter(Patients.full_name.ilike(f"%{params.search_text}%"))
        total = db.session.query(func.count()).select_from(_query.subquery()).scalar()

    # Thực hiện phân trang
        paginated_query = (_query.limit(params.page_size).offset(params.page_size * (params.page - 1)))
    
    # Lấy dữ liệu phân trang
        checks = paginated_query.all()
    
    # Nếu không có kết quả, ném ra lỗi 404
        if not checks:
            logger.error("Check not found")
            raise HTTPException(status_code=404, detail="Check not found")
    
    # Chuẩn bị danh sách kết quả
        result_list = [
        {
            'id': check[0].id,
            'full_name': check[0].full_name,
            'identification': check[0].identification,
            'date_birth': check[0].date_birth,
            'sex': check[0].sex,
            'phone_number': check[0].phone_number,
            'unit_id':check[0].unit_id,
            'unit_name':check[1].name,
            'resident':check[0].resident,
            'home_town':check[0].home_town,
            'medical_history':check[0].medical_history,
            'blood_group':check[0].blood_group,
            'height':check[0].height,
            'weight':check[0].weight,
            'rank':check[0].rank,
            'email':check[0].email,
            'position':check[0].position,
            'image_1':check[2].image_1 if len(check) > 2 and check[2] else None,
            'image_2':check[2].image_2 if len(check) > 2 and check[2] else None,
            'check_id':check[2].id if len(check) > 2 and check[2] else None,
            'description':check[2].description if len(check) > 2 and check[2] else None,
            'date':check[2].date if len(check) > 2 and check[2] else None,
            'time':check[2].time if len(check) > 2 and check[2] else None,
            'result':check[2].result if len(check) > 2 and check[2] else None,
            'status':check[2].status if len(check) > 2 and check[2] else None,
        }
            for check in checks
        ]
    
    # Tính metadata cho phân trang
        metadata = MetadataSchema(
            current_page=params.page,
            page_size=params.page_size,
            total_items=total,
            total_pages=math.ceil(total / params.page_size)
        )
    
    # Trả về kết quả với dữ liệu và metadata
        response_data = {
            'data': result_list,
            'metadata': metadata
        }
        return DataResponse().success_response(response_data)
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

@router.get("/search_text/{cccd}", dependencies=[Depends(login_required)],response_model=Any)
def get(cccd: str) -> Any:
    """
    API Get list Patients
    """
    try:
        _query = db.session.query(Patients.identification).filter(Patients.identification.like(f"{cccd}%")).all()
        cccd_list = [item.identification for item in _query] 
        return DataResponse().success_response(cccd_list)
    except Exception as e:
        return HTTPException(status_code=400, detail=logger.error(e))
    
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
    print(cccd)
    try:
        logger.info(cccd)
        return DataResponse().success_response(data=patients_service.getByCccd(cccd))
    except Exception as e:
        raise CustomException(http_code=400, code='400', message=str(e))
