from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
import json

from bot.helpers import global_state, Global, DELIVERY_TYPE
from database_access import get_items

def send_cart(update, context):
    buttons = [[]]
    user_id = update.message.chat.id
    #if(global_state[user_id].element_buttons.get(0) == None):
    buttons[0].append(InlineKeyboardButton('Сумма заказа: {} руб'.format(global_state[user_id].price_counter), callback_data="dummy"))
    global_state[user_id].element_buttons[0] = buttons
    #else:
        #buttons = global_state[user_id].element_buttons[0]

    markup = InlineKeyboardMarkup(buttons)
    message =  context.bot.send_message(chat_id=update.effective_chat.id,text="Ваша корзина!", reply_markup=markup)
    global_state[user_id].cart_message_id = message.message_id
    print(global_state[user_id].cart_message_id)

def send_arrange_order(update, context):
    buttons = [[]]
    buttons[0].append(KeyboardButton('Оформить заказ'))
    markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)

    context.bot.send_message(chat_id=update.effective_chat.id, text='Оформление заказа!', reply_markup=markup)

    return DELIVERY_TYPE

def send_items(update, context):
    items = get_items()
    user_id = update.message.chat.id
    for item in items:
        message = '{}\nМатериал: {}\n{}\nЗа упаковку: {}руб'.format(item.get_name, item.get_material, item.get_descriptiom, item.get_price_for_pack)
        
        buttons = [[]]

        if(global_state.get(user_id) == None):
            global_state[user_id] = Global()

        #if(global_state[user_id].element_counters.get(item.get_id) == None):
        global_state[user_id].element_counters[item.get_id] = [item.get_name, 0, item.get_price_for_pack]
        global_state[user_id].price_counter = 0
        
        #if(global_state[user_id].element_buttons.get(item.get_id) == None):
        json_callback_data_inc = {"action":"inc","itemId":item.get_id, "price":item.get_price_for_pack}
        json_callback_data_dec = {"action":"dec", "itemId":item.get_id, "price":item.get_price_for_pack}
        json_callback_data_inc_str = json.dumps(json_callback_data_inc, ensure_ascii=False)
        json_callback_data_dec_str = json.dumps(json_callback_data_dec, ensure_ascii=False)
        print(json_callback_data_dec_str)
            

        buttons[0].append(InlineKeyboardButton('+', callback_data=json_callback_data_inc_str))
        buttons[0].append(InlineKeyboardButton('{}'.format(global_state[user_id].element_counters[item.get_id][1]), callback_data="dummy"))
        buttons[0].append(InlineKeyboardButton('-', callback_data=json_callback_data_dec_str))
        global_state[user_id].element_buttons[item.get_id] = buttons
        #else:
           # buttons = global_state[user_id].element_buttons[item.get_id]

        markup = InlineKeyboardMarkup(buttons)

        context.bot.send_photo(chat_id=update.effective_chat.id,photo=item.get_item_image,caption=message, reply_markup=markup)

def send_delivery_types(update, context):
    user_id = update.message.chat.id

    if(global_state[user_id].price_counter == 0):
        context.bot.send_message(chat_id=update.effective_chat.id,text='Ваша корзина пуста')
        return False
    buttons = [[]]
    buttons[0].append(InlineKeyboardButton('Самовывоз', callback_data="pickup"))

    markup = InlineKeyboardMarkup(buttons)
    context.bot.send_message(chat_id=update.effective_chat.id,text='Выберете способ доставки!', reply_markup=markup)
    return True

def update_message(bot, chat_id, message_id,reply_markup):
     bot.edit_message_reply_markup(
        chat_id=chat_id,
        message_id=message_id,
        reply_markup=reply_markup
        )