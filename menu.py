from icecream import ic

from config import *
from event import get_target_print
from event_state.players_on_event import get_code_print
from event_state.set_rating import get_point_print
from fast import *
from menu_state.players_on_menu import get_real_about_player

ic.configureOutput(includeContext=True)


def try_start_set_username(update, context):
    user_id = update.message.chat_id
    telegram_nickname = update.message.from_user.username
    with open(USERS, 'a') as user_file:
        user_file.write(f"{user_id},{telegram_nickname}\n")
    if telegram_nickname is None:
        update.message.reply_text(f"Здравствуйте, у вас отсутствует ник в телеграмме, поэтому будет использоваться ботом ваше имя.")
        use_first_name(update, context)
    else:
        with open(USERS, 'a') as user_file:
            user_file.write(f"{user_id},{telegram_nickname}\n")


def use_first_name(update, context):
    user_id = update.message.chat_id
    new_user_info = update.message.from_user.first_name
    print(new_user_info)
    with open(USERS, "r") as user_file:
        users = user_file.readlines()
    updated_lines = []
    for line in users:
        if line.startswith(f"{user_id},"):
            updated_lines.append(f"{user_id},{new_user_info}\n")
        else:
            updated_lines.append(line)
    with open(USERS, "w") as user_file:
        user_file.writelines(updated_lines)
    return get_state()


def set_username(update, context):
    new_user_info = update.message.text
    user_id = update.message.chat_id
    with open(USERS, "r") as user_file:
        users = user_file.readlines()
    updated_lines = []
    for line in users:
        if line.startswith(f"{user_id},"):
            updated_lines.append(f"{user_id},{new_user_info}\n")
        else:
            updated_lines.append(line)
    with open(USERS, "w") as user_file:
        user_file.writelines(updated_lines)

    update.message.reply_text(f"Вы успешно изменили ник и теперь ваш ник: {new_user_info}.\n")
    return get_state()


def try_update_set_username(update, context):
    user_id = update.message.chat_id
    telegram_nickname = update.message.from_user.username
    if telegram_nickname is not None and telegram_nickname != get_user_name(user_id):
        with open(USERS, "r") as user_file:
            users = user_file.readlines()
        updated_lines = []
        for line in users:
            if line.startswith(f"{user_id},"):
                updated_lines.append(f"{user_id},{telegram_nickname}\n")
            else:
                updated_lines.append(line)
        with open(USERS, "w") as user_file:
            user_file.writelines(updated_lines)


def check_me(update, context):
    user_id = update.message.chat_id
    user_nickname = get_user_name(user_id)
    if find_in_players(user_id):
        if get_state() == EVENT:
            update.message.reply_text(f"{user_nickname}, вот информация о вас:\n"
                                      f"Роль: Игрок.\n"
                                      f"ID: {user_id}.\n"
                                      f"Никнейм: @{user_nickname}.\n"
                                      f"Настоящие фамилия и имя: {get_real_about_player(update, context)}.\n")
            get_code_print(update, context)
            get_target_print(update, context)
            get_point_print(update, context)
        elif get_state() == MENU:
            update.message.reply_text(f"{user_nickname}, вот информация о вас:\n"
                                      f"Роль: Игрок.\n"
                                      f"ID: {user_id}.\n"
                                      f"Никнейм: @{user_nickname}.\n"
                                      f"Настоящие фамилия и имя: {get_real_about_player(update, context)}.")
    elif find_in_admins(user_id):
        update.message.reply_text(f"{user_nickname}, вот информация о вас:\n"
                                  f"Роль: Администратор.\n"
                                  f"ID: {user_id}.\n"
                                  f"Никнейм: @{user_nickname}.")
    else:
        update.message.reply_text(f"{user_nickname}, вот информация о вас:\n"
                                  f"Роль: Пользователь.\n"
                                  f"ID: {user_id}.\n"
                                  f"Никнейм: @{user_nickname}.")
    return get_state()


