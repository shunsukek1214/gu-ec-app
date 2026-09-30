from sqlalchemy import create_engine    #DBとの接続窓口を作る
from sqlalchemy.engine import URL   #MySQL｀接続情報を安全に組み立てる
from sqlalchemy.orm import DeclarativeBase, sessionmaker    #ORMモデルの親クラスを作る、DB操作用Sessionを作る
from app.core.config import settings

 #URLを作る
DATABASE_URL = URL.create(
    "mysql+pymysql",    #MySQLをPyNySQL経由で使う
    username=settings.db_user,
    password=settings.db_password,
    host=settings.db_host,
    port=settings.db_port,
    database=settings.db_name
)

#Engineを作る
engine = create_engine(DATABASE_URL, pool_pre_ping=True, pool_recycle=3600)    #DB接続の生存確認をする、長時間使い続けた接続を再利用し続けない設定
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, expire_on_commit=False)    #DB操作の単位となるSessionを作る

class Base(DeclarativeBase):    #ORMモデルの親クラスを作る
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()