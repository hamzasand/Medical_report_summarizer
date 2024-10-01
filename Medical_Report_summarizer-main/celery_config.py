from celery import Celery
from demo import summarize_medical_report

celery_app = Celery('my_fastapi_app', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')

@celery_app.task
def summarize_medical_report_task(file_path: str):
    try:
        print(f"Processing file: {file_path}")
        summary = summarize_medical_report(file_path)
        print(f"Summary generated: {summary}")
        return summary
    except Exception as e:
        print(f"Error in task: {str(e)}")
        return str(e)
