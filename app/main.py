"""
API本体
"""

from datetime import datetime, timedelta

import httpx
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from app.schemas.site import Site as SiteSchema
from app.crud import external_monitoring as crud
from app.database import get_db

app = FastAPI()


@app.get("/healthcheck")
async def healthcheck() -> dict[str, str]:
    """
    ヘルスチェック用

    Args:
        None

    Returns:
        dict[str, str]: ヘルスチェックメッセージ。
    """
    return {"message": "OK"}


@app.get("/sites/{id}", response_model=SiteSchema)
async def read_item(id: int, db: Session = Depends(get_db)) -> SiteSchema:
    """
    サイトの情報を取得

    Args:
        id (int): サイトのID。
        db (Session, optional): DBセッション

    Returns:
        SiteSchema: 取得されたサイトの情報。
    """
    return crud.get_site(db=db, id=id)


@app.get("/sites/")
async def read_items(
    skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
) -> list[SiteSchema]:
    """
    サイトの一覧を取得

    Args:
        skip (int, optional): 取得開始位置。デフォルトは0。
        limit (int, optional): 取得件数。デフォルトは10。
        db (Session, optional): DBセッション

    Returns:
        list[SiteSchema]: サイト情報一覧
    """
    return crud.get_sites(db=db, skip=skip, limit=limit)


@app.post("/sites/")
async def create_item(
    site: SiteSchema, db: Session = Depends(get_db)
) -> SiteSchema:
    """
    新しいサイトを追加します。

    Args:
        site (SiteSchema): 追加するサイトの情報。
        db (Session, optional): DBセッション

    Returns:
        SiteSchema: 追加されたサイトの情報。
    """
    site = crud.add_site(db=db, site=site)
    db.commit()
    return site


@app.get("/sites-check/")
async def check_sites(db: Session = Depends(get_db)) -> list[SiteSchema]:
    """
    全サイトのステータスをチェックします。

    Args:
        skip (int, optional): 取得開始位置。デフォルトは0。
        limit (int, optional): 取得件数。デフォルトは10。
        db (Session, optional): DBセッション

    Returns:
        list[SiteSchema]: ステータスチェック後のサイト情報一覧
    """

    sites: list[SiteSchema] = crud.get_sites(db=db)
    five_minutes_ago: datetime = datetime.now() - timedelta(minutes=5)
    count: int = 0
    for site in sites:
        print(f"Checking site {site.url}")
        if site.modified >= five_minutes_ago:
            print(f"Skipping {site.url}")

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(site.url)
                site.status = response.status_code
                site.modified = datetime.now()
                print(f"Status for {site.url}: {site.status}")
                count += 1
        except Exception as e:
            print(f"Failed to access {site.url}: {str(e)}")

    if count > 0:
        db.commit()

    return crud.get_sites(db=db)
