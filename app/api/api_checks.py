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
from app.schemas.sche_checks import Check, CheckUpdateRequest
from app.services.srv_user import UserService
logger = logging.getLogger()
router = APIRouter()
@router.get("", dependencies=[Depends(login_required)], response_model=Any)
async def get(params: PaginationParams = Depends()) -> Any:
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

@router.get("/get_by_patient_id/{patient_id}",
            # dependencies=[Depends(login_required)],
            response_model=Any)
async def get(patient_id: int) -> Any:
    try:
        checks = (
            db.session.query(Checks, Patients)
            .select_from(Checks)
            .outerjoin(Patients, Patients.id == Checks.patient_id)
            .filter(Checks.patient_id == patient_id)
            .all()  # Lấy tất cả các kết quả phù hợp
        )
        logging.info(patient_id)
        print(patient_id)
        if not checks:
            raise HTTPException(status_code=404, detail="Check not found")
        result_list = [
            {
                'id':check[0].id,
                'result':check[0].result,
                'time':check[0].time,
                'description':check[0].description,
                'date':check[0].date,
                'status':check[0].status,
        
            }
            for check in checks
        ]
        return DataResponse().success_response(data=result_list)
    
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=400, detail="An error occurred while processing your request")


@router.get("/{check_id}",
            # dependencies=[Depends(login_required)],
            response_model=Any)
async def get(check_id: int) -> Any:
    """
    API Get list Diseases, Checks, and Results
    """
    try:
        logger.info(check_id)
        checks = (
            db.session.query(Checks, Results, Diseases)
            .select_from(Checks)
            .outerjoin(Results, Results.check_id == Checks.id)
            .outerjoin(Diseases, Diseases.id == Results.disease_id)
            .filter(Checks.id == check_id)
            .all()  # Lấy tất cả các kết quả phù hợp
        )
        
        if not checks:
            raise HTTPException(status_code=404, detail="Check not found")
        result_list = []
        for check in checks:
            if len(check) > 1 and check[2]:  # Chỉ xử lý nếu len(check) > 1
                result_list.append({
                    'id': check[0].id if len(check) > 0 else None,
                    'name': check[2].name if len(check) > 2 and check[2] else None,
                    'name_E': check[2].name_E if len(check) > 2 and check[2] else None,
                    'accuracy': check[1].accuracy if len(check) > 1 and check[1] else None,
                    'description': check[2].description if len(check) > 2 and check[2] else None,
                    'reason': check[2].reason if len(check) > 2 and check[2] else None,
                    'expression': check[2].expression if len(check) > 2 and check[2] else None,
                    'advice': check[2].advice if len(check) > 2 and check[2] else None,
                    'image_1':check[0].image_1,
                    'image_2':check[0].image_2
                    
                })
        return DataResponse().success_response(data=result_list)
    
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=400, detail="An error occurred while processing your request")

@router.put("/{check_id}",
            dependencies=[Depends(login_required)],       
            response_model=Any)
async def update(check_id: int,request: CheckUpdateRequest,current_user: User = Depends(UserService.get_current_user)) -> Any:
    try:
        check = db.session.query(Checks).filter(Checks.id == check_id).first()
        if not check:
            raise HTTPException(status_code=404, detail="Check not found")

        # Cập nhật các trường
        check.description = request.description
        check.result = request.result
        check.user_id=current_user.id
        check.status=True
        # Lưu thay đổi vào database
        db.session.commit()

        return DataResponse().success_response(data={"description": check.description, "result": check.result})
    except Exception as e:
        raise CustomException(http_code=400, code='400', message=str(e))