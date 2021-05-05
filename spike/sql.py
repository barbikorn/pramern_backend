        sql = table.model.select().where(
                                and_(
                                    func.ST_Intersects(
                                        func.ST_setsrid(
                                            func.ST_Buffer(
                                                func.ST_GeomFromText(input_geom),
                                                buffer_size,
                                                "quad_segs=8"),4326),
                                        func.ST_setsrid(table.model.c.geom,4326)),
                                    table.model.c.category_id == cat_id)
                                                )