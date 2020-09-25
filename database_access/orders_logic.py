
from bot.helpers import global_state
from .base import DataBase
from .entities import Order

def create_order(user_id,customer_name, customer_secondname,customer_phone,customer_email, 
                ordertype_id,orderstatus_id,unique_order_id,customer_post_index=None,boxberry_track_number=None,papersize_id=None):
    database = DataBase()

    conn = database.get_conn

    cursor = conn.cursor()
    if(customer_post_index != None):
        cursor.execute(f'''
            INSERT INTO KZRBotDb.dbo.[Order](CustomerName,CustomerLastname,CustomerPhone,CustomerEmail,CustomerPostIndex,OrderTypeId,OrderStatusId,UniqueOrderId)
            OUTPUT Inserted.Id
            VALUES ('{customer_name}','{customer_secondname}','{customer_phone}','{customer_email}','{customer_post_index}',{ordertype_id},{orderstatus_id},'{unique_order_id}')
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
        if(items[key] == 0):
            continue
        
        item_amount = items[key]
        cursor.execute(f'''
            INSERT INTO KZRBotDb.dbo.OrderItem(OrderId, ItemId, Amount)
            VALUES ({order_id}, {key}, {item_amount})
        ''')
        cursor.commit()

