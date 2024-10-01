from celery import Celery
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Task, Base, DATABASE_URL  # Import your Task model and database setup

app = Celery('tasks', broker='redis://localhost:6379/0')

# Database setup
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@app.task
def save_summary_to_db(task_id: str, summary_text: str):
    # Create a new session
    db_session = SessionLocal()
    try:
        # Find the task by task_id
        task = db_session.query(Task).filter(Task.task_id == task_id).first()
        
        # If the task exists, update the summary
        if task:
            task.summary = summary_text
            db_session.commit()
            return f"Summary for task {task_id} saved successfully!"
        else:
            return f"Task with id {task_id} not found."

    except Exception as e:
        db_session.rollback()
        print(f"Failed to save summary: {e}")
        return "Failed to save summary."
    finally:
        db_session.close()
