# from sqlalchemy import create_engine, Column, Integer, String, Text
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker

# DATABASE_URL = "sqlite:///./test.db"

# engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = declarative_base()

# class Task(Base):
#     __tablename__ = "tasks"
#     id = Column(Integer, primary_key=True, index=True)
#     task_id = Column(String, unique=True, index=True)
#     filename = Column(String)
#     summary = Column(Text)

# Base.metadata.create_all(bind=engine)
