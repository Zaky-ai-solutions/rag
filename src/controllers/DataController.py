from .BaseController import BaseController
from fastapi import FastAPI, UploadFile, Depends,APIRouter

class DataController(BaseController):
    def __init__(self):
        super().__init__()
        self.scale = 1048576
    def validate_uploaded_file(self, file:UploadFile):
        if file.content_type not in self.app_settings.FILE_ALLOWED_TYPES:
            return False
        if file.size > self.app_settings.FILE_MAX_SIZE * self.scale:
            return False
        return True