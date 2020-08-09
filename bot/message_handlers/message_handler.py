from telegram import InlineKeyboardMarkup, InlineKeyboardButton
import json
import sys

from database_access import get_items
from bot.helpers import CART, Global


def message_handler(update, context):
    if(update.message.text == 'Показать продукты'):
        send_items(update, context)

    return CART


def send_items(update, context):
    items = get_items()

    for item in items:
        message = '{}\nМатериал: {}\n{}\nЗа упаковку: {}руб'.format(item.get_name, item.get_material, item.get_descriptiom, item.get_price_for_pack)
        
        buttons = [[]]

        if(Global.element_counters.get(item.get_id) == None):
            Global.element_counters[item.get_id] = 0
        if(Global.element_buttons.get(item.get_id) == None):
            json_callback_data = {"itemId":item.get_id, "price":item.get_price_for_pack}
            json_callback_data_str = json.dumps(json_callback_data, ensure_ascii=False)
            print(json_callback_data_str)

            buttons[0].append(InlineKeyboardButton('+', callback_data=json_callback_data_str))
            buttons[0].append(InlineKeyboardButton('{}'.format(Global.element_counters[item.get_id]), callback_data="dummy"))
            buttons[0].append(InlineKeyboardButton('-', callback_data=json_callback_data_str))
            Global.element_buttons[item.get_id] = buttons
        else:
            buttons = Global.element_buttons[item.get_id]

        markup = InlineKeyboardMarkup(buttons)

        context.bot.send_message(chat_id=update.effective_chat.id,text=message, reply_markup=markup)


