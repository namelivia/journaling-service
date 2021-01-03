from sqlalchemy.orm import Session
import datetime
import logging

from . import models, schemas

logger = logging.getLogger(__name__)


# TODO: skip and limit
def get_entries(db: Session):
    return db.query(models.Entry).all()


def create_entry(db: Session, entry: schemas.EntryCreate):
    db_entry = models.Entry(**entry.dict(), timestamp=datetime.datetime.now())
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    logger.info("New entry created")
    return db_entry
