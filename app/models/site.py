"""
Webサイトモデル
"""

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.sql import func

from app.database import DeclarativeBase


class Site(DeclarativeBase):
    """
    Webサイトモデルクラス

    Args:
        Base (_type_): DBモデルのベースクラス
    """

    __tablename__ = "sites"

    id = Column(Integer, primary_key=True)
    url = Column(String, unique=True, index=True)
    description = Column(String)
    status = Column(Integer, default=0)
    created_at = Column(
        DateTime, default=func.now()
    )  # 現在の時刻をデフォルト値として設定
    updated_at = Column(
        DateTime, default=func.now(), onupdate=func.now()
    )  # 更新時にも現在の時刻をセット
