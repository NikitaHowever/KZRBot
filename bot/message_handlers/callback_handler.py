from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from telegram.error import BadRequest
import json
import uuid

from bot.helpers import CART, global_state, DELIVERY_TYPE, BOXBERRY, CREDENTIALS_N, admin_list
from bot.command_handlers import  start
from .message_handler import message_handler
from database_access import create_order
from .utils import get_new_cart_markup, update_and_get_markup, update_message, get_payment_url, get_points, get_cities_list, create_parsel, get_regions

def increment_cart_handler(update, context):
    query = update.callback_query
    query_data = query.data
    query_data_json = json.loads(query_data)
    #print(update)
    user_id = update.callback_query.message.chat.id

    
    markup = update_and_get_markup(query_data_json['itemId'],user_id,query_data_json['price'], True)
    cart_markup = get_new_cart_markup(user_id)
    bot = context.bot

    try:
        update_message(bot, query.message.chat_id, query.message.message_id, markup)
        update_message(bot, query.message.chat_id, global_state[user_id].cart_message_id, reply_markup=cart_markup)

        return CART

    except BadRequest as e:
        print(e.message)
        return CART

def decrement_cart_handler(update, context):
    query = update.callback_query
    query_data = query.data
    query_data_json = json.loads(query_data)

    user_id = update.callback_query.message.chat.id

    markup = update_and_get_markup(query_data_json['itemId'],user_id,query_data_json['price'])

    cart_markup = get_new_cart_markup(user_id)
    if(markup == None):
        return CART

    bot = context.bot
    try:
        update_message(bot, query.message.chat_id, query.message.message_id, markup)
        update_message(bot, query.message.chat_id, global_state[user_id].cart_message_id, reply_markup=cart_markup)
        
        return CART
    except BadRequest as ex:
        print(ex.message)
        return CART

def picckup_handler(update, context):
    global_state[update.effective_chat.id].order_type = "pickup"
    
    context.bot.send_message(chat_id=update.effective_chat.id, text='Введите ваше имя')
    return CREDENTIALS_N

def boxberry_handler(update, context):
    buttons = []
    cities = get_cities_list()
    regions = get_regions(cities)
    print(regions)

    global_state[update.effective_chat.id].order_type = "boxberry"
    
    region_count = 0
    new_buttons = []

    for region in regions:
        if(region_count == 2):
            buttons.append(new_buttons)
            new_buttons = []
            region_count = 0
        callb_data = ''

        if(len(region) > 12):
            callb_data = region[0:12]
        else:
            callb_data = region
        new_buttons.append(InlineKeyboardButton(region, callback_data=f"reg={callb_data}"))
        region_count+=1

        markup = InlineKeyboardMarkup(buttons)

    context.bot.send_message(chat_id=update.effective_chat.id, text="Выберете вашу область\n", reply_markup = markup)
    return BOXBERRY

def boxberry_region_handler(update,context):
    query = update.callback_query
    query_data = query.data

    data_arr = query_data.split("=")
    city_list = get_cities_list()
    buttons = []
    back_buttons = [[]]
    back_buttons[0].append(InlineKeyboardButton("Назад", callback_data="city_code_back"))

    curr_cities = []
    city_count = 0
    new_buttons = []
    for city in city_list:
        if data_arr[1] in city["Region"]:
            if(city_count == 2):
                buttons.append(new_buttons)
                new_buttons = []
                city_count = 0
            new_buttons.append(InlineKeyboardButton(city["Name"], callback_data="city_code={}".format(city["Code"])))
            city_count+=1
    markup = InlineKeyboardMarkup(buttons)
    back_markup = InlineKeyboardMarkup(back_buttons)
    context.bot.send_message(chat_id=update.effective_chat.id, text="Выберете ваш город\n", reply_markup = markup)
    context.bot.send_message(chat_id=update.effective_chat.id, text="<-", reply_markup = back_markup)

    return BOXBERRY

def boxberry_back_handler(update, context):
    boxberry_handler(update, context)

