import logging
from typing import Any
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from fastapi_sqlalchemy import db
from sqlalchemy import func
import math
from app.helpers.exception_handler import CustomException
from app.helpers.login_manager import login_required, PermissionRequired
from app.helpers.paging import Page, PaginationParams, paginate,  MetadataSchema
from app.models import Diseases, Checks, Results, Patients, Units, User
from app.schemas.sche_base import DataResponse
from app.schemas.sche_checks import Check
logger = logging.getLogger()
router = APIRouter()
@router.get("", dependencies=[Depends(login_required)], response_model=Any)
def get(params: PaginationParams = Depends()) -> Any:
    # Tạo truy vấn cơ bản
    query = (
        db.session.query(Checks, Patients, Units, User)
        .join(Patients, Checks.patient_id == Patients.id)
        .join(Units, Patients.unit_id == Units.id)
        .join(User, Checks.user_id== User.id)
    )
    
    # Thực hiện lọc nếu có từ khóa tìm kiếm
    if params.search_text:
        query = query.filter(Patients.full_name.ilike(f"%{params.search_text}%"))

    # Tính tổng số bản ghi
    total = db.session.query(func.count()).select_from(
        query.subquery()
    ).scalar()

    # Thực hiện phân trang
    paginated_query = (
        query.limit(params.page_size).offset(params.page_size * (params.page - 1))
    )
    
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
            'full_name': check[1].full_name,
            'date': check[0].date,
            'time': check[0].time,
            'unit': check[2].name,
            'user':check[3].full_name
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


@router.get("/{check_id}", dependencies=[Depends(login_required)], response_model=Any)
def get(check_id: int) -> Any:
    """
    API Get list Diseases, Checks, and Results
    """
    try:
        checks = (
            db.session.query(Checks, Results, Diseases)
            .select_from(Checks)
            .join(Results, Results.check_id == Checks.id)
            .join(Diseases, Diseases.id == Results.disease_id)
            .filter(Checks.id == check_id)
            .all()  # Lấy tất cả các kết quả phù hợp
        )
        
        if not checks:
            raise HTTPException(status_code=404, detail="Check not found")
        result_list = [
            {
                'id':check[0].id,
                'name':check[2].name,
                'name_E':check[2].name_E,
                'accuracy':check[1].accuracy,
                'description':check[2].description,
                'reason':check[2].reason,
                'expression':check[2].expression,
                'advice': check[2].advice
            }
            for check in checks
        ]
        return DataResponse().success_response(data=result_list)
    
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=400, detail="An error occurred while processing your request")
