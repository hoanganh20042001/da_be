from fastapi import APIRouter, File, UploadFile,Depends, HTTPException
from typing import Any
from app.services.srv_excel import ExcelService
import pandas as pd
from fastapi_sqlalchemy import db
from app.models.model_patients import Patients
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
router = APIRouter()
TEMPLATE_PATH = "D:/DA/fastapi-base/files/templates/report_result.xlsx"
TEST = "D:/DA/fastapi-base/files/report"
@router.post("/import_patients/")
async def import_patients(file: UploadFile = File(...), excel_service: ExcelService = Depends()) -> Any:
    try:
        logger.info(file)
        await excel_service.import_patients(file)
        return {"status": "success", "file_name": file}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/writefile/")
async def write_file(data: list, file_name: str, title: str):
    try:
        excel_service.write_to_excel_file(data, file_name, title)
        return {"status": "success", "file_name": file_name}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/readfile/")
async def read_file(file_name: str, sheet_name: str):
    try:
        data = excel_service.read_excel_file(file_name, sheet_name)
        return {"status": "success", "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/export_result/")
async def export_data_to_excel(excel_service: ExcelService = Depends()) -> Any:
    try:       
        output=await excel_service.export_data_to_excel(TEMPLATE_PATH,TEST)
        return {"status": "success", "output": output}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))