"""
Webサイトモデル
"""

from sqlalchemy import Column, DateTime, Integer, String

from app.database import Base


class Site(Base):
    """
    Webサイトモデルクラス

    Args:
        Base (_type_): DBモデルのベースクラス
    """

    __tablename__ = "sites"

    id: Column = Column(Integer, primary_key=True)
    url: Column = Column(String, unique=True, index=True)
    description: Column = Column(String)
    status: Column = Column(Integer, default=0)
    created_at: Column = Column(DateTime, default=DateTime.now())
    updated_at: Column = Column(DateTime, default=DateTime.now())
