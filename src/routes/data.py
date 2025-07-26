from fastapi import FastAPI, UploadFile, Depends,APIRouter, status
from fastapi.responses import JSONResponse
import os
from helper.config import get_settings, Settings
from controllers import DataController, ProjectController
import aiofiles
from models import ResponseSignal
import logging

logger = logging.getLogger('uvicorn.error')

data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["api_v1","data"]
)

@data_router.post("/upload/{project_id}")
async def upload_file(project_id:str,
                      file: UploadFile,
                      app_settings: Settings = Depends(get_settings)):
    #validation for allowed max size and allowed extension
    datacontroller =  DataController()
    is_valid, signal = datacontroller.validate_uploaded_file(file)
    if not is_valid:
        return JSONResponse(status_code = status.HTTP_400_BAD_REQUEST,
                            content= {"signal": signal})
    
    project_dir_path = ProjectController().get_project_path(project_id)
    file_path = datacontroller.generate_unique_filename(org_file_name = file.filename,
                                                        project_id = project_id
                                                        )
    try:                                                     
        async with aiofiles.open(file_path, "wb") as f:
            while chunk:= await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
                await f.write(chunk)
    except Exception as e:
        logger.error(f"Error while uploading the file: {e}")
        return JSONResponse( status_code= status.HTTP_400_BAD_REQUEST ,
                            content= {"signal": ResponseSignal.FILE_UPLOAD_FAILED.value})
    
    return JSONResponse( content= {"signal": ResponseSignal.FILE_UPLOAD_SUCCESS.value})


