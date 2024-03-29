#
#
# def set_point(user_id, new_point):
#     with open(POINTS, "r") as points_file:
#         points = points_file.readlines()
#     with open(POINTS, "w") as points_file:
#         for line in points:
#             user_id_from_line, point = line.strip().split(",")
#             if user_id_from_line == str(user_id):
#                 points_file.write(f"{user_id_from_line},{new_point}\n")

from config import *
from event import close_event
from fast import *


def end_event_for_all(update, context):
    user_id = update.message.chat_id
    user_nickname = get_user_name(user_id)
    if find_in_admins(user_id):
        close_event(update, context)
        update.message.reply_text(f"{user_nickname}, Вы закончили событие.")
        return MENU
    else:
        update.message.reply_text(f"{user_nickname}, у вас недостаточно прав для окончания события.")
        return EVENT


def stop_event_for_all(update, context):
    user_id = update.message.chat_id
    user_nickname = get_user_name(user_id)
    if find_in_admins(user_id):
        set_event_state(WAIT_EVENT)
        update.message.reply_text(f"{user_nickname}, Вы приостановили событие.")
        with open(USERS, 'r') as file:
            user_ids = file.read().splitlines()
            for ids in user_ids:
                user_id = int(ids.split(",")[0].strip())
                context.user_data[user_id] = {"state": f"{get_state()}"}
                context.bot.send_message(user_id, f"Событие {get_event_name()} приостановлено.\n"
                                                  f"Проверьте доступные команды с помощью /commands")
        return get_state()
    else:
        update.message.reply_text(f"{user_nickname}, у вас недостаточно прав для окончания события.")
        return get_state()


def continue_event_for_all(update, context):
    user_id = update.message.chat_id
    user_nickname = get_user_name(user_id)
    if find_in_admins(user_id):
        set_event_state(EVENT)
        update.message.reply_text(f"{user_nickname}, Вы возобновили событие.")
        with open(USERS, 'r') as file:
            user_ids = file.read().splitlines()
            for ids in user_ids:
                user_id = int(ids.split(",")[0].strip())
                context.user_data[user_id] = {"state": f"{get_state()}"}
                context.bot.send_message(user_id, f"Событие {get_event_name()} возобновлено.\n"
                                                  f"Проверьте доступные команды с помощью /commands")
        return get_state()
    else:
        update.message.reply_text(f"{user_nickname}, у вас недостаточно прав для окончания события.")
        return get_state()
