import asyncio
import re

import fastapi
import httpx
import uvicorn
import nest_asyncio
from fastapi import HTTPException, UploadFile, File
from utils.log import setup_logger
from database import connection

app = fastapi.FastAPI()

logger = setup_logger('fastapi', "DEBUG")

# -------Подключение к БД-------------------
nest_asyncio.apply()
db = connection.DBConnection()
try:
    asyncio.run(db.initialize_connection())
except Exception as e:
    logger.error("Ошибка во время подключения к базе данных", exc_info=e)


# ----------------------------------------


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post('/create-user/{user}')
async def create_user(user: str):
    if not (asyncio.run(db.check_auth_user(user=user))):
        asyncio.run(db.auth_user(user=user))
        return {"message": "User created"}
    else:
        raise HTTPException(status_code=409, detail="User already exists")


@app.post("/create-file/{folder_name}")
async def create_file(folder_name: str, file: UploadFile = File(...)):
    url = "http://10.1.0.156:8080/upload"
    user_id = folder_name

    # Используем асинхронного клиента
    async with httpx.AsyncClient() as client:
        # Используем объект `UploadFile` от FastAPI для получения содержимого файла
        file_content = await file.read()

        # Отправляем файл на другой сервер
        response = await client.post(
            url,
            files={
                'file': (file.filename, file_content, file.content_type)
            },
            params={
                'user_id': user_id
            }
        )
    pattern = r'f=([^&]+)'
    if response.status_code == 200:
        url_ = response.text
        match = re.search(pattern, url_)
        if match:
            # Извлечение и вывод значения
            link = match.group(1).strip()
        if not asyncio.run(db.check_folder(folder_name)):
            asyncio.run(db.create_folder(folder_name))
        asyncio.run(db.create_file(folder_name, file.filename, link))
    return {
        "status_code": response.status_code,
        "response_text": response.text.strip()
    }


@app.get("/show-links/{folder_name}")
async def show_links(folder_name: str):
    if not (asyncio.run(db.check_folder(folder=folder_name))):
        return {"message": "NET PAPKI CHTOBI CHETO DATb"}
    try:
        links = await db.show_links(folder_name)
        return links
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/file-id/{link}")
async def file_id(link: str):
    file_name = await db.get_filename(link)
    if not file_name:
        raise HTTPException(status_code=404, detail="File not found")
    else:
        return file_name


#.run(app, host="127.0.0.1", port=8001)  # прикол для дебага
