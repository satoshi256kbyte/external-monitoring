"""
コンフィグ
"""

import json
import os

import boto3


class SystemConfig:
    """
    システム設定管理クラス
    """

    # SSMクライアント
    ssm_client = boto3.client("ssm", region_name="ap-northeast-1")

    @classmethod
    def get_sqlalchemy_db_url(cls) -> str:
        """
        SQLAlchemyのDB接続URLを取得

        Returns:
            str: DB接続URL
        """

        db_host = os.environ.get("DB_HOST", "DB_HOST")
        db_name = os.environ.get("DB_NAME", "DB_NAME")
        db_user = os.environ.get("DB_USER", "DB_USER")
        db_pass = os.environ.get("DB_PASS", "DB_PASS")
        print(f"db_host: {db_host}")
        print(f"db_name: {db_name}")
        print(f"db_username: {db_user}")
        print(f"db_password: {db_pass}")

        # データベース接続設定
        sqlalchemy_db_uri = (
            "mysql+pymysql://{user}:{password}@{host}/{dbname}?charset=utf8".format(
                **{
                    "user": db_user,
                    "password": db_pass,
                    "host": db_host,
                    "dbname": db_name,
                }
            )
        )
        # SQLALCHEMY_TRACK_MODIFICATIONS = False
        # SQLALCHEMY_ECHO = True
        # SQLALCHEMY_ENGINE_OPTIONS = {
        #     # 'pool': QueuePool(creator),
        #     # 'pool_size': 10,
        #     "pool_recycle": 900,
        #     # 'pool_pre_ping': True
        # }

        return sqlalchemy_db_uri

    @classmethod
    def get_secret(cls):
        """
        AWS Secrets Managerから秘密情報を取得

        Returns:
            dict: Secret情報
        """

        secret_name = os.environ.get("AWS_SECRET_NAME", "AWS_SECRET_NAME")
        print(f"secret_name: {secret_name}")

        # Secrets Manager クライアントを初期化
        session = boto3.session.Session()
        client = session.client(
            service_name="secretsmanager", region_name="ap-northeast-1"
        )
        print("create boto3 client")

        # Secrets Managerから秘密情報を取得
        response = client.get_secret_value(SecretId=secret_name)

        print("get secret value")
        print(response)

        if "SecretString" in response:
            secret = response.get("SecretString")
            print(f"secret: {secret}")
            return json.loads(secret)
        return None


Config = SystemConfig
