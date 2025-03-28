# app/core/config.py
from pydantic import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "ABM con FastAPI y SQL Server"
    # Cadena de conexión para SQL Server usando autenticación de Windows y la base de datos "Blast"
    SQLALCHEMY_DATABASE_URI: str = (
        r"mssql+pyodbc://@Facu\MSSQLSERVER01/Blast?driver=ODBC+Driver+17+for+SQL+Server&Trusted_Connection=yes"
    )

    class Config:
        env_file = ".env"  # Opcional, para manejar variables de entorno

settings = Settings()


