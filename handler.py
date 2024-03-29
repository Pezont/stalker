from icecream import ic
from telegram.ext import CommandHandler, ConversationHandler, MessageHandler, Filters

from config import *
from event import enter_code, attempt_to_find_target, get_quantity_players_print
from event_state.admins_on_event import end_event_for_all, stop_event_for_all, continue_event_for_all
from event_state.players_on_event import start_leave_from_event, leave_from_event, cancel_leave_from_event
from event_state.set_rating import get_point_print, get_rating_of_points
from fast import *
from menu import try_start_set_username, check_me, commands, stop, get_admins_nicks, rules, \
    try_update_set_username
from menu_state.admins_on_menu import start_add_admin, add_admin, start_delete_admin, delete_admin, cancel_set_admin, \
    start_set_event_name, set_event_name, cancel_set_event_name, start_event
from menu_state.players_on_menu import registration_for_event, start_set_info_about_player, \
    cancel_registration_for_event, cancel_set_me, add_player, set_info_about_player
from nofity import start_send_to_users, start_send_to_players, start_send_to_admins, send_to_users, cancel_send, \
    send_to_players, send_to_admins

ic.configureOutput(includeContext=True)


def try_register_new_user(update, context):
    user_id = update.message.chat_id
    if find_in_users(user_id):
        update.message.reply_text(f"{get_user_name(user_id)}, Вы уже пользователь бота.")
        try_update_set_username(update, context)
    else:
        try_start_set_username(update, context)
        update.message.reply_text(f"Поздравляем, {get_user_name(user_id)}! Теперь вы пользователь нашего бота.")

    context.user_data[user_id] = {"state": f"{get_state()}"}
    commands(update, context)
    return get_state()


# Обработчики команд, которые будут запускать команды
all_users_to_event_handler = CommandHandler("start_event", start_event)
all_users_to_main_handler = CommandHandler("end_event", end_event_for_all)

conversation_handler = ConversationHandler(
    entry_points=[CommandHandler('start', try_register_new_user)],
    states={
        MENU: [
            # команды всех
            CommandHandler("start", try_register_new_user),
            CommandHandler("commands", commands),
            CommandHandler("check_me", check_me),
            CommandHandler("get_admins", get_admins_nicks),
            CommandHandler("rules", rules),

            # команды пользователей
            CommandHandler("registration", registration_for_event),

            # команды игроков
            CommandHandler("set_my_info", start_set_info_about_player),
            CommandHandler("cancel_registration", cancel_registration_for_event),

            # команды администраторов
            CommandHandler("add_admin", start_add_admin),
            CommandHandler("delete_admin", start_delete_admin),
            CommandHandler("set_name_of_event", start_set_event_name),
            CommandHandler("start_event", start_event),
            CommandHandler("notify_users", start_send_to_users),
            CommandHandler("notify_players", start_send_to_players),
            CommandHandler("notify_admins", start_send_to_admins),

        ],
        EVENT: [
            # CommandHandler("sss", end_event_for_all),
            CommandHandler("commands", commands),
            CommandHandler("check_me", check_me),
            CommandHandler("get_points", get_point_print),
            CommandHandler("get_players", get_quantity_players_print),
            CommandHandler("get_rating", get_rating_of_points),
            # Для игроков
            CommandHandler("try_enter_code", attempt_to_find_target),
            CommandHandler("leave", start_leave_from_event),
            # Для администраторов
            CommandHandler("notify_users", start_send_to_users),
            CommandHandler("notify_players", start_send_to_players),
            CommandHandler("notify_admins", start_send_to_admins),
            CommandHandler("end_event", end_event_for_all),
            CommandHandler("stop_event", stop_event_for_all),
            # --------------Приостановить событие
            CommandHandler("continue_event", continue_event_for_all),
            # --------------Продолжить событие

            # --------------Накинуть баллов
            # --------------Выкинуть из события
        ],
        # IN MENU
        # Состояния пользователей


        # Состояния игроков
        WAIT_ADD_PLAYER_NAME: [CommandHandler("cancel", cancel_set_me), MessageHandler(Filters.text, add_player)],
        WAIT_SET_PLAYER_NAME: [CommandHandler("cancel", cancel_set_me),
                               MessageHandler(Filters.text, set_info_about_player)],

        # Состояния администраторов
        WAIT_ADD_ADMIN_NAME: [CommandHandler("cancel", cancel_set_admin), MessageHandler(Filters.text, add_admin)],
        WAIT_DELETE_ADMIN_NAME: [CommandHandler("cancel", cancel_set_admin),
                                 MessageHandler(Filters.text, delete_admin)],
        WAIT_NEW_EVENT_NAME: [CommandHandler("cancel", cancel_set_event_name),
                              MessageHandler(Filters.text, set_event_name)],
        WAIT_MESSAGE_FOR_ALL_USERS: [CommandHandler("cancel", cancel_send),
                                     MessageHandler(Filters.text, send_to_users)],
        WAIT_MESSAGE_FOR_ALL_PLAYERS: [CommandHandler("cancel", cancel_send),
                                       MessageHandler(Filters.text, send_to_players)],
        WAIT_MESSAGE_FOR_ALL_ADMINS: [CommandHandler("cancel", cancel_send),
                                      MessageHandler(Filters.text, send_to_admins)],

        # IN EVENT
        # Состояния игроков
        WAIT_CODE: [MessageHandler(Filters.text, enter_code)],
        WAIT_CODE_LEAVE: [CommandHandler("cancel", cancel_leave_from_event),
                          MessageHandler(Filters.text, leave_from_event)]

    },
    fallbacks=[CommandHandler('stop', stop), all_users_to_event_handler]
)
