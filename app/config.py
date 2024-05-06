"""
コンフィグ
"""

import os


class SystemConfig:
    """
    システム設定管理クラス
    """

    SQLALCHEMY_DATABASE_URI = (
        "mysql+pymysql://{user}:{password}@{host}/{dbname}?charset=utf8".format(
            **{
                "user": os.environ.get("DB_USER", "root"),
                "password": os.environ.get("DB_PASSWORD", ""),
                "host": os.environ.get("DB_HOST", "127.0.0.1"),
                "dbname": os.environ.get("DB_NAME", ""),
            }
        )
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_ENGINE_OPTIONS = {
        # 'pool': QueuePool(creator),
        # 'pool_size': 10,
        "pool_recycle": 900,
        # 'pool_pre_ping': True
    }


Config = SystemConfig
