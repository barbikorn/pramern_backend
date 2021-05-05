import sqlalchemy
from sqlalchemy import and_
import geoalchemy2
from geoalchemy2 import func


s = select([lake_table.c.name,
                func.ST_Area(
                    lake_table.c.geom.ST_Buffer(2)).label('bufferarea')])