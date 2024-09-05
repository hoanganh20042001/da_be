from fastapi import APIRouter

from app.api import api_files, api_user, api_login, api_register, api_healthcheck, api_patients, api_diseases, api_units, api_result, api_excel, api_checks, api_statistical, api_reports

router = APIRouter()

router.include_router(api_healthcheck.router, tags=["health-check"], prefix="/healthcheck")
router.include_router(api_login.router, tags=["login"], prefix="/login")
router.include_router(api_register.router, tags=["register"], prefix="/register")
router.include_router(api_user.router, tags=["user"], prefix="/users")
router.include_router(api_patients.router, tags=["patients"], prefix="/patients")
router.include_router(api_diseases.router, tags=["diseases"], prefix="/diseases")
router.include_router(api_units.router, tags=["units"], prefix="/units")
router.include_router(api_reports.router, tags=["reports"], prefix="/reports")
router.include_router(api_result.router, tags=["result"], prefix="/result")     
router.include_router(api_excel.router, tags=["excel"], prefix="/excel")   
router.include_router(api_files.router, tags=["files"], prefix="/files")  
router.include_router(api_checks.router, tags=["checks"], prefix="/checks")  
router.include_router(api_statistical.router, tags=["statistical"], prefix="/statistical")  
