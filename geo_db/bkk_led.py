import crud

table = crud.Crud('shp_test')


def insert_record(record):
    return table.insert_record(record)


def get_record(id):
    return table.get_record(id)

def get_by_buffer(geom):
    return table.get_by_buffer(geom)




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
    