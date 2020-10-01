
from bot.helpers import global_state
from .base import DataBase
from .entities import Order

def create_order(user_id,customer_name, customer_secondname,customer_phone,customer_email, 
                ordertype_id,orderstatus_id,unique_order_id,boxberry_track_number=None,papersize_id=None):
    database = DataBase()

    conn = database.get_conn

    cursor = conn.cursor()
    if(boxberry_track_number == None):
        cursor.execute(f'''
            INSERT INTO KZRBotDb.dbo.[Order](CustomerName,CustomerLastname,CustomerPhone,CustomerEmail,OrderTypeId,OrderStatusId,UniqueOrderId)
            OUTPUT Inserted.Id
            VALUES ('{customer_name}','{customer_secondname}','{customer_phone}','{customer_email}',{ordertype_id},{orderstatus_id},'{unique_order_id}')
        ''')

    if(boxberry_track_number != None):
        cursor.execute(f'''
            INSERT INTO KZRBotDb.dbo.[Order](CustomerName,CustomerLastname,CustomerPhone,CustomerEmail,OrderTypeId,OrderStatusId,UniqueOrderId)
            OUTPUT Inserted.Id
            VALUES ('{customer_name}','{customer_secondname}','{customer_phone}','{customer_email}',{ordertype_id},{orderstatus_id},'{unique_order_id}')
        ''')  
    order_id = cursor.fetchone()[0]
    cursor.commit()

    items = global_state[user_id].element_counters

    for key in items:
        if(items[key][1] == 0):
            continue
        
        item_amount = items[key][1]
        cursor.execute(f'''
            INSERT INTO KZRBotDb.dbo.OrderItem(OrderId, ItemId, Amount)
            VALUES ({order_id}, {key}, {item_amount})
        ''')
        cursor.commit()

