import os
from fastapi import APIRouter, File, UploadFile
import shutil
import uuid

upload = APIRouter()

# 设置图片保存的目录
IMAGE_DIR = "uploaded_images"
os.makedirs(IMAGE_DIR, exist_ok=True)


@upload.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    # 生成唯一的文件名
    filename = f"{uuid.uuid4()}.{file.filename.split('.')[-1]}"
    file_path = os.path.join(IMAGE_DIR, filename)

    # 保存文件
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"url": f"/static/{filename}"}
