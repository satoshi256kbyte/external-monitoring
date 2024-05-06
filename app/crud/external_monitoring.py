"""
外形監視用のCRUD処理
"""

from sqlalchemy.orm import Session

from app.models.site import Site
from app.schemas.site import Site as SiteSchema


def get_site(db: Session, id: int) -> Site:
    """
    指定されたIDに対応するサイト情報を取得

    Parameters:
        db (Session): SQLAlchemy のセッション
        id (int): 取得したいサイトのID

    Returns:
        Site: 指定されたIDに対応するサイト情報
    """
    return db.query(Site).filter(Site.id == id).first()


def get_sites(db: Session, skip: int = 0, limit: int = 100) -> list[Site]:
    """
    サイト情報を一覧で取得

    Parameters:
        db (Session): SQLAlchemy のセッション
        skip (int): 取得をスキップする件数 (デフォルト: 0)
        limit (int): 取得する最大件数 (デフォルト: 100)

    Returns:
        list[Site]: 取得されたサイト情報のリスト
    """
    return db.query(Site).offset(skip).limit(limit).all()


def add_site(db: Session, site: SiteSchema) -> Site:
    """
    新しいサイト情報を追加

    Parameters:
        db (Session): SQLAlchemy のセッション
        site (SiteSchema): 追加するサイトの情報

    Returns:
        Site: 追加されたサイト情報
    """
    db_site = Site(url=site.url, description=site.description)
    db.add(db_site)
    db.refresh(db_site)
    return db_site


def update_site_status(db: Session, site: SiteSchema) -> Site:
    """
    サイト情報のステータスを更新

    Parameters:
        db (Session): SQLAlchemy のセッション
        site (SiteSchema): サイト情報

    Returns:
        Site: 更新されたサイト情報
    """
    db_site = db.query(Site).filter(Site.id == site.id).first()
    db_site.status = site.status
    db.commit()
    db.refresh(db_site)
    return db_site
