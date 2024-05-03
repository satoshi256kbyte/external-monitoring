"""
外形監視用のCRUD処理
"""

from sqlalchemy.orm import Session

from app import models, schemas


def get_site(db: Session, id: int) -> models.Site:
    """
    指定されたIDに対応するサイト情報を取得

    Parameters:
        db (Session): SQLAlchemy のセッション
        id (int): 取得したいサイトのID

    Returns:
        models.Site: 指定されたIDに対応するサイト情報
    """
    return db.query(models.Site).filter(models.Site.id == id).first()


def get_sites(db: Session, skip: int = 0, limit: int = 100) -> list[models.Site]:
    """
    サイト情報を一覧で取得

    Parameters:
        db (Session): SQLAlchemy のセッション
        skip (int): 取得をスキップする件数 (デフォルト: 0)
        limit (int): 取得する最大件数 (デフォルト: 100)

    Returns:
        list[models.Site]: 取得されたサイト情報のリスト
    """
    return db.query(models.Site).offset(skip).limit(limit).all()


def add_site(db: Session, site: schemas.Site) -> models.Site:
    """
    新しいサイト情報を追加

    Parameters:
        db (Session): SQLAlchemy のセッション
        site (schemas.Site): 追加するサイトの情報

    Returns:
        models.Site: 追加されたサイト情報
    """
    db_site = models.Site(url=site.url, description=site.description)
    db.add(db_site)
    db.refresh(db_site)
    return db_site


def update_site_status(db: Session, site: schemas.Site) -> models.Site:
    """
    サイト情報のステータスを更新

    Parameters:
        db (Session): SQLAlchemy のセッション
        site (schemas.Site): サイト情報

    Returns:
        models.Site: 更新されたサイト情報
    """
    db_site = db.query(models.Site).filter(models.Site.id == site.id).first()
    db_site.status = site.status
    db.commit()
    db.refresh(db_site)
    return db_site
