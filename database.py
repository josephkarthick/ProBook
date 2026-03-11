from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

postgresql+psycopg2://user:Yd6YUjCb4uy0pzYICXzfxClny38mte8o@host:5432/probook

engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()


# 🔥 ADD THIS FUNCTION
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
