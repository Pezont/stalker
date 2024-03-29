from icecream import ic

from config import *
from fast import find_in_admins, get_user_name

ic.configureOutput(includeContext=True)


def notify_all_users(message, context):
    with open(USERS, "r") as user_file:
        lines = user_file.readlines()
        for line in lines:
            user_id, username = line.strip().split(",")
            try:
                context.bot.send_message(chat_id=int(user_id), text=message)
            except Exception as e:
                ic(e)


def notify_all_admins(message, context):
    with open(ADMINS, "r") as admin_file:
        lines = admin_file.readlines()
        for line in lines:
            admin_id = line.strip().replace("...", "")
            try:
                context.bot.send_message(chat_id=int(admin_id), text=message)
            except Exception as e:
                ic(e)


def notify_all_players(message, context):
    with open(PLAYERS, "r") as player_file:
        lines = player_file.readlines()
        for line in lines:
            player_id, _ = line.strip().split(",")
            try:
                context.bot.send_message(chat_id=int(player_id), text=message)
            except Exception as e:
                ic(e)


def start_send_to_users(update, context):
    ic(context)
    user_id = update.message.chat_id
    if find_in_admins(user_id):
        update.message.reply_text(f"Введите сообщение, которое хотите отправить всем пользователям.")
        return WAIT_MESSAGE_FOR_ALL_USERS
    else:
        update.message.reply_text(f"У вас недостаточно прав для отправки сообщений всем пользователям.")
        return get_state()


def send_to_users(update, context):
    message = f"Администратор @{get_user_name(update.message.chat_id)} отправил сообщение вам и другим пользователям:\n\n {update.message.text}"
    notify_all_users(message, context)
    update.message.reply_text(f"Сообщение отправлено всем пользователям.\n\n"
                              f"{message}")
    return get_state()


def start_send_to_players(update, context):
    ic(context)
    user_id = update.message.chat_id
    if find_in_admins(user_id):
        update.message.reply_text(f"Введите сообщение, которое хотите отправить всем игрокам.")
        return WAIT_MESSAGE_FOR_ALL_PLAYERS
    else:
        update.message.reply_text(f"У вас недостаточно прав для отправки сообщений всем игрокам.")
        return get_state()


def send_to_players(update, context):
    message = f"Администратор @{get_user_name(update.message.chat_id)} отправил сообщение вам и другим игрокам:\n\n {update.message.text}"
    notify_all_players(message, context)
    notify_all_admins(message, context)
    update.message.reply_text(f"Сообщение отправлено всем игрокам.\n\n"
                              f"{message}")
    return get_state()


def start_send_to_admins(update, context):
    ic(context)
    user_id = update.message.chat_id
    if find_in_admins(user_id):
        update.message.reply_text(f"Введите сообщение, которое хотите отправить всем администраторам.")
        return WAIT_MESSAGE_FOR_ALL_ADMINS
    else:
        update.message.reply_text(f"У вас недостаточно прав для отправки сообщений всем администраторам.")
        return get_state()


def send_to_admins(update, context):
    message = f"Администратор @{get_user_name(update.message.chat_id)} отправил сообщение вам и другим администраторам:\n\n{update.message.text}"
    notify_all_admins(message, context)
    update.message.reply_text(f"Сообщение отправлено всем администраторам.\n\n"
                              f"{message}")
    return get_state()


def cancel_send(update, context):
    ic(context)
    update.message.reply_text(f"Отправка сообщения  отменена.")
    return get_state()
