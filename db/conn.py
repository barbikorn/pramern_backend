import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base

DB_URL = 'postgresql://postgres:asdfjkLL123@34.126.65.172:5432/re_investor_tool'
engine = sqlalchemy.create_engine(DB_URL, echo=False)
database = engine.connect()

metadata = sqlalchemy.MetaData()

### Section create Table from model ###
#Base = declarative_base()


def createTables():
    # Base.metadata.create_all(bind=engine)
    metadata.create_all(bind=engine)
