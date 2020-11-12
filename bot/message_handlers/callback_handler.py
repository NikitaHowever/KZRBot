# -*- coding: utf-8 -*-
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from telegram.error import BadRequest
from telegram import Invoice
from telegram import LabeledPrice
import json
import string
import random
import re

from bot.helpers import CART, global_state, DELIVERY_TYPE,PAYMENT_PICKUP,PAYMENT_BOXBERRY, BOXBERRY, admin_list
from bot.command_handlers import  start
from .message_handler import message_handler
from database_access import create_order
from .utils import get_new_cart_markup, update_and_get_markup, update_message, get_payment_url, get_points, get_cities_list, create_parsel, get_regions, Item

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
    user_id = update.effective_chat.id
    global_state[user_id].order_type = "pickup"
    
    #invoice = Invoice("Оплата заказа", "Заказ", "kzr-paper", "rub", global_state[user_id].price_counter)
    token = '410694247:TEST:8b1c9ed2-63ba-48c9-aecd-69b6c7841865'
    prices = [LabeledPrice("Сумма заказа", global_state[user_id].price_counter * 100)]

    context.bot.sendInvoice(user_id, 'Оплата заказа', 'Заказ', 'pickup', token, 'kzr-paper-start-param', 'RUB', prices, need_name=True, need_phone_number=True, need_email=True)
    return DELIVERY_TYPE


    

def cancel_order_handler(update, context):
    user_id = update.callback_query.message.chat.id
    global_state[user_id].price_counter = 0
    buttons = [[]]
    buttons[0].append(KeyboardButton("Показать продукты"))
    markup = ReplyKeyboardMarkup(buttons,True, True)
    context.bot.send_message(chat_id=update.effective_chat.id, text='Заказ отменен!',reply_markup=markup)
    return CART

def precheckout_handler(update, context):
    
    query = update.pre_checkout_query
    email = query.order_info.email
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

    if(re.search(regex, email)):
        query.answer(ok=True)
    else:
        query.answer(ok=False, error_message='Вы вели невалидный email!')

    return DELIVERY_TYPE

def successful_payment_callback(update, context):
    print("success")
    print(update)
    query = update.message.successful_payment
    user_id = update.message.chat.id
    user_nickname = update.message.chat.username
    username_arr = query.order_info.name.split(' ')
    user_name = ""
    user_secondname = ""
    user_phone =  query.order_info.phone_number
    user_email =  query.order_info.email

    if(len(username_arr) == 1):
        user_name = username_arr[0]
    else:
        user_name = username_arr[0]
        user_secondname = username_arr[1]

    print(query)
    unique_order_id = _generate_random_order_number()
    create_order(user_id, user_name, user_secondname, user_phone, user_email, 1, 5, unique_order_id)
    context.bot.send_message(chat_id=user_id, text="Мы свяжемся с вами как только ваш заказ будет готов!\n Ваш номер заказа: {}".format(unique_order_id))

    notify_all_admins(user_id,user_email,user_name, user_secondname, user_phone, context, user_nickname, unique_order_id)

    
    return CART

def _generate_random_order_number(size=15, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def get_items(user_id):
    items = []

    for item in global_state[user_id].element_counters:
        if(global_state[user_id].element_counters[item][1] == 0):
            continue
        items.append(Item(item, global_state[user_id].element_counters[item][0], "ШТ", 10, global_state[user_id].element_counters[item][2], global_state[user_id].element_counters[item][1]))
    
    return items


def notify_all_admins(user_id,email,name,secondt_name,phone, context, username, order_id):
    if admin_list.count == 0:
        return

    else:
        message = "Пользователь {} сделал заказ\nНомер заказа: {}\nEmail: {}\nИмя: {}\nФамилия: {}\nТелефон: {}\nТовары в заказе: \n\n".format(username, order_id, email, name, secondt_name, phone)
        elements = global_state[user_id].element_counters

        for key, value in elements.items():
            print(value[1])
            if(value[1] > 0):
                print(value[0])
                message += '{}: {}шт\n'.format(value[0], value[1])

        for admin in admin_list:
            context.bot.send_message(chat_id=admin, text=message)

    






