import handlers
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters

from creds import TOKEN


def main():
    print('SMTH')
    updater = Updater(TOKEN)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", handlers.start))
    dp.add_handler(CallbackQueryHandler(handlers.menu_option))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(MessageHandler(Filters.text, handlers.message_reply))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()