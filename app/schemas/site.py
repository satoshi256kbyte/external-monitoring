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
    created_at: str
    updated_at: str

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