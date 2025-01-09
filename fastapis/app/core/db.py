from sqlalchemy.orm import sessionmaker
from sqlmodel import create_engine

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:111222@localhost/g_p"

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
