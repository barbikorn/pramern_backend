import sqlalchemy

#oนำpagesize dับ offset ออก

class Crud:

    def __init__(self, database, model):
        self.database = database
        self.model = model
        # self.page_size = page_size

        
    # def query_all(self, whereClause=None, page_no: int = 0, page_size=None, order_by=None):
    def query_all(self, whereClause=None, order_by=None):
        sql = self.model.select()

        if whereClause is not None:
            sql = sql.where(sqlalchemy.sql.text(whereClause))

        records = self.database.execute(sql).fetchall()
        # print(records)
        return records

    def query_by_id(self, id):
        sql = self.model.select().where(self.model.c.id == id)
        return self.database.execute(sql).fetchone()

    def insert_record(self, record):
        sql = self.model.insert(None).values(
            **record).returning(self.model.c.id)
        last_record_id = self.database.execute(sql).fetchone()[0]

        # return result

        # last_record_id = result.lastrowid
        # print(result)
        # last_record_id = self.database.execute(sql) #sqlite
        return self.query_by_id(last_record_id)

    def update_record(self, id, record):
        sql = self.model.update(None).values(
            **record).where(self.model.c.id == id)
        self.database.execute(sql)
        return self.query_by_id(id)
        #result = self.database.execute(sql)
        # print(result)
        # success
        # if result == 1:
        #     return self.query_by_id(id)
        # else:
        #     return None

    def delete_record(self, id):
        sql = self.model.delete(None).where(self.model.c.id == id)
        return self.database.execute(sql).rowcount

    