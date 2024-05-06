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

    @classmethod
    def get_sqlalchemy_db_url(cls) -> str:
        """
        SQLAlchemyのDB接続URLを取得

        Returns:
            str: DB接続URL
        """

        secrets = cls.get_secret()
        db_host = cls.get_ssm_parameter("external-monitoring-ssm-db-host")
        db_name = cls.get_ssm_parameter("external-monitoring-ssm-db-name")
        print(f"db_username: {secrets.get('username')}")
        print(f"db_password: {secrets.get('password')}")
        print(f"db_host: {db_host}")
        print(f"db_name: {db_name}")

        # データベース接続設定
        sqlalchemy_db_uri = (
            "mysql+pymysql://{user}:{password}@{host}/{dbname}?charset=utf8".format(
                **{
                    "user": secrets.get("username"),
                    "password": secrets.get("password"),
                    "host": os.environ.get("DB_HOST", "127.0.0.1"),
                    "dbname": os.environ.get("DB_NAME", ""),
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

        secret_name = cls.get_ssm_parameter("external-monitoring-ssm-secret-name")
        region_name = "ap-northeast-1"
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

    @classmethod
    def get_ssm_parameter(cls, param_name: str, default: str) -> str:
        """
        Get parameter from AWS SSM Parameter Store

        Args:
            param_name (str): Parameter name
            default (str): Default value
        Returns:
            str: Parameter value

        """
        ssm = boto3.client("ssm")
        response = ssm.get_parameter(Name=param_name)
        return response.get("Parameter", {}).get("Value", default)


Config = SystemConfig
