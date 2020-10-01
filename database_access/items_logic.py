import pandas as pd

from .base import DataBase
from .entities import Item



def get_items():
    database = DataBase()
    items_list = []
    conn = database.get_conn

    cursor = conn.cursor()
    cursor.execute('SELECT * FROM KZRBotDb.dbo.Item')

    for row in cursor:
        item = Item(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
        items_list.append(item)
    
    return items_list



