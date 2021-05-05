
from typing import List
from fastapi import APIRouter
from pydantic import BaseModel
import sqlalchemy
from sqlalchemy import MetaData

from .conn import database
from .crud import Crud

metadata = sqlalchemy.MetaData()

model = sqlalchemy.Table(
    "category",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column("description", sqlalchemy.String),
)


class TypeCreate(BaseModel):
    name: str
    description: str


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
    # print(dict(records[0]))
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
    # print(record)
    record = request.dict()
    return update_record(id, record)


@router.delete("/{id}", response_model=int)
def delete_category(id: int):
    return delete_record(id)

    ###
    # run in console
    # import asyncio
    # record = asyncio.run( query_all() )
    # def query_all(whereClause=None, limit: int = 5):
    #     sql = model.select().limit(limit)
    #     if whereClause is not None:
    #         sql = sql.where(sqlalchemy.sql.text(whereClause))
    #     return database.fetch_all(sql)

    # def query_by_id(id):
    #     sql = model.select().where(model.c.id == id)
    #     return database.fetch_one(sql)

    # def insert_record(record):
    #     sql = model.insert(None).values(**record)
    #     # query = model.insert().values(name=record.name, description=record.description)
    #     last_record_id = database.execute(sql)
    #     return query_by_id(last_record_id)
    #     # return {**record, "id": last_record_id}

    # def update_record(id, record):
    #     sql = model.update(None).values(
    #         **record).where(model.c.id == id)
    #     result = database.execute(sql)
    #     # success
    #     if result == 1:
    #         return query_by_id(id)
    #     else:
    #         return None

    # def delete_record(id):
    #     sql = model.delete(None).where(model.c.id == id)
    #     return database.execute(sql)
