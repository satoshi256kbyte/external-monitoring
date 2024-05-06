"""
Webサイトモデルのスキーマ
"""

from typing import Union

from pydantic import BaseModel


class Site(BaseModel):
    """
    Webサイトモデルクラス

    Args:
        BaseModel: Pydanticのベースモデルクラス
    """

    id: int
    url: str
    description: Union[str, None] = None
    status: Union[int, None] = None
    # created_at: datetime
    # updated_at: datetime
