from telegram.ext import Updater
# from icecream import ic


from config import *
from handler import conversation_handler, all_users_to_event_handler, all_users_to_main_handler


def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    dp.add_handler(conversation_handler)
    dp.add_handler(all_users_to_event_handler)
    dp.add_handler(all_users_to_main_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
