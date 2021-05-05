import sys
wqs_path = "/home/tanakrit_tiger/senior/DSS/market_approch"

sys.path.append(wqs_path)

from WQS import WQS
import geoalchemy2
from geoalchemy2 import func

#APPR_type : 1 ->wqs
#          : 2 ->

#PROP TYPE : 1  -> Land
test_data = {
        'province'    :   'กรุงเทพฯ',
        'district'    :   'หลักสี่',
        'sub_district' :   'ทุ่งสองห้อง',
        'size'        :   '25',
        'prop_type'        :   1,
        'cit_plan_color': 'red',
        'geom'        :   "POINT (100.5561 13.8958)" ,
        'appr_type'   :   1,
    }   


# def find_appr():
#     # markte_aprpoch
#     if prop_type = 1  

# def change_prop_type(prop_type:str):
#     if prop_type == ' ที่ดินว่างเปล่า':
#         return 1
#     if prop_type == ' ที่ดินพร้อมสิ่งปลูกสร้าง':
#         return 2
#     if prop_type == ' ห้องชุด' :
#         return 3
#     else :
#         return 4

if __name__ == '__main__':
    test_geom1 = "POINT (100.523186 13.736717)"
    test_geom2 = "POINT (100.6473777 13.9913317)"
    test_geom3 = "POINT (100.523186 13.736717)"

    test_data = {
        'province'    :   'กรุงเทพฯ',
        'district'    :   'หลักสี่',
        'sub_district' :   'ทุ่งสองห้อง',
        'size'        :   '25',
        'prop_type'        :   2,
        'cit_plan_color': 'red',
        'geom'        :   "POINT (100.5561 13.8958)" ,
    }   

    test_data1 = {
        'province'    :   'กรุงเทพฯ',
        'district'    :   'หลักสี่',
        'sub_district' :   'ทุ่งสองห้อง',
        'size'        :   '25',
        'prop_type'        :   1,
        'cit_plan_color': 'yellow',
        'geom'        :   test_geom1 ,
    }   
    test_data2 = {
        'province'    :   'กรุงเทพฯ',
        'district'    :   'หลักสี่',
        'sub_district' :   'ทุ่งสองห้อง',
        'size'        :   '25',
        'prop_type'        :   2,
        'cit_plan_color': 'red',
        'geom'        :   test_geom2 ,
    }   

    test_data3 = {
        'province'    :   'กรุงเทพฯ',
        'district'    :   'หลักสี่',
        'sub_district' :   'ทุ่งสองห้อง',
        'size'        :   '25',
        'prop_type'        :   2,
        'cit_plan_color': 'red',
        'geom'        :   test_geom3 ,
    }   

    wqs3 = WQS(test_data3)
    # wqs2 = WQS(test_data2)
    #155 => bma_school
    #161 => BTS-station
    #162 => department_store
    #166 => market
    #175 =>public_park

    # print(wqs.self_distance_to_nearest_cat(175))
    #**********test part**************#
    
    # in_buffer = wqs.buffer_in_meter(in_buffer,1000)
    
    # print(in_buffer)
            
    # print(wqs.get_comparetor())
    # print(wqs.cal_area_score(wqs.comparetors[10]))
#################
        #155 => bma_school
        #161 => BTS-station
        #162 => department_store
        #166 => market
        #175 =>public_park
###################        
    print(wqs3.get_appr_price())
    # in_buffer = shp.get_by_buffer( "POINT (100.5561 13.8958)",cat_id=162,buffer_size=1000)
    # print(in_buffer)
    # print(wqs.self_distance_to_nearest_cat(138, 10000))
    # lowest_item = wqs.self_distance_to_nearest_cat(138, 10000)['lowest_item']
    # wkt = wqs.convert_wkb(lowest_item['geom'])
    # print(wkt)
    #use catid
    
    # print(wqs.)





    #comparetor rule  : same 