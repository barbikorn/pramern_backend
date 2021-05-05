import sys
db_path = "/home/tanakrit_tiger/senior/db/tables"
geo_db_path = "/home/tanakrit_tiger/senior/geo_db/tables"
sys.path.append(db_path)
sys.path.append(geo_db_path)
import BKK_led
import shp
import geoalchemy2
from geoalchemy2 import func

from typing import List, Optional
import datetime

from fastapi import APIRouter
from pydantic import BaseModel
import sqlalchemy
from sqlalchemy import MetaData
import json


# import numpy as np

#เพิ่ม 2 key เข้าทุก record 1. distance 2. score

class WQS :
#for location same subdistrict w = 5 same only distric w = 4
#input : {"type": ..., "geom": ...}
# 1 random หาที่จากเขตเดียวกัน
    def __init__(self,record:dict):
        self.record = record
        # self.record['geom'] = 'SRID=4326;'+ self.record['geom']
        self.record['geom'] = func.ST_GeomFromText(self.record['geom'],4326)
        #insert factor to selfrecord
        self.record = self.insert_dis_factor(self.record)
        print("insert dis factor to self.record complete")
        self.show_calculate = False
        self.setting = {
            "show_comparetor" : True 
        }
        #read main factor for prop type from ini 
        # self.appr_rule = read_init("wqs.ini")

        self.factor_weight = {
            "location" : 50 ,
            "distance" : [ 10 , 10 , 5 , 5 , 5] ,
            "area" : 15 ,
            }
        # 5: dis +-300 and area +- 500 
        self.item_weight_rule = {
            5 : [300 ,500],                 # weight = 5 when distance +-300
            4 : [500,800],
            3 : [1000,1500]
        }
        "where district = "
        #must in ini file 
        self.comparetor_num = 5
        print("start finding ",self.comparetor_num," comparetor")
        self.comparetors = self.find_all_comparetor(self.record)
        if self.setting['show_comparetor'] :
            self.record["comparetors"] = self.comparetors
        print("finish finding")
        self.cal_apprisal_price()




        
        # self.record['distance']['department_store'] = self.distance_to_nearest_cat(record,138)["lowest_distance"]
        
    ##กำหมดตรงนี้ด้วยfactor หลัก
    #155 => bma_school
    #161 => BTS-station
    #162 => department_store
    #166 => market
    #175 =>public_park

    #this func for only comparetor record
    #give score to all comparetor record
    def insert_factor_score(self,record):
        
        record = self.cal_distance_score(record)
        record = self.cal_area_score(record)
        record = self.cal_locate_score(record)
        record = self.cal_avg_score(record)

        return record
    #this for both self and comparetor record

    #กำหนดตรงนี้ว่า distance มี factorอะไรบ้าง
    def insert_dis_factor(self,record):

        out_record = record
        out_record['distance'] = {}
        out_record['distance']['department_store'] = shp.find_nearest_cat_distance(record['geom'],162)
        out_record['distance']['market'] = shp.find_nearest_cat_distance(record['geom'],166)
        out_record['distance']['public_park'] = shp.find_nearest_cat_distance(record['geom'],175)
        
        ###use school instead of university because not have university shapefile
        out_record['distance']['bma_school'] = shp.find_nearest_cat_distance(record['geom'],155)
        out_record['distance']['bts_station'] = shp.find_nearest_cat_distance(record['geom'],161)

        return out_record

    # def insert_dis_factor(self,record):
    #     out_record = record
    #     out_record['distance'] = {}
    #     out_record['distance']['department_store'] = self.distance_to_nearest_cat(record,162)["lowest_distance"]
    #     out_record['distance']['market'] = self.distance_to_nearest_cat(record,166)["lowest_distance"]
    #     out_record['distance']['public_park'] = self.distance_to_nearest_cat(record,175)["lowest_distance"]
        
    #     ###use school instead of university because not have university shapefile
    #     out_record['distance']['bma_school'] = self.distance_to_nearest_cat(record,155)["lowest_distance"]
    #     out_record['distance']['bts_station'] = self.distance_to_nearest_cat(record,161)["lowest_distance"]
    #     return out_record


    def check_best_comparetor(self,record,comparetor_num):

        return
    # def find_all_comparetor(self,record):
    #     comparetors = []
    #     all_comparetor = []
    #     ##FIND SAME LOCATION
    #     comparetor_records = self.find_from_sub_district(record)
    #     if len(comparetor_records) < self.comparetor_num :
    #         comparetor_records = self.find_from_district(record)

    #     for c_record in comparetor_records :
    #         c_record = self.insert_factor_score(c_record)
    #         # print(c_record)
    #         # print(record)
    #         if c_record['prop_type'] == record['prop_type'] :
    #             all_comparetor.append(c_record)
    #     all_comparetor = self.sort_comparetors(all_comparetor)
        
    #     # print(all_comparetor)
    #     if len(all_comparetor) >= self.comparetor_num :
    #         for i in range(self.comparetor_num - 1 ):
    #             comparetors.append(all_comparetor[i])
    #     else :
    #         for com in all_comparetor :
    #             comparetors.append(com)

    #     print("find comparetors complete")
    #     return comparetors

    def find_all_comparetor(self,record):
        comparetors = []
        all_comparetor = []
        ##FIND SAME LOCATION
        comparetor_records = self.find_from_sub_district(record)
        if len(comparetor_records) < self.comparetor_num :
            comparetor_records = self.find_from_district(record)

        for c_record in comparetor_records :
            c_record = self.insert_factor_score(c_record)
            # print(c_record)
            # print(record)
            if c_record['prop_type'] == record['prop_type'] :
                all_comparetor.append(c_record)
        all_comparetor = self.sort_comparetors(all_comparetor)
        
        # print(all_comparetor)
        if len(all_comparetor) >= self.comparetor_num :
            for i in range(self.comparetor_num - 1 ):
                comparetors.append(all_comparetor[i])
        else :
            for com in all_comparetor :
                comparetors.append(com)

        print("find comparetors complete")
        return comparetors

    def sort_comparetors(self,comparetor_list):
        comparetor_list = sorted(comparetor_list, key = lambda i: i['avg_score'],reverse=True)
        return comparetor_list
    def get_comparetor(self):
        print("total comparetor = ",len(self.comparetors))
        return self.comparetors

        # for record in comparetor_records :
        #     if record['district'] = self.record['district'] and record['sub_district'] == self.record['sub_district']


        #check dis from hospital  
        # for record in comparetor_records:

    #ให้คะแนนเทียบกับ self.record
    def give_score(self):
        return 

    def apprisal(self):
        return






    # type0 = location**   type 2 = size type2 = distance 
    def check_score(self,value,type):
        if tpye == 1 :
            return



    def get_by_buffer(self,cat_id,buffer_size=100000):
        print("start finding all buffer")
        results = shp.get_by_buffer(self.record['geom'],buffer_size)
        output = []
        for record in results :
            r_record = dict(record.items())
            if r_record['category_id'] == cat_id :
                output.append(r_record)
        results = self.buffer_in_meter(output,buffer_size)
        for i in results :
            i['geom'] = self.convert_wkb(i['geom'])

        print("finish finding all cat_id: ",cat_id, "in distance",buffer_size, "meters" )
        return results
        

    def buffer_in_meter(self,in_buffer,buffer_size):
        output = []
        for record in in_buffer :
            distance = self.find_distance(record['geom'])
            if distance < buffer_size :
                record['distance'] = distance
                output.append(record)
        return output

    ## need tot return in form of normal list
    def find_from_sub_district(self,record):
        new_records = []
        #find prop  in same sub district
        results = BKK_led.get_by_sub_disctrict(record['sub_district'])
        for record in results :
            record = dict(record.items())
            new_records.append(record)

        return new_records


    #return normal LIST with normal record
    def find_from_district(self,record):
        new_records = []
        #find prop  in same sub district
        ressults = BKK_led.get_by_disctrict(record['district'])
        for record in results :
            record = dict(record.items())
            new_records.append(record)

        return new_records


    def self_distance_to_nearest_cat(self,cat_id,buffer_size=1000):
        return self.distance_to_nearest_cat(self.record,cat_id,buffer_size)

    def distance_to_nearest_cat(self,record,cat_id,buffer_size=1000):
        results = shp.get_by_buffer(record['geom'],buffer_size)
        lowest_dis = 100000
        lowest_item = 'No item'

        for n_record in results :
            r_record = dict(n_record.items())
            if r_record['category_id'] == cat_id :
                #check if distance is lowest
                diff = shp.find_distance(record['geom'],r_record['geom'])
                if diff < lowest_dis :
                    lowest_dis = diff
                    lowest_item = r_record
                # recs_in_buffer.append(record)
        lowest = {
            "lowest_item":lowest_item ,
            "lowest_distance":lowest_dis
        }

        return lowest

        # def distance_to_nearest_cat(self,record,cat_id,buffer_size=1000):
        # results = shp.get_by_buffer(record['geom'],buffer_size)
        # lowest_dis = 100000
        # lowest_item = 'No item'

        # for n_record in results :
        #     r_record = dict(n_record.items())
        #     if r_record['category_id'] == cat_id :
        #         #check if distance is lowest
        #         diff = shp.find_distance(record['geom'],r_record['geom'])
        #         if diff < lowest_dis :
        #             lowest_dis = diff
        #             lowest_item = r_record
        #         # recs_in_buffer.append(record)
        # lowest = {
        #     "lowest_item":lowest_item ,
        #     "lowest_distance":lowest_dis
        # }

        # return lowest

    def find_distance(self,geom):
        return abs(shp.find_distance(self.record['geom'],geom))


    # def find_distance(geom1,geom2):
    #     return 

    def check_weight(record):
        main_factor = []
        max_weight = len(main_factor) * 5
        ##
    def cal_top_comparetor(com_num):
        return 

    def convert_wkb(self,wkb):
        return shp.convert_wkb(wkb)

