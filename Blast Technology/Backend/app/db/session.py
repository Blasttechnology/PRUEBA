# app/db/session.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    echo=False  # Ponlo en True si quieres ver las sentencias SQL en la consola
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
