from fastapi import (
    FastAPI,
    Depends,
)
from fastapi.middleware.cors import CORSMiddleware
from http import HTTPStatus
from app.dependencies import get_db
from uuid import UUID
from sqlalchemy.orm import Session
from .database import engine, Base
from . import crud, schemas
from typing import List
import logging
import sys

Base.metadata.create_all(bind=engine)

app = FastAPI()

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

origins = [
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/{key}/all", response_model=List[schemas.Entry])
def entries(key: UUID, db: Session = Depends(get_db), skip: int = 0, limit: int = 10):
    entries = crud.get_entries(db, key)
    return entries


@app.post("/new", response_model=schemas.Entry, status_code=HTTPStatus.CREATED)
def create_entry(entry: schemas.EntryCreate, db: Session = Depends(get_db)):
    return crud.create_entry(db, entry)
