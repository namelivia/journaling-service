from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

EntryBase = declarative_base()


class Entry(EntryBase):
    __tablename__ = "entries"
    id = Column(Integer, primary_key=True, index=True)
    message = Column(String)
    timestamp = Column(DateTime, nullable=False)