def boxbery_city_handler(update, context):
    query = update.callback_query
    query_data = query.data

    data_arr = query_data.split("=")
    print("data_arr:{}".format(data_arr[1]))
    buttons = [[]]
    user_id = query.message.chat.id
    cities_counter = global_state[user_id].cities_counter

    if data_arr[1] != "next":
        picks = get_points(data_arr[1])
        global_state[user_id].picks = picks
        if len(picks) > 10:
            i = cities_counter
            cities_counter += 10
            while i < cities_counter:
                buttons[0].append(InlineKeyboardButton("Выбрать", callback_data="pick_code={}".format(picks[i]["Code"])))
                markup = InlineKeyboardMarkup(buttons)
                context.bot.send_message(chat_id=update.effective_chat.id, text=picks[i]["Address"])
                context.bot.send_location(chat_id=update.effective_chat.id,latitude=picks[i]["Lat"], longitude=picks[i]["Lang"], reply_markup=markup)
                buttons = [[]]
                i+=1
            global_state[user_id].cities_counter = cities_counter
            buttons[0].append(InlineKeyboardButton("Показать еще", callback_data="city_code=next"))
            markup = InlineKeyboardMarkup(buttons)
            context.bot.send_message(chat_id=update.effective_chat.id, text="...", reply_markup=markup)
            buttons=[[]]

        else:
            for pick in picks:
                buttons[0].append(InlineKeyboardButton("Выбрать", callback_data="pick_code={}".format(pick["Code"])))
                markup = InlineKeyboardMarkup(buttons)
                context.bot.send_message(chat_id=update.effective_chat.id, text=pick["Address"])
                context.bot.send_location(chat_id=update.effective_chat.id,latitude=pick["Lat"], longitude=pick["Lang"], reply_markup=markup)
                buttons = [[]]
    
            buttons[0].append(InlineKeyboardButton("Назад", callback_data="pick_code=back"))
            markup = InlineKeyboardMarkup(buttons)

            context.bot.send_message(chat_id=update.effective_chat.id, text="<-", reply_markup=markup)
            
    else:
        picks = global_state[user_id].picks
        i = 0
        if ((len(picks) - cities_counter) - 10) >= 0:
            i = cities_counter
            cities_counter+=10
        else:
            i = cities_counter
            cities_counter += len(picks) - cities_counter
        
        while i < cities_counter:
            buttons[0].append(InlineKeyboardButton("Выбрать", callback_data="pick_code={}".format(picks[i]["Code"])))
            markup = InlineKeyboardMarkup(buttons)
            context.bot.send_message(chat_id=update.effective_chat.id, text=picks[i]["Address"])
            context.bot.send_location(chat_id=update.effective_chat.id,latitude=picks[i]["Lat"], longitude=picks[i]["Lang"], reply_markup=markup)
            buttons = [[]]
            i+=1
        global_state[user_id].cities_counter = cities_counter

        if global_state[user_id].cities_counter != len(picks):
            buttons[0].append(InlineKeyboardButton("Показать еще", callback_data="city_code=next"))
            markup = InlineKeyboardMarkup(buttons)
            context.bot.send_message(chat_id=update.effective_chat.id, text="...", reply_markup=markup)
            buttons=[[]]
        else:
            buttons[0].append(InlineKeyboardButton("Назад", callback_data="pick_code=back"))
            markup = InlineKeyboardMarkup(buttons)

            context.bot.send_message(chat_id=update.effective_chat.id, text="<-", reply_markup=markup)
    
    return DELIVERY_TYPE
    


def pick_handler(update, context):
    username = update.effective_user.username
    user_id = update.callback_query.message.chat.id
    global_state[user_id].pick_code = update.callback_query.data
    print("pick")
    print(username)

    context.bot.send_message(chat_id=update.effective_chat.id, text='Введите ваше имя')
    return CREDENTIALS_N

    
    

def cancel_order_handler(update, context):
    user_id = update.callback_query.message.chat.id
    global_state[user_id].price_counter = 0
    buttons = [[]]
    buttons[0].append(KeyboardButton("Показать продукты"))
    markup = ReplyKeyboardMarkup(buttons,True, True)
    context.bot.send_message(chat_id=update.effective_chat.id, text='Заказ отменен!',reply_markup=markup)
    return CART

def change_creds_handler(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Введите ваше имя')
    return CREDENTIALS_N

def cancel_creds_handler(update, context):
    if(global_state[update.effective_chat.id].order_type == 'boxberry'):
        boxberry_handler(update, context)
    else:
        message_handler(update, context)

def accept_creds_handler(update, context):
    unique_id = uuid.uuid4()
    user_id = update.effective_chat.id

    name = global_state[user_id].credentials['name']
    second_name = global_state[user_id].credentials['secondname']
    phone = global_state[user_id].credentials['phone']
    email = global_state[user_id].credentials['email']

    

    if(global_state[user_id].order_type == 'boxberry'):
        create_order(user_id,name, second_name, phone, email, 2, 1,unique_id,boxberry_track_number='dsad')
    else:
        create_order(user_id, name, second_name, phone, email, 1, 1,unique_id,customer_post_index='dsada')
    context.bot.send_message(chat_id=user_id, text="Номер вашего заказа: {}".format(unique_id))
    
    username = update.effective_user.username
    notify_all_admins(context, username, unique_id)
    global_state[user_id].price_counter = 0
    return start(update, context)

def notify_all_admins(context, username, order_id):
    if admin_list.count == 0:
        return
    for admin in admin_list:
        context.bot.send_message(chat_id=admin, text="Пользователь {} сделал заказ\nНомер заказа: {}".format(username, order_id))

    






