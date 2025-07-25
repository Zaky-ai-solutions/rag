from fastapi import FastAPI, UploadFile, Depends,APIRouter
import os
from helper.config import get_settings, Settings
from controllers import DataController
data_router = APIRouter(
    prefix="/app/v1/data",
    tags=["api_v1","data"]
)

@data_router.post("/upload/{project_id}")
async def upload_file(project_id:str,
                      file: UploadFile,
                      app_settings: Settings = Depends(get_settings)):
    #validation for allowed max size and allowed extension
    is_valid = await DataController.validate_uploaded_file(file)
    return {"messag" : is_valid,
            "proj_id": project_id }