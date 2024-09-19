from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from typing import List
import shutil
import os
import subprocess
import logging
import torch
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from fastapi import UploadFile
from pydantic import ValidationError
from starlette import status
from fastapi_sqlalchemy import db
from app.models import Checks
from app.models import Results
from app.models import User
from app.models import Patients
from app.models import Diseases
from sqlalchemy import desc
from datetime import datetime
# Khởi tạo FastAPI
from app.helpers.save_file_result import get_timestamped_file_path
from app.schemas.sche_result import PredictionsResponse, Prediction
from app.schemas.sche_result import PredictionsResponse
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Đường dẫn tới mô hình YOLOv9
WEIGHTS_PATH = "yolov9/runs/train/exp/weights/best.pt"
DETECT_SCRIPT = "yolov9/detect.py"
RESULTS_DIR = "files/detect"

class ResultService(object):
    __instance = None

    def __init__(self) -> None:
        pass

    reusable_oauth2 = HTTPBearer(
        scheme_name='Authorization'
    )


    @staticmethod
    async def predict(file: UploadFile,cccd) -> PredictionsResponse:
        patient = db.session.query(Patients).filter(Patients.identification == cccd).first()
        if patient is None:
            raise Exception('patient not exists')
        check = db.session.query(Checks).filter(Checks.patient_id == patient.id).order_by(desc(Checks.time)).first()
        time=1
        if check :
            time=check.time+1
        
    # Lưu file ảnh tạm thời với timestamp
        temp_file = get_timestamped_file_path("files/temp_images", file.filename)
        with open(temp_file, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        logger.info(f"Temporary file saved at {temp_file}")

        # Tạo thư mục kết quả mới với tên tăng dần
        output_dir = get_timestamped_file_path(RESULTS_DIR, "")
        logger.info(f"Temporary file saved at 1 {output_dir}")
        # Chạy YOLOv9 detect.py script
        command = [
            "python", DETECT_SCRIPT,
            "--weights", WEIGHTS_PATH,
            "--source", temp_file,
            "--project", RESULTS_DIR,
            "--name", os.path.basename(RESULTS_DIR),
            "--exist-ok",
            # "--conf-thres", "0.3",  # Ngưỡng confidence
            # "--iou-thres", "0.4" 
        ]
        result = subprocess.run(command, capture_output=True, text=True)
        logger.info(result)
        logger.info(result.stdout)

        # Xóa file ảnh tạm thời
        # os.remove(temp_file)
        logger.info(temp_file)
        # Tìm đường dẫn của ảnh đã nhận diện
        detected_image_path = None
        logger.info(os.path.basename(temp_file))
        detected_image_path = os.path.join('files/detect/detect', os.path.basename(temp_file))
        #             break
        logger.info(detected_image_path)
        new_check = Checks(
        #    user_id=current_user.id,
           patient_id=patient.id,
        #    description=data.description,
           time=time,
           date=datetime.now(),
           image_1=temp_file,
           image_2=detected_image_path.replace("\\", "/"),
        )
        logger.info(f"Ttest {new_check}")
        db.session.add(new_check)
        db.session.commit()
        # Trích xuất kết quả từ output của YOLOv9
        predictions = []
        output_lines = result.stdout.replace("[tensor([", "").replace("])]", "").replace("\n", "").strip()
        if output_lines.startswith('['):
            logger.info(output_lines)
            logger.info(type(output_lines))
            data_list = output_lines
            data_list = eval(output_lines)
            logger.info(data_list)
            print(type(data_list))
            if type(data_list) == list:
                disease_id = int(data_list[5]) + 1  # Đảm bảo line[5] là số nguyên
                accuracy = float(data_list[4])  # Đảm bảo line[4] là số thực hoặc có thể chuyển đổi thành số thực
                new_result = Results(
                    check_id=new_check.id,
                    disease_id=disease_id,
                    accuracy=accuracy,
                        # image=detected_image_path.replace("\\", "/"),
                )
                logger.info(new_result)
                db.session.add(new_result)
                db.session.commit()
                    
            for line in data_list:
                if isinstance(line, list):
                    disease_id = int(line[5]) + 1  # Đảm bảo line[5] là số nguyên
                    accuracy = float(line[4])  # Đảm bảo line[4] là số thực hoặc có thể chuyển đổi thành số thực
                    new_result = Results(
                        check_id=new_check.id,
                        disease_id=disease_id,
                        accuracy=accuracy,
                        # image=detected_image_path.replace("\\", "/"),
                    )
                    logger.info(new_result)
                    db.session.add(new_result)
                    db.session.commit()
        return PredictionsResponse( detected_image_path=str(detected_image_path.replace("/", "\\")), check_id= new_check.id)


    @staticmethod
    def get(patient_id):
        exist_patient = db.session.query(Patients, Diseases).join(Diseases, Patients.id == Diseases.patient_id).filter(Patients.id == patient_id).all()
        if exist_patient is None:
            raise Exception('patient not exists')
        return exist_disease

