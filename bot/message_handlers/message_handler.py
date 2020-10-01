from telegram import InlineKeyboardMarkup, InlineKeyboardButton,ReplyKeyboardMarkup, KeyboardButton
import json
import sys

from database_access import get_items
from .utils import send_cart, send_items, send_arrange_order, send_delivery_types
from bot.command_handlers import start, become_admin
from bot.helpers import admin_list,  ADMIN_CREDS, CART, DELIVERY_TYPE, global_state


def message_handler(update, context):
    send_items(update, context)
    send_cart(update, context)
    send_arrange_order(update, context)

    return CART


def order_handler(update, context):
    print("ord")
     
    if(update.message.text == 'Оформить заказ'):
        result = send_delivery_types(update, context)
        if(result == False):
            return CART
        
    return DELIVERY_TYPE



def admin_password_handler(update, context):
    password = update.message.text
    print("PASSSS")
    user_id=update.effective_chat.id

    if(password != 'smokingkzr'):
        context.bot.send_message(chat_id=user_id,text='Неверный пароль')
        return become_admin(update, context)
    else:
        context.bot.send_message(chat_id=user_id, text='Теперь вы админ!')
        admin_list.append(user_id)
        return start(update, context)
    #return ADMIN_CREDS
    

def cancel_admin(update, context):
    return start(update, context)




