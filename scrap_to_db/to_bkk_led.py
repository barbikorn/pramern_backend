# ต้องใส่ column geom กับ สี ให้
# เปลี่ยนขนาดที่ดินเป็นตัวเลข
import sys
db_path = "/home/tanakrit_tiger/senior/db/tables"
geo_db_path = "/home/tanakrit_tiger/senior/geo_db/tables"
sys.path.append(db_path)
sys.path.append(geo_db_path)

import from_led
import shp
import BKK_led
from geoalchemy2 import func
import re
import csv


def change_size_unit(size_str):
    rai_units = ["ไร่"]
    ngan_units = ["งาน"]
    sqm_units = ["ตร.วา/ตร.ม."]
    number = '\d+[.,]?\d*'                              # pattern for number
    plus_minus = '\+\/\-'                               # plus minus

    rai_cases = fr'({number})(?:[\s\d\-\+\/]*)(?:{rai_units})'
    rai_pattern = re.compile(rai_cases)
    try :
        rai = float(rai_pattern.findall(size_str)[0])
    except :
        rai = 0

    ngan_cases = fr'({number})(?:[\s\d\-\+\/]*)(?:{ngan_units})'
    ngan_pattern = re.compile(ngan_cases)
    try:        
        ngan = float(ngan_pattern.findall(size_str)[0])
    except :
        ngan = 0

    sqm_cases = fr'({number})(?:[\s\d\-\+\/]*)(?:{sqm_units})'
    sqm_pattern = re.compile(sqm_cases)
    try :
        sqm = float(sqm_pattern.findall(size_str)[0])
    except :
        sqm = 0
    
    sum_sqm = (rai * 1600)+(ngan * 400)+(sqm)

    return  sum_sqm
# print(from_led_record_bkk[0])

def dummy_geom_from_district(record):
    record = record
    subdistrict = record[9]
    geom = shp.random_point_from_district(record['district'])
    record.append(geom)

def get_color_by_geom(geom):
    color = "red"
    return color

def change_prop_type(prop_type:str):
    if prop_type == ' ที่ดินว่างเปล่า':
        return 1
    if prop_type == ' ที่ดินพร้อมสิ่งปลูกสร้าง':
        return 2
    if prop_type == ' ห้องชุด' :
        return 3
    else :
        return 4

def arrange_record(record):
    new_record = {}
    for key in record :
        if key == "id" :
            new_record["o_id"] = record[key]
        else :
            new_record[key] = record[key]

    new_record['size'] = change_size_unit(str(new_record['size']))
    district = "เขต" + record['district'].strip()
    geom = shp.random_point_from_district(district)
    color = get_color_by_geom(geom)
    new_record['prop_type'] = change_prop_type(record['prop_type'])
    new_record['color'] = color
    new_record['geom'] = geom

    ##drop group
    new_record.pop("owner",None)
    new_record.pop("plaintiff",None)
    new_record.pop("house_num",None) 
    new_record.pop("case_owner",None)
    new_record.pop("idiom_owner",None)
    new_record.pop("sale_place",None)
    new_record.pop("case_num",None)
    new_record.pop("case_num",None)
    new_record.pop("defendant",None)
    new_record.pop("contact",None)
    new_record.pop("court",None)
    #strip space
    for key in new_record :
        try : 
            new_record[key] = new_record[key].lstrip()
        except :
            pass
    return new_record

def add_geom_color_to_record(records):
    new_records = []
    for record in records:
        record = arrange_record(record)
        new_records.append(record)
    return new_records

def insert_all(records):
    for record in records :
        BKK_led.insert_record(record)

    return True

if __name__ == '__main__':

    bkk_records  =  from_led.query_all(whereClause="province=' กรุงเทพฯ'")
    new_bkk_records = []
    for record in bkk_records :
        record = dict(record.items())
        new_record = arrange_record(record)
        # print(new_record['geom'])
        # for key in new_record:
        #     print(key,type(new_record[key]))
        # break

        # print(new_record['size'])
        # break
        BKK_led.insert_record(new_record)
    print("finish")
        
    # new_bkk_records = add_geom_color_to_record(bkk_records)
    # insert_all(new_bkk_records)
    # print(new_bkk_records[0])

    
    #record have 21 column 
    #column 22 เป็น สี
    #column 23 เป็น geom
    
    
    
        
    # print(len(bkk_records))




# def gen_geom(subdistrict:str):

    
#     shp



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
    