def commands(update, context):
    user_id = update.message.chat_id
    update.message.reply_text(f"Вам доступны следующие команды")
    if get_state() == WAIT_EVENT:
        if find_in_users(user_id):
            update.message.reply_text(f"как пользователю:\n"
                                      f"/commands - список команд\n"
                                      f"/check_me - получение информации о себе\n"
                                      f"/get_points - количество найденных целей в текущем событии\n"
                                      f"/get_rating - ваше место в топе по найденным целям\n"
                                      f"/get_players - количество игроков в текущем событии\n")
        if find_in_admins(user_id):
            update.message.reply_text(f"как администратору:\n"
                                      f"/continue_event остановка события\n"
                                      f"сд удаление игрока\n"
                                      f"сд добавление баллов\n"
                                      f"/notify_users - отправить уведомление всем пользователям\n"
                                      f"/notify_players - отправить уведомление всем игрокам\n"
                                      f"/notify_admins - отправить уведомление всем администраторам\n"
                                      f"/end_event - досрочное окончание события")
    if get_state() == EVENT:
        if find_in_users(user_id):
            update.message.reply_text(f"как пользователю:\n"
                                      f"/commands - список команд\n"
                                      f"/check_me - получение информации о себе\n"
                                      f"/get_points - количество найденных целей в текущем событии\n"
                                      f"/get_rating - ваше место в топе по найденным целям\n"
                                      f"/get_players - количество игроков в текущем событии\n")
        if find_in_players(user_id):
            update.message.reply_text(f"как игроку:\n"
                                      f"/try_enter_code - попытка ввести код цели\n"
                                      f"/leave - покинуть событие\n"
                                      f"сд отправит сообщение цели\n"
                                      f"сд отправит сообщение админам\n"
                                      f"сд отправит сообщение искателю\n")
        if find_in_admins(user_id):
            update.message.reply_text(f"как администратору:\n"
                                      f"/stop_event остановка события\n"
                                      f"сд удаление игрока\n"
                                      f"сд добавление баллов\n"
                                      f"/notify_users - отправить уведомление всем пользователям\n"
                                      f"/notify_players - отправить уведомление всем игрокам\n"
                                      f"/notify_admins - отправить уведомление всем администраторам\n"
                                      f"/end_event - досрочное окончание события")
        return get_state()

    if get_state() == MENU:

        if find_in_users(user_id):
            update.message.reply_text(f"как пользователю:\n"
                                      f"/start - запуск бота\n"
                                      f"/commands - список команд\n"
                                      f"/registration - регистрация на событие\n"
                                      f"/check_me - получение информации о себе\n"
                                      f"/get_admins - получить список администраторов\n"
                                      f"/cancel - отмена команды\n"
                                      f"/stop - остановить бота\n")
        if find_in_players(user_id):
            update.message.reply_text(f"как игроку:\n"
                                      f"/set_my_info - изменение информации о себе\n"
                                      f"/cancel_registration - отмена регистрации\n"
                                      f"/cancel - отмена изменения информации о себе\n")
        if find_in_admins(user_id):
            update.message.reply_text(f"как администратору:\n"
                                      f"/add_admin - добавление нового администратора\n"
                                      f"/delete_admin - удаление администратора\n"
                                      f"/cancel - отмена процесса добавления/удаления администратора\n"
                                      f"/set_name_of_event - изменение названия события\n"
                                      f"/start_event - начало события\n"
                                      f"/notify_users - отправка сообщения всем пользователям\n"
                                      f"/notify_players - отправка сообщения всем игрокам\n"
                                      f"/notify_admins - отправка сообщения всем администраторам\n")
        return get_state()


def stop(update, context):
    ic(context)
    update.message.reply_text("Бот остановлен.")


def get_admins_nicks(update, context):
    ic(context)
    message = f"Список администраторов:\n"
    with open(ADMINS, "r") as admin_file:
        admins = admin_file.readlines()
    for line in admins:
        user_id_from_line, _ = line.strip().split(" ")
        message = message + f"@{get_user_name(user_id_from_line)}\n"
    update.message.reply_text(message)


def rules(update, context):
    ic(context)
    update.message.reply_text(f"Правила событий:\n")
