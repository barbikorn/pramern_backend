import sqlalchemy
from sqlalchemy import and_
import geoalchemy2 
from geoalchemy2 import func


import sys
db_path = "/home/tanakrit_tiger/senior/geo_db"
sys.path.append(db_path)

from geo_crud import Crud
from geo_crud import connection 




table_name = 'BKK_led'
table = Crud(table_name)
## มี 14 column
##เปลี่ยน prop_type เป็น int (0,1,2)(ที่เปล่า สิ่งปลูกสร้าง ห้องชุด)


def insert_record(record):
    return table.insert_record(record)

def get_all(whereClause=None):
    return table.get_all(whereClause)

def get_record(id):
    return table.get_record(id)

def find_distance_to_nearby_prop(geom,buffer_size=2000):
    sql =  sqlalchemy.select(
                    [func.ST_Distance(
                        func.ST_Transform(geom,3857),
                        func.ST_Transform(table.model.c.geom,3857)
                        ),table.model.c.id
                    ]
                ).where(
                    and_(
                        func.ST_Distance(
                            func.ST_Transform(geom,3857),
                            func.ST_Transform(table.model.c.geom,3857)
                        ) < buffer_size 
                    )

                )
    result = connection.execute(sql).fetchall()

    return result
def find_nearest_prop_distance(geom,cat_id):
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

# def get_by_buffer(input_geom,buffer_size = "10"):
#     sql = table.model.select().where(func.ST_Intersects(func.ST_setsrid(func.ST_Buffer(func.ST_GeomFromText(input_geom),buffer_size,"quad_segs=8"),4326),func.ST_setsrid(table.model.c.geom,4326)))
#     # new_geom = func.ST_GeomFromText(geom)
#     results =  connection.execute(sql).fetchall()
#     return results


def find_distance_to_nearby_prop(geom,cat_id,buffer_size=2000):
    sql =  sqlalchemy.select(
                    [func.ST_Distance(
                        func.ST_Transform(geom,3857),
                        func.ST_Transform(table.model.c.geom,3857)
                        )
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



def get_by_sub_disctrict(sub_district):
    sql = table.model.select().where(table.model.c.sub_district == sub_district )  
    results = connection.execute(sql).fetchall()
    return results

def get_by_disctrict(district):
    sql = table.model.select().where(table.model.c.district == district )  
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
    