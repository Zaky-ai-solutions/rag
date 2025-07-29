from fastapi import FastAPI, UploadFile, Depends,APIRouter, status
from fastapi.responses import JSONResponse
import os
from helper.config import get_settings, Settings
from controllers import DataController, ProjectController,ProcessController
import aiofiles
from models import ResponseSignal
import logging
from schemas.data import ProcessRequest


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
    file_path, file_id = datacontroller.generate_unique_filename(org_file_name = file.filename,
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
    
    return JSONResponse( content= {
        "signal": ResponseSignal.FILE_UPLOAD_SUCCESS.value,
         "file_id": file_id
        }
        )

@data_router.post("/process/{project_id}")
async def process_endpoint(project_id, process_request:ProcessRequest ):
    file_id = process_request.file_id
    chunk_size = process_request.chunk_size
    chunk_overlap = process_request.overlap_size

    process_controller = ProcessController(project_id)
    file_content = process_controller.get_file_content(file_id)
    chunks = process_controller.process_file_content(
        file_content = file_content,
        file_id= file_id,
        chunk_size =chunk_size ,
        overlap_size=chunk_overlap,
    )
    if chunks is None or len(chunks) == 0:
        return JSONResponse( content= {
        "signal": ResponseSignal.PROCESSING_FAIL.value,
         "file_id": file_id
        },
        status_code= status.HTTP_400_BAD_REQUEST
        )
    return chunks



