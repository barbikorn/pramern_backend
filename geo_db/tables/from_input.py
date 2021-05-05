import sqlalchemy
from sqlalchemy import and_
import geoalchemy2 
from geoalchemy2 import func


import sys
db_path = "/home/tanakrit_tiger/senior/geo_db"
sys.path.append(db_path)

from geo_crud import Crud
from geo_crud import connection 

test_data = {
        'province'    :   'กรุงเทพฯ',
        'district'    :   'หลักสี่',
        'sub_district' :   'ทุ่งสองห้อง',
        'size'        :   '25',
        'prop_type'        :   2,
        'cit_plan_color': 'red',
        'geom'        :   "POINT (100.5561 13.8958)" ,
        'appr_type'   :   1,
    }   



table_name = 'from_input'
table = Crud(table_name)
## มี 14 column
##เปลี่ยน prop_type เป็น int (0,1,2)(ที่เปล่า สิ่งปลูกสร้าง ห้องชุด)


def insert_record(record):
    return table.insert_record(record)

def get_all(whereClause=None):
    return table.get_all(whereClause)

def get_record(id):
    return table.get_record(id)

def get_by_buffer(input_geom,cat_id=None ,buffer_size=500):
        
    sql = table.model.select().where(
                                    and_(
                                        func.ST_Intersects(
                                            func.ST_setsrid(
                                                func.ST_Buffer(
                                                    func.ST_GeomFromText(input_geom),
                                                    buffer_size,
                                                    "quad_segs=8"),4326),
                                            func.ST_setsrid(table.model.c.geom,4326)),
                                        table.model.c.category_id == cat_id
                                        )
                                    )
    # new_geom = func.ST_GeomFromText(geom)
    if cat_id is not None :
        sql = table.model.select().where(
                                        func.ST_Intersects(
                                            func.ST_setsrid(
                                                func.ST_Buffer(
                                                    func.ST_GeomFromText(input_geom),
                                                    buffer_size,
                                                    "quad_segs=8")
                                                ,4326),
                                            func.ST_setsrid(table.model.c.geom,4326)))
    results =  connection.execute(sql).fetchall()
    return results
# def get_by_buffer(input_geom,buffer_size = "10"):
#     sql = table.model.select().where(func.ST_Intersects(func.ST_setsrid(func.ST_Buffer(func.ST_GeomFromText(input_geom),buffer_size,"quad_segs=8"),4326),func.ST_setsrid(table.model.c.geom,4326)))
#     # new_geom = func.ST_GeomFromText(geom)
#     results =  connection.execute(sql).fetchall()
#     return results

def get_by_sub_disctrict(sub_district):
    sql = table.model.select().where(table.model.c.sub_district == sub_district )  
    results = connection.execute(sql).fetchall()
    return results

def get_by_disctrict(district):
    sql = table.model.select().where(table.model.c.district == district )  
    results = connection.execute(sql).fetchall()
    return results



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
    