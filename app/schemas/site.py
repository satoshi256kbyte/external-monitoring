"""
Webサイトモデルのスキーマ
"""

import datetime
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
    created_at: datetime
    updated_at: datetime

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "url": "https://example.com",
                    "description": "A very nice site",
                    "status": 200,
                    "created_at": "2021-07-01T00:00:00",
                    "updated_at": "2021-07-01T00:00:00",
                }
            ]
        }
    }

    class Config:
        # フィールドのカスタム設定
        json_encoders = {
            datetime: lambda v: v.isoformat()  # datetime 型のフィールドを ISO 8601 形式の文字列に変換
        }