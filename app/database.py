"""
DB接続管理
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import Config

# データベース接続設定
SQLALCHEMY_DATABASE_URI = Config.get_sqlalchemy_db_url()
print(SQLALCHEMY_DATABASE_URI)
engine = create_engine(SQLALCHEMY_DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

DeclarativeBase = declarative_base()
DeclarativeBase.metadata.create_all(bind=engine)


def get_db():
    """
    DBセッションを取得します。

    Returns:
        Session: DBセッション
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