# x = [location,color,bts_distance]
# weight = 

# find_similar():

# find_nearest_hospital():

    ###CALCULATE WEIGHT(SCORE QUALITY) FOR EVERY FACTOR
    ##devide score into three type เทียบกับ self.record
    #SCORE FORM 3-5
    #retrun เพิ่มrecord['dis_score] => []
    def cal_distance_score(self,record):
        record = self.insert_dis_factor(record)
        dis_score = []
        distance_record = record['distance']
        for key in distance_record :
            diff = abs(distance_record[key] - self.record['distance'][key])
        
            if diff < 500 :
                dis_score.append(5)
            elif diff < 1000 :
                dis_score.append(4)
            elif diff < 1500 :
                dis_score.append(3)
            else :
                dis_score.append(0)
        record['dis_score'] = dis_score
        
        return record
    
    
    # def cal_distance_score(distance1:float,distance2:float):
    #     diff = abs(distance1 - distance2)
    #     if diff < 500 :
    #         return 5
    #     elif diff < 1000 :
    #         return 4
    #     elif diff < 1500 :
    #         return 3
    #     else :
    #         return 0
    
    def cal_area_score(self,record):
        diff = abs(float(record['size'])-float(self.record['size']))
        if diff < 500 :
            record['area_score'] = 5
        elif diff < 1000 :
            record['area_score'] = 4
        elif diff < 1500 :
            record['area_score'] = 3
        else :
            record['area_score'] = 0

        return record 

    #5 if same district and subdistrict    


    # def cal_locate_score(self,record) :
    #     if self.record['province'] == record['province']  :
    #         loc_score = 3
    #         if self.record['district'] == record['district'] :
    #             loc_score = 4
    #             if self.record['sub_district'] == record['sub_district'] :
    #                 loc_score = 5
    #         elif self.record['sub_district'] == record['sub_district'] :
    #             loc_score = 4

    #     record['loc_score'] = loc_score
    #     return record


    def cal_locate_score(self,record) :
        if self.record['province'] == record['province']  :
            loc_score = 3
            if self.record['district'] == record['district'] :
                loc_score = 4
                if self.record['sub_district'] == record['sub_district'] :
                    loc_score = 5
            elif self.record['sub_district'] == record['sub_district'] :
                loc_score = 4

        record['loc_score'] = loc_score
        return record

    #for self.record only
    def cal_avg_score(self,record):
        # 2 is loc and area score 
        # len(record['dis_score'])
        full_score = 100

        LrxW = record['loc_score'] * self.factor_weight['location']
        ArxW = record['area_score'] * self.factor_weight['area']
        sum_score = LrxW + ArxW

        if len(self.factor_weight['distance']) != len(record['dis_score']):
            print('number of weight not equal to number of diatance factor in record')
            record['avg_score'] = -1
            record['full_score'] = -1        
        else: 
            for i in range(len(record['dis_score'])) : 
                SxW = record['dis_score'][i] * self.factor_weight['distance'][i]
                sum_score = sum_score + SxW
            avg_score = sum_score/full_score
            
            record['avg_score'] = avg_score
        return record


    def cal_apprisal_price(self):
        print('start apprisal')
        #chance size in record from string into float
        #change geom to wkt
        self.record['size'] = float(self.record['size'])
        self.record['geom'] = self.convert_wkb(self.record['geom'])
        total_weight = 0
        total_price = 0

        for i in self.comparetors :
            n = 0
            sum_price = 0
            weight = float(i['avg_score'])
            i['size'] = float(i['size'])
            if i['price_from_expert'] is not None :
                i['price_from_expert'] = float(i['price_from_expert'])
                n = n + 1
                sum_price = sum_price + i['price_from_expert']  
            if i['price_from_led'] is not None :
                i['price_from_led'] = float(i['price_from_led'])
                n = n + 1
                sum_price = sum_price + i['price_from_led']  
            if i['price_from_led_em'] is not None :
                i['price_from_led_em'] = float(i['price_from_led_em'])
                n = n + 1
                sum_price = sum_price + ['price_from_led_em']  
            if i['price_from_committee'] is not None :
                i['price_from_committee'] = float(i['price_from_committee'])
                n = n + 1
                sum_price = sum_price + i['price_from_committee']  
            avg_price = sum_price / n
            price_on_sqM = avg_price / i['size'] 
            total_price = total_price + ( price_on_sqM  * weight )
            total_weight = total_weight + weight

        appr_price = total_price/total_weight
        self.record['appr_price_on_sqm'] = appr_price
        self.record['appr_price'] = appr_price * self.record['size']
        print('finish apprisal')
    
    def get_appr_price(self):
        record = {
            "appr_price_on_sqm":self.record['appr_price_on_sqm'],
            "appr_price"   :  self.record['appr_price']
         }
        return record


        
    # def cal_area_score():
    #     if diff < 500 :
    #         return 5
    #     elif diff < 1000 :
    #         return 4
    #     elif diff < 1500 :
    #         return 3
    #     else :
    #         return 0

test_data = {
        'province'    :   'กรุงเทพฯ',
        'district'    :   'หลักสี่',
        'sub_district' :   'ทุ่งสองห้อง',
        'size'        :   '25',
        'prop_type'        :   1,
        'cit_plan_color': 'red',
        'geom'        :   "POINT (100.5561 13.8958)" ,
    }   




router = APIRouter()


@router.post("/")
def read_category(request):
    record = json.loads(request)
    wqs = WQS(record)
    result = wqs.get_appr_price()
    return json.dumps(result)



####calculate and add new key to self.record 

