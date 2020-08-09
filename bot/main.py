from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackQueryHandler,ConversationHandler, Filters

from .command_handlers import start
from .message_handlers.message_handler import message_handler 
from .message_handlers.callback_handler import increment_cart_handler
from bot.helpers import CART

start_handler = CommandHandler('start', start)
message_handler = MessageHandler(Filters.text, message_handler)
callback_hand = CallbackQueryHandler(increment_cart_handler)

#conv_handler = ConversationHandler(
#    entry_points=[start_handler],
 #   states={
#        CART: 
#    }
#)


updater = Updater('1398450165:AAFC9iquGnVr6Kyy49RvojtSJbMNdtlHT5Q', use_context=True)

dispatcher = updater.dispatcher
dispatcher.add_handler(start_handler)
dispatcher.add_handler(message_handler)
dispatcher.add_handler(callback_hand)


def start_bot():
    updater.start_polling()



