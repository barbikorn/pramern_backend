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


table_name = 'consignment_prop'
table = Crud(table_name)






def insert_record(record):
    return table.insert_record(record)

def get_all(whereClause=None):
    return table.get_all(whereClause)

def get_record(id):
    return table.get_record(id)

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



## มี 14 column
##เปลี่ยน prop_type เป็น int (0,1,2)(ที่เปล่า สิ่งปลูกสร้าง ห้องชุด)




# shp_table = sqlalchemy.Table(
#         'shp_1',
#         metadata,
#         sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
#         sqlalchemy.Column("name", sqlalchemy.String),
#         sqlalchemy.Column('properties', sqlalchemy.String),
#         sqlalchemy.Column('geom', geoalchemy2.Geometry),
#         # sqlalchemy.Column('point', geoalchemy2.Geometry('POINT')),
#         # sqlalchemy.Column('line', geoalchemy2.Geometry('LINESTRING')),
#         # sqlalchemy.Column('poly', geoalchemy2.Geometry('POLYGON')),
#         sqlalchemy.Column("category_id", sqlalchemy.Integer),
#     )
    