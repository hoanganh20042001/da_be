import logging
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi_sqlalchemy import db
from sqlalchemy import func
import math
from app.helpers.exception_handler import CustomException
from app.helpers.login_manager import login_required, PermissionRequired
from app.helpers.paging import Page, PaginationParams, paginate, MetadataSchema
from app.schemas.sche_base import DataResponse
from app.schemas.sche_units import UnitsItemResponse, UnitsCreateRequest,  UnitsUpdateRequest
from app.services.srv_units import UnitsService
from app.models import Units
from sqlalchemy.orm import aliased
logger = logging.getLogger()
router = APIRouter()


@router.get("", dependencies=[Depends(login_required)], response_model=Any)
def get(params: PaginationParams = Depends()) -> Any:
    """
    API Get list Units
    """
    try:
        unit_alias = aliased(Units)
        unit_father_alias = aliased(Units, name='unit_father')

        # Thực hiện truy vấn Self-Join
        query = (
            db.session.query(unit_alias, unit_father_alias)
            .join(unit_father_alias, unit_alias.unit_father_id == unit_father_alias.id)
        )

        # Thực hiện lọc nếu có từ khóa tìm kiếm
        if params.search_text:
            query = query.filter(unit_alias.name.ilike(f"%{params.search_text}%"))

    # Tính tổng số bản ghi
        total = db.session.query(func.count()).select_from(query.subquery()).scalar()

    # Thực hiện phân trang
        paginated_query = (
            query.limit(params.page_size).offset(params.page_size * (params.page - 1)))
    
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
                'name': check[0].name,
                'symbol': check[0].symbol,
                'unit_father': check[1].name,
        
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
