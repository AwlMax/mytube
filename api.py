import shutil

from typing import List
from fastapi import APIRouter, UploadFile, File, Form, Request
from fastapi.responses import JSONResponse

from schemas import UploadVideo, GetVideo, Message

video_router = APIRouter()

@video_router.post("/")
async def root(title: str = Form(...), description: str = Form(...), file: UploadFile = File(...)):
    info = UploadVideo(title=title, description=description)
    with open(f'{file.filename}', "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"file_name": file.filename, "info": info}

@video_router.post("/image", status_code=201)
async def upload_image(files: List[UploadFile] = File(...)):
    for image in files:
        with open(f'{image.filename}', "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
    return {"file_name": "good"}

@video_router.get("/video", response_model=GetVideo, responses={404: {"model": Message}})
async def get_video():
    user = {'id': 25, 'name': 'Test'}
    video = {'title': 'Test', 'description': 'Descrtiption'}
    info = GetVideo(user=user, video=video)
    return JSONResponse(status_code=200, content=info.dict())
