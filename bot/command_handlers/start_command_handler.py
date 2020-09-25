from telegram import ReplyKeyboardMarkup, KeyboardButton
from bot.helpers import CART,ADMIN_CREDS, global_state

def start(update, context):
    buttons = [[]]
    buttons[0].append(KeyboardButton("Показать продукты"))
    markup = ReplyKeyboardMarkup(buttons,True, True)
    print(update.effective_chat.id)
    context.bot.send_message(chat_id=update.effective_chat.id, text='Добро пожаловать в KZR!',reply_markup=markup)

    return CART