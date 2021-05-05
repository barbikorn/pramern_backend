from fastapi import FastAPI

# import tables.conn as conn


import sys
crud_path = "/home/tanakrit_tiger/senior/geo_db"
db_path =  "/home/tanakrit_tiger/senior/geo_db/tables"
wqs_path = "/home/tanakrit_tiger/senior/DSS/market_approch"
sys.path.append(db_path)
sys.path.append(crud_path)
sys.path.append(wqs_path)

#import table 
import shp
import consignment_prop
import geo_crud
import WQS
import category
# import tables.category as category
# import tables.person as person
# import tables.student as student
# import tables.from_led as from_led

app = FastAPI()

# conn.createTables()

database = geo_crud.connection

# @app.on_event("startup")
# async def startup():
#     await database.connect()


# @app.on_event("shutdown")
# async def shutdown():
#     await database.disconnect()

app.include_router(
    shp.router,
    prefix="/shp",
    tags=["shape"],
)

app.include_router(
    WQS.router,
    prefix="/wqs",
    tags=["weight-quality-score"],
)

app.include_router(
    consignment_prop.router,
    prefix="/consignment_prop",
    tags=["รายการฝากขาย"],
)

app.include_router(
    category.router,
    prefix="/category",
    tags=["category"],
)


# app.include_router(
#     from_led.router,
#     prefix="/from_led",
#     tags=["from_led"],
#)

#to run : uvicorn main:app --localhost --port 8000 --reload
#       scrapy crawl all_page
# scrapy crawl page_data
# scrapy crawl field_page

# uvicorn main:app --reload --port 8000
#155 => bma_school
        #161 => BTS-station
        #162 => department_store
        #166 => market
        #175 =>public_park

#api
# 34.126.65.172:8000/wqs
# 34.126.65.172:8000/shp
# 34.126.65.172:8000/consignment_prop
# http://34.126.65.172

# http://127.0.0.1:8000/wqs
# http://127.0.0.1:8000/shp/buffer
# http://127.0.0.1:8000/category
#TEST FACILITY
input_data = {  
  "geom" : "POINT (100.523186 13.736717)" ,
  "cat_id" : 161 ,
  "buffer_size": 1000
}
input_data = {  
  "geom" : "POINT (100.523186 13.736717)" ,
  "cat_id" : 162  ,
  "buffer_size": 1000
}
input_data = {  
  "geom" : "POINT (100.6473777 13.9913317)" ,
  "cat_id" : 164 ,
  "buffer_size": 1000
}

test_data = {
        "province"    :   "กรุงเทพฯ",
        "district"    :   "หลักสี่",
        "sub_district" :   "ทุ่งสองห้อง",
        "size"        :   25,
        "prop_type"        :   2,
        "cit_plan_color": "red",
        "geom" : "POINT (100.5561 13.8958)" 
    }   
test_data2 = {
        "province"    :   "กรุงเทพฯ",
        "district"    :   "หลักสี่",
        "sub_district" :   "ทุ่งสองห้อง",
        "size"        :   25,
        "prop_type"        :   2,
        "cit_plan_color": "red",
        "price" : 25000,
        "contact"   :   "022211111",
        "other" : "-"
    }   
