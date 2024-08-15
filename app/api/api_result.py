import logging
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, File, UploadFile

from app.helpers.exception_handler import CustomException
from app.helpers.login_manager import login_required, PermissionRequired
from app.helpers.paging import Page, PaginationParams, paginate
from app.schemas.sche_base import DataResponse
from app.schemas.sche_result import PredictionsResponse
from app.services.srv_result import ResultService
from app.services.srv_user import UserService
from app.models import User
logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/{cccd}", dependencies=[Depends(login_required)], response_model=DataResponse[PredictionsResponse])
def detail(cccd: str,file: UploadFile = File(...),
           current_user: User = Depends(UserService.get_current_user),
            result_service: ResultService = Depends()) -> Any:
    # try:
        result = result_service.predict(file,cccd,current_user)
        return DataResponse().success_response(data=result)
    # except CustomException as ce:
    #     logger.error(f"CustomException: {ce}")
    #     raise HTTPException(status_code=ce.status_code, detail=ce.detail)
    # except Exception as e:
    #     logger.error(f"Unhandled exception: {e}")
    #     raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/{filename}")
async def get_image(filename: str):
    logger.info(f"Received request for filename: {filename}")
    
    # Xóa phần "/files/" khỏi tên tệp nếu cần
    file_location = filename.replace("/files/", "", 1)
    logger.info(f"Processed file location: {file_location}")
    
    # Chuyển đổi file_location thành Path object
    file_path =  file_location
    
    # Kiểm tra xem file có tồn tại không
    # if not file_path.exists():
    #     raise HTTPException(status_code=404, detail="Image not found")
    return 1