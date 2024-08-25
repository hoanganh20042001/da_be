import logging
from typing import Any
from fastapi import APIRouter, Depends
from fastapi_sqlalchemy import db
from sqlalchemy import func
from app.helpers.login_manager import login_required
from app.models import Patients, User

logger = logging.getLogger()
router = APIRouter()

@router.get("/users/", dependencies=[Depends(login_required)], response_model=Any)
def getUser() -> Any:
    # Tạo truy vấn cơ bản cho bảng User
    user_query = db.session.query(User.role_id, func.count(User.id)).group_by(User.role_id).all()
    user_result = [{"role": role_id, "count": count} for role_id, count in user_query]

    # Tạo truy vấn cơ bản cho bảng Patient và lấy số lượng bệnh nhân
    patient_count = db.session.query(func.count(Patients.id)).scalar()
    
    # Thêm quyền "P" vào kết quả với số lượng bệnh nhân
    patient_result = [{"role": "P", "count": patient_count}]
    
    # Kết hợp dữ liệu từ hai bảng
    combined_result = user_result + patient_result
    
    return {"data": combined_result}
