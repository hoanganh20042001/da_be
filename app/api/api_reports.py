from fastapi import APIRouter, HTTPException
from typing import Any
from app.services.srv_report import generate_docx_from_template
from fastapi_sqlalchemy import db
from app.models import Patients, Checks, Diseases, Results, User, Units
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/{check_id}")
async def import_patients(check_id: int) -> Any:
    # Truy vấn dữ liệu từ cơ sở dữ liệu
    check = db.session.query(Checks).filter(Checks.id == check_id).first()
    if not check:
        raise HTTPException(status_code=404, detail="Check not found")
    
    diseases = db.session.query(Results, Diseases).join(Results, Results.disease_id == Diseases.id).filter(Results.check_id == check_id).all()
    user = db.session.query(User).filter(User.id == check.user_id).first()
    patient = db.session.query(Patients, Units).join(Patients, Patients.unit_id == Units.id).filter(Patients.id == check.patient_id).first()
    
    # Gán giá trị mặc định nếu không có dữ liệu
    patient_full_name = patient[0].full_name if patient else "Không có tên bệnh nhân"
    patient_unit_name = patient[1].name if patient and patient[1] else "Không có đơn vị"
    birth_date_str = patient[0].date_birth.strftime('%d/%m/%Y') if patient and patient[0].date_birth else "Không có ngày sinh"
    user_full_name = user.full_name if user else "Không có tên người dùng"
    check_time = str(check.time) if check.time else "Không có thời gian"
    result_status = 'bất thường' if check.result == 0 else 'bình thường'
    diseases_str = ', '.join([disease[1].name for disease in diseases]) if diseases else "Không có bệnh"
    check_description = check.description if check.description else "Không có nhận xét"
    
    # Đường dẫn tới template DOCX có sẵn
    template_path = "files/templates/template_report.docx"
    
    # Sinh báo cáo từ template
    report_path = generate_docx_from_template(
        template_path,
        patient_full_name,
        birth_date_str,
        patient_unit_name,
        user_full_name,
        check_time,
        diseases_str,
        check_description,
        result_status
    )
    
    # Trả về đường dẫn của file DOCX mới
    return {"report_path": report_path.replace("\\", "/")}
