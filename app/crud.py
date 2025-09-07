from sqlalchemy import desc
from sqlalchemy.orm import Session
from uuid import UUID
import datetime
import logging

from . import models, schemas

logger = logging.getLogger(__name__)


# TODO: skip and limit
def get_entries(db: Session, key: UUID):
    return (
        db.query(models.Entry)
        .filter_by(key=key)
        .order_by(desc(models.Entry.timestamp))
        .all()
    )


def create_entry(db: Session, entry: schemas.EntryCreate):
    db_entry = models.Entry(**entry.dict(), timestamp=datetime.datetime.now())
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    logger.info("New entry created")
    return db_entry
