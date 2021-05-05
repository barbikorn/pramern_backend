from typing import List, Optional
import datetime
import json
from fastapi import APIRouter
from pydantic import BaseModel
import sqlalchemy

from sqlalchemy import and_
import geoalchemy2 
from geoalchemy2 import func


import sys
db_path = "/home/tanakrit_tiger/senior/geo_db"
sys.path.append(db_path)

from geo_crud import Crud
from geo_crud import connection


table_name = 'category'
table = Crud(table_name)






def insert_record(record):
    return table.insert_record(record)

def get_all(whereClause=None):
    newlist = []
    result = table.get_all(whereClause)
    for i in result :
        i = dict(i.items())
        newlist.append(i)
    return newlist

def get_record(id):
    result = table.get_record(id)
    return dict(result.items())

def delete_record(id):
    return table.delete_record(id)



consignment_data = {
        'province'    :   'กรุงเทพฯ',
        'district'    :   'หลักสี่',
        'sub_district' :   'ทุ่งสองห้อง',
        'size'        :   25,
        'prop_type'        :   2,
        'cit_plan_color': 'red',
        'geom'        :   "POINT (100.5561 13.8958)" ,
        'price'   :   300000,
        'contact' : '0658885548',
        'other' : 'asdfadfadsofjadsipfjasdpifjasipf'
    }   

router = APIRouter()


# @router.get("/", response_model=List[Type])
# def read_category():
#     records = query_all()
#     return records



#
#input data = {
#   'geom' : ,
#   'cat_id' : ,
# }
@router.get("/")
def read_category():
    records = get_all()
    return records


@router.get("/{id}")
def read_category_by_id(id: int):
    return get_record(id)

@router.post("/")
def create_category(request):
    record = json.loads(request)
    return insert_record(record)


@router.put("/{id}")
def update_category(id: int,request):
    record = json.loads(request)
    return update_record(id, record)


@router.delete("/{id}", response_model=int)
def delete_category(id: int):
    return delete_record(id)


