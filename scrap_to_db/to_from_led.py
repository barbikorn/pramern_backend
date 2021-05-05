import csv
import dblib
import tables.from_led as from_led
from tables.crud import Crud



conn = dblib.connectDb( "ini/database.ini" , "postgresql")
from_led = Crud( conn , 'from_led')
from_led.clear()

with open('all_data.csv', 'r' , encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader) #skip first row
    for row in reader:
        try : 
            row = [None if 'ไม่มี' in i else i for i in row]
            id = from_led.insert(row)
            print("add ",id ,"success")
        except : 
            print("can't add ...")


    print(from_led.get(1))
    print(from_led.get(2))
        # print(row)
    #     cur.execute(
    #     "INSERT INTO users VALUES (%s, %s, %s, %s)",
    #     row
    # )