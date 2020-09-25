from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from bot.helpers import ADMIN_CREDS

def become_admin(update, context):
    buttons = [[]]
    buttons[0].append(InlineKeyboardButton('Отмена', callback_data="admin_cancel"))
    markup = InlineKeyboardMarkup(buttons)
    context.bot.send_message(chat_id=update.effective_chat.id, text='Введите пароль', reply_markup=markup)

    return ADMIN_CREDS
