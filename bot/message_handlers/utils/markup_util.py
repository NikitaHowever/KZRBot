from telegram import InlineKeyboardMarkup

from bot.helpers import global_state

def get_new_cart_markup(user_id):
    buttons = global_state[user_id].element_buttons[0]
    buttons[0][0].text = "Сумма заказа: {} руб".format(global_state[user_id].price_counter)
    global_state[user_id].element_buttons[0] = buttons

    markup = InlineKeyboardMarkup(buttons)

    return markup

def update_and_get_markup(item_id,user_id,price,inc_or_dec=False):
    keyboard = global_state[user_id].element_buttons[item_id]
    counter = global_state[user_id].element_counters[item_id][1]

    if(inc_or_dec):
        counter += 1
        global_state[user_id].price_counter+=price
    else:
        if(counter == 0): return None
        else:
            counter -= 1
            global_state[user_id].price_counter -= price

    keyboard[0][1].text = str(counter)
    global_state[user_id].element_counters[item_id][1] = counter
    global_state[user_id].element_buttons[item_id] = keyboard

    reply_markup = InlineKeyboardMarkup(keyboard)

    return reply_markup