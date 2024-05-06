"""
DB接続管理
"""

import json
import os

import boto3
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


def get_secret():
    """
    AWS Secrets Managerから秘密情報を取得

    Returns:
        dict: Secret情報
    """

    secret_name = os.environ.get("AWS_SECRET_NAME")
    region_name = os.environ.get("AWS_REGION", "ap-northeast-1")
    print(f"secret_name: {secret_name}")
    print(f"region_name: {region_name}")

    # Secrets Manager クライアントを初期化
    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager", region_name=region_name)

    # Secrets Managerから秘密情報を取得
    response = client.get_secret_value(SecretId=secret_name)

    if "SecretString" in response:
        secret = response.get("SecretString")
        return json.loads(secret)
    return None


secrets = get_secret()

# データベース接続設定
SQLALCHEMY_DATABASE_URI = (
    "mysql+pymysql://{user}:{password}@{host}/{dbname}?charset=utf8".format(
        **{
            "user": secrets.get("username"),
            "password": secrets.get("password"),
            "host": os.environ.get("DB_HOST", "127.0.0.1"),
            "dbname": os.environ.get("DB_NAME", ""),
        }
    )
)

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
