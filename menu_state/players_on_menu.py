from config import *
from fast import *


def registration_for_event(update, context):
    if get_state() != MENU:
        update.message.reply_text(f"Регистрация на событие недоступна.")
    else:
        user_id = update.message.chat_id
        user_nickname = get_user_name(user_id)
        if find_in_players(user_id):
            update.message.reply_text(f"{user_nickname}, Вы уже зарегистрированы на cледующее событие.")
        elif find_in_admins(user_id):
            update.message.reply_text(
                f"{user_nickname}, Ваша роль: Администратор и вы не можете участвовать в событии.")
        else:
            update.message.reply_text(f"{user_nickname}, для регистрации на событие вам необходимо ввеcти свои "
                                      f"настоящие фамилию и имя\n")
            return WAIT_ADD_PLAYER_NAME
    return get_state()


def add_player(update, context):
    new_player_id = update.message.chat_id
    new_player_info = update.message.text
    if not find_in_admins(new_player_id):
        with open(PLAYERS, "a") as player_file:
            player_file.write(f"{new_player_id},{new_player_info}\n")
        update.message.reply_text(f"Вы успешно зарегистрированы на следующее событие и теперь ваша роль: Игрок.\n")
        update.message.reply_text(f"Проверьте доступные команды с помощью /commands")
    return get_state()


def cancel_registration_for_event(update, context):
    user_id = update.message.chat_id
    if find_in_players(user_id) and get_state() == MENU:
        del_player(update, context)
    else:
        update.message.reply_text(f"У вас недостаточно прав для исполнения данной команды.")


def del_player(update, context):
    user_id = update.message.chat_id
    user_nickname = get_user_name(user_id)
    if find_in_players(user_id):
        with open(PLAYERS, "r") as player_file:
            players = player_file.readlines()
        with open(PLAYERS, "w") as player_file:
            for line in players:
                if str(user_id) not in line.strip():
                    player_file.write(line)
        update.message.reply_text(f"{user_nickname}, Вы успешно отменили регистрацию на следующее событие и теперь "
                                  f"ваша роль: Пользователь.\n")
        update.message.reply_text(f"Проверьте доступные команды с помощью /commands")
    return get_state()


def get_real_about_player(update, context):
    player_info = ""
    user_id = update.message.chat_id
    if find_in_players(user_id):
        with open(PLAYERS, "r") as player_file:
            players = player_file.readlines()
        for line in players:
            if str(user_id) in line.strip():
                player_info = line.split(",")[1].strip()
    return player_info


def start_set_info_about_player(update, context):
    user_id = update.message.chat_id
    user_nickname = get_user_name(user_id)
    if find_in_players(user_id):
        update.message.reply_text(f"{user_nickname}, введите новую информацию о вас.")
        return WAIT_SET_PLAYER_NAME
    else:
        update.message.reply_text(f"{user_nickname}, у вас недостаточно прав для этой команды'.")
        return get_state()


def set_info_about_player(update, context):
    user_id = update.message.chat_id
    user_nickname = get_user_name(user_id)
    new_info = update.message.text
    if find_in_players(user_id):
        with open(PLAYERS, "r") as player_file:
            players = player_file.readlines()
        with open(PLAYERS, "w") as player_file:
            for line in players:
                if str(user_id) in line.strip():
                    player_file.write(f"{user_id},{new_info}\n")
                else:
                    player_file.write(line)
        update.message.reply_text(f"{user_nickname}, информация о вас успешно обновлена.\n")
        update.message.reply_text(f"Проверьте доступные команды с помощью /commands")
    return get_state()


def cancel_set_me(update, context):
    update.message.reply_text("Изменение информации отменено.")
    return get_state()  # Вернуться в основное состояние после отмены
