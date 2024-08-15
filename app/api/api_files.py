import logging
from typing import Any
from fastapi.responses import FileResponse
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile

from app.helpers.exception_handler import CustomException
from app.helpers.login_manager import login_required, PermissionRequired
from app.helpers.paging import Page, PaginationParams, paginate
from app.schemas.sche_base import DataResponse
from app.schemas.sche_result import PredictionsResponse
from app.services.srv_result import ResultService
from app.services.srv_user import UserService
from app.models import User
from pathlib import Path
logger = logging.getLogger(__name__)
router = APIRouter()
UPLOAD_DIRECTORY = Path("files")

@router.get("/")
async def get_image(file_path: str):
    # logger.info(f"Received request for filename: {file_path}")
    file_location = Path(file_path)

    # Kiểm tra xem file có tồn tại hay không
    if not file_location.exists() or not file_location.is_file():
        raise HTTPException(status_code=404, detail="File not found")

    # Trả về file ảnh
    return FileResponse(file_location)
