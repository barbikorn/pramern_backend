from typing import List, Optional
import datetime

from fastapi import APIRouter
from pydantic import BaseModel
import sqlalchemy
from sqlalchemy import MetaData

import sys
db_path = "/home/tanakrit_tiger/senior/db"
sys.path.append(db_path)
from conn import database
from crud import Crud

metadata = sqlalchemy.MetaData()

model = sqlalchemy.Table(
    "from_led",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("court", sqlalchemy.String),
    sqlalchemy.Column("case_num", sqlalchemy.String),
    sqlalchemy.Column("plaintiff", sqlalchemy.String),
    sqlalchemy.Column("defendant", sqlalchemy.String),
    sqlalchemy.Column("prop_type", sqlalchemy.String),
    sqlalchemy.Column("deed_num", sqlalchemy.String),
    sqlalchemy.Column("size", sqlalchemy.String),
    sqlalchemy.Column("house_num", sqlalchemy.String),
    sqlalchemy.Column("sub_district", sqlalchemy.String),
    sqlalchemy.Column("district", sqlalchemy.String),
    sqlalchemy.Column("province", sqlalchemy.String),
    sqlalchemy.Column("owner", sqlalchemy.String),
    sqlalchemy.Column("case_owner", sqlalchemy.String),
    sqlalchemy.Column("contact", sqlalchemy.String),
    sqlalchemy.Column("idiom_owner", sqlalchemy.String),
    sqlalchemy.Column("sale_place", sqlalchemy.String),
    sqlalchemy.Column("price_from_expert", sqlalchemy.Integer),
    sqlalchemy.Column("price_from_led", sqlalchemy.Integer),
    sqlalchemy.Column("price_from_led_em", sqlalchemy.Integer),
    sqlalchemy.Column("price_from_committee", sqlalchemy.Integer),
)


class TypeCreate(BaseModel):
    court: str
    case_num: str
    plaintiff: str
    defendant: str
    prop_type: str
    deed_num: str
    size: str
    house_num: str
    sub_district: str
    district: str
    province: str
    owner: str
    case_owner: str
    contact: str
    idiom_owner: str
    sale_place: str
    price_from_expert: Optional[int]
    price_from_led: Optional[int]
    price_from_led_em: Optional[int]
    price_from_committee: Optional[int]


class Type(TypeCreate):
    id: int

    class Config:
        orm_mode = True


crud = Crud(database, model)


def query_all(whereClause=None, ):
    return crud.query_all(whereClause)


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
