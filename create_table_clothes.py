from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Boolean
from datalayer.database import engine

def SetClothesDB():
    metadata = MetaData(bind=engine)
    existing_table = Table('Clothes', metadata, autoload=True)

    # ADD LATER TO CHECK AND ADD ALL COLUMNS
    columns_to_add = [
        Column('hue', Integer),
        Column('saturation', Integer),
        Column('value', Integer),
        Column('tone', Integer),
        Column('colortemp', Integer)
    ]

    for column in columns_to_add:
        if not hasattr(existing_table.c, column.name):
            column.create(existing_table)

    metadata.create_all(engine)

if __name__ == "__main__":
    SetClothesDB()
