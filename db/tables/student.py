
from typing import List
import datetime

from fastapi import APIRouter
from pydantic import BaseModel
import sqlalchemy
from sqlalchemy import MetaData

from .conn import database
from .crud import Crud

metadata = sqlalchemy.MetaData()

model = sqlalchemy.Table(
    "student",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column("lastname", sqlalchemy.String),
    sqlalchemy.Column("age", sqlalchemy.Integer),
    sqlalchemy.Column("birth", sqlalchemy.Date),
)


class TypeCreate(BaseModel):
    name: str
    lastname: str
    age: int
    birth: datetime.date


class Type(TypeCreate):
    id: int

    class Config:
        orm_mode = True


crud = Crud(database, model)


def query_all(whereClause=None, page_no: int = 0, page_size=None, order_by=None):
    return crud.query_all(whereClause, page_no, page_size, order_by)


def query_by_id(id):
    return crud.query_by_id(id)


def insert_record(record):
    return crud.insert_record(record)


def update_record(id, record):
    return crud.update_record(id, record)


def delete_record(id):
    return crud.delete_record(id)


router = APIRouter()


@router.get("/", response_model=List[Type])
def read_category():
    records = query_all()
    return records


@router.get("/{id}", response_model=Type)
def read_category_by_id(id: int):
    return query_by_id(id)


@router.post("/", response_model=Type)
def create_category(request: TypeCreate):
    record = request.dict()
    return insert_record(record)


@router.put("/{id}", response_model=Type)
def update_category(id: int, request: TypeCreate):
    record = request.dict()
    return update_record(id, record)


@router.delete("/{id}", response_model=int)
def delete_category(id: int):
    return delete_record(id)
