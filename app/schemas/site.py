"""
Webサイトモデルのスキーマ
"""

from datetime import datetime
from typing import Union

from pydantic import BaseModel


class Site(BaseModel):
    id: int
    url: str
    description: Union[str, None] = None
    status: Union[int, None] = None
    created_at: datetime
    updated_at: datetime

    # 暫定対応
    class Config:
        arbitrary_types_allowed = True
