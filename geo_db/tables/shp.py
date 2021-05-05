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


table_name = 'shp_test'
table = Crud(table_name)






def insert_record(record):
    return table.insert_record(record)

def get_all(whereClause=None):
    return table.get_all(whereClause)

def get_record(id):
    return table.get_record(id)

# def get_by_buffer(input_geom,cat_id=None,buffer_size = "10"):   
#     return table.get_by_buffer(input_geom,buffer_size,cat_id)

def get_by_category_id(input_id):
    sql = table.model.select().where(self.model.c.category_id == input_id )  
    results = connection.execute(sql).fetchall()
    return results

def get_by_category_id_and_name(input_id,input_name):
    sql = table.model.select().where(and_(self.model.c.category_id == input_id,self.model.c.name == input_name) )  
    results = connection.execute(sql).fetchall()
    return results

#####not done
def get_nearest_in_cat(cat_id):
    sql = table.model.select
    return result

def random_point_from_district(d_name:str):
    district_cat_id = 163
    sql = sqlalchemy.select(
                [func.ST_SetSRID(
                    func.ST_GeneratePoints(
                        table.model.c.geom,1),4326)]).where(
                                and_(
                                    table.model.c.name == d_name,
                                    table.model.c.category_id == district_cat_id))
    result = connection.execute(sql).fetchone()
    if result is not None:
        return result[0]
    else :
        return print('None')

#transportation -> cat_id:
#   

def find_distance(geom1,geom2):
    return table.find_distance(geom1,geom2)


#NEWW GET BY BUFFER
def find_distance_to_nearby_cat(geom,cat_id,buffer_size=2000):
    sql =  sqlalchemy.select(
                    [func.ST_Distance(
                        func.ST_Transform(geom,3857),
                        func.ST_Transform(table.model.c.geom,3857)
                        ),table.model.c.name
                    ]
                ).where(
                    and_(
                        func.ST_Distance(
                            func.ST_Transform(geom,3857),
                            func.ST_Transform(table.model.c.geom,3857)
                        ) < buffer_size ,
                        table.model.c.category_id == cat_id
                    
                    )

                )
    result = connection.execute(sql).fetchall()

    return result

#if no item return None

def find_nearest_cat_distance(geom,cat_id):
    records = find_distance_to_nearby_cat(geom,cat_id)
    new_buffer = 20000
    if len(records) == 0 :
        records = find_distance_to_nearby_cat(geom,cat_id,new_buffer)
    min_num =  new_buffer
    
    for i in records :
        if i[0] < min_num:
            min_num = i[0]
    if min_num == new_buffer :
        return None 
    else : 
        return min_num
def get_naerby_facility(geom,cat_id,buffer_size=2000):
    new_records = []
    geom = func.ST_GeomFromText(geom,4326)
    results = find_distance_to_nearby_cat(geom,cat_id,buffer_size)
    for result in results :
        new_record = {}
        new_record['name'] = result[1]
        new_record['distance'] = result[0]
        new_records.append(new_record)
    return new_records
        
    

        



def get_distance_from(cat_id):
    sql = table.model.select().where(self.model.c.category_id == input_id )  
    #create ex .( hostpitle )buffer 
    
    results = connection.execute(sql).fetchall()
    return results

def get_by_buffer(input_geom,buffer_size=100000):
        sql = table.model.select().where(
                                    func.ST_Intersects(
                                        func.ST_setsrid(
                                            func.ST_Buffer(
                                                input_geom,
                                                buffer_size,)
                                            ,4326),
                                        table.model.c.geom
                                        # func.ST_setsrid(table.model.c.geom,4326)
                                        )
                                    )

        
        # new_geom = func.ST_GeomFromText(geom)
        results =  connection.execute(sql).fetchall()
        return results

def get_by_buffer_in_meter(input_geom,cat_id,buffer_size=100000):
    print("start finding all buffer")
    if isinstance(input_geom, str):
        input_geom = func.ST_GeomFromText(input_geom,4326)
    results = get_by_buffer(input_geom,buffer_size)
    output = []
    for record in results :
        r_record = dict(record.items())
        if r_record['category_id'] == cat_id :
            output.append(r_record)
    results = buffer_in_meter(output,buffer_size,input_geom)
    for i in results :
        i['geom'] = convert_wkb(i['geom'])

    print("finish finding all cat_id: ",cat_id, "in distance",buffer_size, "meters" )
    return results


def buffer_in_meter(in_buffer,buffer_size,input_geom):
    output = []
    for record in in_buffer :
        distance = find_distance(record['geom'],input_geom)
        if distance < buffer_size :
            record['distance'] = distance
            output.append(record)
    return output





def convert_wkb(wkb):
    return table.convert_wkb(wkb)
# def get_by_buffer(input_geom,cat_id=None ,buffer_size=2000):
#         sql = table.model.select().where(
#                                     func.ST_Intersects(
#                                         func.ST_setsrid(
#                                             func.ST_Buffer(
#                                                 func.ST_GeomFromText(input_geom),
#                                                 buffer_size,
#                                                 "quad_segs=8")
#                                             ,4326),
#                                         func.ST_setsrid(table.model.c.geom,4326)
#                                         )
#                                     )

        
#         # new_geom = func.ST_GeomFromText(geom)
#         if cat_id is not None :
#             sql = table.model.select().where(
#                                             and_(
#                                                 func.ST_Intersects(
#                                                     func.ST_setsrid(
#                                                         func.ST_Buffer(
#                                                             func.ST_GeomFromText(input_geom),
#                                                             buffer_size,
#                                                             "quad_segs=8"),4326),
#                                                     func.ST_setsrid(table.model.c.geom,4326)),
#                                                 table.model.c.category_id == cat_id
#                                                 )
#                                         )
#         results =  connection.execute(sql).fetchall()
#         return results


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
#     )router = APIRouter()


router = APIRouter()


# @router.get("/", response_model=List[Type])
# def read_category():
#     records = query_all()
#     return records

# @router.get("/")
# def read_category():
#     records = get_all()
#     return records


#
#input data = {
#   'geom' : ,
#   'cat_id' : ,
# }


#ได้มาเป็น tuple ของ รหัส
@router.post("/buffer")
def read_category(request):
    record = json.loads(request)
    return json.dumps(get_naerby_facility(func.ST_GeomFromText(record['geom'],4326),record['cat_id'],record['buffer_size']))


@router.get("/{id}")
def read_category_by_id(id: int):
    return get_record(id)


# @router.post("/", response_model=Type)
# def create_category(request: TypeCreate):
#     record = request.dict()
#     return insert_record(record)


# @router.put("/{id}", response_model=Type)
# def update_category(id: int, request: TypeCreate):
#     record = request.dict()
#     return update_record(id, record)


# @router.delete("/{id}", response_model=int)
# def delete_category(id: int):
#     return delete_record(id)
