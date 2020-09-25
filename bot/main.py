from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackQueryHandler,ConversationHandler, Filters

from .command_handlers import start,become_admin
from .message_handlers.message_handler import cancel_admin,admin_password_handler , message_handler,email_handler, order_handler, name_handler, secondname_handler, phone_handler, order_handler, postindex_handler
from .message_handlers.callback_handler import increment_cart_handler, decrement_cart_handler, picckup_handler, cancel_order_handler, boxberry_handler, boxberry_region_handler, boxberry_back_handler, accept_creds_handler, change_creds_handler, cancel_creds_handler, boxbery_city_handler, pick_handler
from bot.helpers import ADMIN_CREDS, CART, DELIVERY_TYPE, BOXBERRY,CREDENTIALS_N,CREDENTIALS_EMAIL,CREDENTIALS_SN,CREDENTIALS_PHONE,CREDENTIALS_CHECK,CREDENTIALS_POSTINDEX, global_state



start_handler = CommandHandler('start', start)
admin_handler = CommandHandler('admin', become_admin)
buttons_prod = ['Показать продукты']
buttons_order = ['Оформить заказ']
message_handler = MessageHandler(Filters.text(buttons_prod), message_handler)
ord_handler = MessageHandler(Filters.text(buttons_order), order_handler)
inc_callback_handler = CallbackQueryHandler(increment_cart_handler, pattern='{"action": "inc"')
dec_callback_handler = CallbackQueryHandler(decrement_cart_handler, pattern='{"action": "dec"')
cancel_ord_handler = CallbackQueryHandler(cancel_order_handler, pattern='cancel_order')
pickup_callback_handler = CallbackQueryHandler(picckup_handler, pattern='pickup')
boxberry_callback_handler = CallbackQueryHandler(boxberry_handler, pattern='boxberry')
boxberry_region_callback_handler = CallbackQueryHandler(boxberry_region_handler, pattern="reg=")
boxberry_back_callback_handler = CallbackQueryHandler(boxberry_back_handler, pattern="city_code_back")
boxberry_city_callback_handler = CallbackQueryHandler(boxbery_city_handler, pattern="city_code=")
boxberry_pick_callback_handler = CallbackQueryHandler(pick_handler, pattern="pick_code=")
creds_name_handler = MessageHandler(Filters.text, name_handler)
creds_secondname_handler = MessageHandler(Filters.text, secondname_handler)
creds_phone_handler = MessageHandler(Filters.text, phone_handler)
creds_postindex_handler = MessageHandler(Filters.text, postindex_handler)
creds_email_handler = MessageHandler(Filters.text, email_handler)
change_creds_callback_handler = CallbackQueryHandler(change_creds_handler, pattern='creds_data=change')
cancel_creds_callback_handler = CallbackQueryHandler(cancel_creds_handler, pattern='creds_data=cancel')
accept_creds_callback_handlel = CallbackQueryHandler(accept_creds_handler, pattern='creds_data=accept')
admin_creds_callback_handler = MessageHandler(Filters.text,admin_password_handler)
admin_creds_cancel_handler = CallbackQueryHandler(cancel_admin, pattern='admin_cancel')



conv_handler = ConversationHandler(
    entry_points=[start_handler],
    states={
        CART: [admin_handler,inc_callback_handler, dec_callback_handler, message_handler, ord_handler],
        DELIVERY_TYPE: [admin_handler,pickup_callback_handler,cancel_ord_handler, boxberry_callback_handler,boxberry_pick_callback_handler,boxberry_city_callback_handler],
        BOXBERRY: [admin_handler,boxberry_region_callback_handler, boxberry_back_callback_handler,boxberry_city_callback_handler ],
        CREDENTIALS_N: [creds_name_handler],
        CREDENTIALS_SN: [creds_secondname_handler],
        CREDENTIALS_PHONE: [creds_phone_handler],
        CREDENTIALS_POSTINDEX: [creds_postindex_handler],
        CREDENTIALS_EMAIL: [creds_email_handler],
        CREDENTIALS_CHECK: [change_creds_callback_handler, cancel_creds_callback_handler,accept_creds_callback_handlel],
        ADMIN_CREDS: [admin_creds_callback_handler, admin_creds_cancel_handler]
        
    },
    fallbacks=[start_handler],
    allow_reentry=True
)


updater = Updater('1398450165:AAFC9iquGnVr6Kyy49RvojtSJbMNdtlHT5Q', use_context=True)

dispatcher = updater.dispatcher
#dispatcher.add_handler(start_handler)
#dispatcher.add_handler(message_handler)
dispatcher.add_handler(conv_handler)
dispatcher.add_handler(admin_handler)


def start_bot():
    updater.start_polling()
    updater.idle()



