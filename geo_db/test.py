import sys
geo_db_path = "/home/tanakrit_tiger/senior/geo_db/tables"

sys.path.append(geo_db_path)

import BKK_led
import shp
import category
import geoalchemy2
from geoalchemy2 import func

#FOR TEST FACILITY
test_geom = "POINT (100.5561 13.8958)"
# test_geom1 = "POINT (100.523186 13.736717)"
# test_geom2 = "POINT (100.6473777 13.9913317)"
# test_geom3 = "POINT (100.523186 13.736717)"

# test_geom1 = func.ST_GeomFromText(test_geom1,4326)
# test_geom2 = func.ST_GeomFromText(test_geom2,4326)
# test_geom3 = func.ST_GeomFromText(test_geom3,4326)



# # list_prop1 = shp.find_distance_to_nearby_cat(test_geom1,161,2000)
# # list_prop2 = shp.find_distance_to_nearby_cat(test_geom1,162,2000)
# # list_prop3 = shp.find_distance_to_nearby_cat(test_geom2,164,10000)
# list_prop4 = shp.find_distance_to_nearby_cat(test_geom3,155,2000)
# list_prop5 = shp.find_distance_to_nearby_cat(test_geom3,164,2000)

# # print(list_prop1)
# # print(list_prop2)
# # print(list_prop3)
# print(list_prop4)
# print(list_prop5)

input_data1 = {  
  "geom" : "POINT (100.523186 13.736717)" ,
  "cat_id" : 161 ,
  "buffer_size": 1000
}
input_data2 = {  
  "geom" : "POINT (100.523186 13.736717)" ,
  "cat_id" : 162  ,
  "buffer_size": 1000
}
input_data3 = {  
  "geom" : "POINT (100.6473777 13.9913317)" ,
  "cat_id" : 164 ,
  "buffer_size": 1000
}
# list_prop = shp.get_naerby_facility


#TEST SHP
# list_prop = shp.find_distance_to_nearby_cat(test_geom,166)
# list_prop = shp.find_distance_to_nearby_cat(test_geom,161,20000)
list_prop = shp.get_naerby_facility(test_geom,161,20000)
print(list_prop)


# dis = shp.find_nearest_cat_distance(test_geom,161)
# dis = shp.find_nearest_cat_distance(test_geom,166)
# print(dis)


#TEST category

# category = category.get_all()
# # category = category.get_record(167)
# print(category)





# out_record = {}
# out_record['distance'] = {}
# out_record['distance']['department_store'] = shp.find_nearest_cat_distance(test_geom,162)
# print('fin1')
# out_record['distance']['market'] = shp.find_nearest_cat_distance(test_geom,166)
# print('fin2')
# out_record['distance']['public_park'] = shp.find_nearest_cat_distance(test_geom,175)
# print('fin3')

# ###use school instead of university because not have university shapefile
# out_record['distance']['bma_school'] = shp.find_nearest_cat_distance(test_geom,155)
# print('fin4')
# out_record['distance']['bts_station'] = shp.find_nearest_cat_distance(test_geom,161)
# print('fin5')

# print(out_record)


# BKK_led.get_by_buffer_in_meter("POINT (100.5561 13.8958)")