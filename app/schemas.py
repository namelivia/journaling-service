import datetime

from pydantic import BaseModel, Field


class EntryBase(BaseModel):
    message: str = Field(title="Journal message")


class EntryCreate(EntryBase):
    pass


class Entry(EntryBase):
    id: int
    timestamp: datetime.datetime = Field(
        title="Timestamp for the journal entry"
    )

    class Config:
        orm_mode = True
