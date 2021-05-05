import sqlalchemy
from sqlalchemy import and_
import geoalchemy2
from geoalchemy2 import func

DATABASE_URL = 'postgresql://postgres:asdfjkLL123@34.126.65.172:5432/BKK_shape_file'
engine = sqlalchemy.create_engine(DATABASE_URL, echo=False)
connection = engine.connect()
meta = sqlalchemy.MetaData()


class Crud:

    def __init__(self, table_name):
        self.model = sqlalchemy.Table(table_name, meta, autoload=True,
                                      autoload_with=engine)

    def insert_record(self, record):
        sql = self.model.insert().values(
            **record).returning(self.model.c.id)
        last_record_id = connection.execute(sql).fetchone()[0]
        return last_record_id
    
    def get_all(self,whereClause=None):
        sql = self.model.select()
        records = connection.execute(sql).fetchall()
        # print(records)
        return records
    
    # def get_all(self,whereClause=None):
    #     sql = self.model.select()
    #     if whereClause is not None:
    #         sql = self.model.select().where(sqlalchemy.sql.text(whereClause))
    #     records = connection.execute(sql).fetchall()
    #     # print(records)
    #     return records

    def get_record(self, id):
        sql = self.model.select().where(self.model.c.id == id)
        result = connection.execute(sql).fetchone()
        return result

    def delete_record(self, id):
        sql = self.model.delete(None).where(self.model.c.id == id)
        return self.database.execute(sql).rowcount


#for shp table

#geo function 
#use 3857 to get meters unit
    def find_distance(self,geom_1,geom_2):
        sql =  sqlalchemy.select(
                    [func.ST_Distance(
                        func.ST_Transform(geom_1,3857),
                        func.ST_Transform(geom_2,3857)
                        )
                    ]
                )
        result = connection.execute(sql).fetchone()
        return result[0]
    
    def convert_wkb(self,wkb):
        sql =  sqlalchemy.select(
                    [func.ST_AsEWKT(wkb)]
                )
        result = connection.execute(sql).fetchone()
        return result[0]

    
                    
    def get_by_category_id(self,input_id):

        sql = self.model.select().where(self.model.c.category_id == input_id )  
        result = connection.execute(sql).fetchall()

        return result


    #edit category to subdistrict polygon directory
   

    # def getTable(self):
    #     return self.model
#sqlalchemy.sql.text(whereClause)


