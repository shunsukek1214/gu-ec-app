import pymysql
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    db_host: str
    db_port: int = 3306
    db_user: str
    db_password: str
    db_name: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()

connection = pymysql.connect(
    host=settings.db_host,
    port=settings.db_port,
    user=settings.db_user,
    password=settings.db_password,
    database=settings.db_name,
    charset='utf8mb4',
    connect_timeout=5
)

try:
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        print("SELECT 1の結果:", result)

        cursor.execute("SELECT DATABASE()")
        database = cursor.fetchone()
        print("現在のデータベース:", database)
finally:
    connection.close()