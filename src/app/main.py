"""
API本体
"""

from datetime import datetime, timedelta

import httpx
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from app import models, schemas
from app.crud import external_monitoring as crud

from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/sites/{id}", response_model=schemas.Site)
async def read_item(id: int, db: Session = Depends(get_db)) -> schemas.Site:
    """
    サイトの情報を取得

    Args:
        id (int): サイトのID。
        db (Session, optional): DBセッション

    Returns:
        schemas.Site: 取得されたサイトの情報。
    """
    return crud.get_site(db=db, id=id)


@app.get("/sites/")
async def read_items(
    skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
) -> list[schemas.Site]:
    """
    サイトの一覧を取得

    Args:
        skip (int, optional): 取得開始位置。デフォルトは0。
        limit (int, optional): 取得件数。デフォルトは10。
        db (Session, optional): DBセッション

    Returns:
        list[schemas.Site]: サイト情報一覧
    """
    return crud.get_sites(db=db, skip=skip, limit=limit)


@app.post("/sites/")
async def create_item(
    site: schemas.Site, db: Session = Depends(get_db)
) -> schemas.Site:
    """
    新しいサイトを追加します。

    Args:
        site (schemas.Site): 追加するサイトの情報。
        db (Session, optional): DBセッション

    Returns:
        schemas.Site: 追加されたサイトの情報。
    """
    site = crud.add_site(db=db, site=site)
    db.commit()
    return site


@app.get("/sites-check/")
async def check_sites(db: Session = Depends(get_db)) -> list[schemas.Site]:
    """
    全サイトのステータスをチェックします。

    Args:
        skip (int, optional): 取得開始位置。デフォルトは0。
        limit (int, optional): 取得件数。デフォルトは10。
        db (Session, optional): DBセッション

    Returns:
        list[schemas.Site]: ステータスチェック後のサイト情報一覧
    """

    sites: list[schemas.Site] = crud.get_sites(db=db)
    five_minutes_ago: datetime = datetime.now() - timedelta(minutes=5)
    count: int = 0
    for site in sites:
        if site.modified < five_minutes_ago:
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.get(site.url)
                    status_code: int = response.status_code
                    site.status = status_code if status_code else "Error"
                    site.modified = datetime.now()
                    count += 1
            except Exception as e:
                print(f"Failed to access {site.url}: {str(e)}")

    if count > 0:
        db.commit()

    return crud.get_sites(db=db)
