from telegram import InlineKeyboardMarkup, InlineKeyboardButton,ReplyKeyboardMarkup, KeyboardButton
import json
import sys

from database_access import get_items
from .utils import send_cart, send_items, send_arrange_order, send_delivery_types
from bot.command_handlers import start, become_admin
from bot.helpers import admin_list,  ADMIN_CREDS, CART, DELIVERY_TYPE, CREDENTIALS_SN,CREDENTIALS_POSTINDEX,CREDENTIALS_EMAIL ,CREDENTIALS_PHONE,CREDENTIALS_CHECK, global_state


def message_handler(update, context):
    send_items(update, context)
    send_cart(update, context)
    send_arrange_order(update, context)

    return CART



def form_check_creds_data(user_id, context):
    buttons = [[]]
    buttons[0].append(InlineKeyboardButton('Подтвердить', callback_data='creds_data=accept'))
    buttons[0].append(InlineKeyboardButton('Изменить', callback_data='creds_data=change'))
    buttons[0].append(InlineKeyboardButton('Отменить', callback_data='creds_data=cancel'))

    markup = InlineKeyboardMarkup(buttons)
    name = global_state[user_id].credentials['name']
    second_name = global_state[user_id].credentials['secondname']
    email = global_state[user_id].credentials['email']
    phone = global_state[user_id].credentials['phone']

    data = 'Имя: {}\nФамилия: {}\nТелефон: {}\nEmail: {}'.format(name, second_name, phone, email)
    if(global_state[user_id].order_type == 'pickup'):
        data += '\nПочтовый индекс: {}'.format(global_state[user_id].credentials["post_index"])
    context.bot.send_message(chat_id=user_id,text='Проверьте данные: \n{}'.format(data), reply_markup=markup)


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




