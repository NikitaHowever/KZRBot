from bot.helpers import Global
from telegram import InlineKeyboardMarkup
import json
from bot.helpers import CART

def increment_cart_handler(update, context):
    query = update.callback_query
    query_data = query.data
    query_data_json = json.loads(query_data)

    markup = update_and_get_markup(query_data_json['itemId'], True)
    bot = context.bot

    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text=query.message.text,
        reply_markup=markup
    )
    return CART


def decrement_cart_handler(update, context):
    pass


def update_and_get_markup(item_id,inc_or_dec=False):
    keyboard = Global.element_buttons[item_id]
    counter = Global.element_counters[item_id]

    if(inc_or_dec):
        counter += 1
    else:
        counter -= 1

    keyboard[0][1].text = str(counter)
    Global.element_counters[item_id] = counter
    Global.element_buttons[item_id] = keyboard

    reply_markup = InlineKeyboardMarkup(keyboard)

    return reply_markup


