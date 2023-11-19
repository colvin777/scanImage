from fastapi import FastAPI, File, UploadFile
# from fastapi.staticfiles import StaticFiles
import shutil
import uuid
import os

# 设置图片保存的目录
IMAGE_DIR = "uploaded_images"
os.makedirs(IMAGE_DIR, exist_ok=True)


# app.mount("/static", StaticFiles(directory="uploaded_images"), name="static")
#
# @app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    # 生成唯一的文件名
    filename = f"{uuid.uuid4()}.{file.filename.split('.')[-1]}"
    file_path = os.path.join(IMAGE_DIR, filename)

    # 保存文件
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"url": f"/static/{filename}"}
