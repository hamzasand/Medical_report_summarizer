from fastapi import FastAPI, UploadFile, File, HTTPException, Depends, BackgroundTasks
from fastapi.security import OAuth2PasswordBearer
from jwt_utils import create_access_token, verify_token
from celery.result import AsyncResult
from celery_config import summarize_medical_report_task
import shutil
import os

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.post("/token")
async def login():
    access_token = create_access_token(data={"sub": "user"})
    return {"access_token": access_token, "token_type": "bearer"}

def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    return payload

@app.post("/summarize/")
async def summarize_medical_report_api(background_tasks: BackgroundTasks ,file: UploadFile = File(...),token: str = Depends(oauth2_scheme)):
    try:
        if not file.filename.endswith(".pdf"):
            raise HTTPException(status_code=400, detail="File must be a PDF.")
        
        print('we here')
        file_path = "tmp/tmp.pdf"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        get_current_user(token)

        task = summarize_medical_report_task.delay(file_path)
        background_tasks.add_task(task.get)
        
        return {"task_id": task.id, "status": "Task started"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/tasks/{task_id}")
async def get_task_status(task_id: str):
    task_result = AsyncResult(task_id)
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result if task_result.status == 'SUCCESS' else None
    }
    return result
