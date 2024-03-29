from icecream import ic

from config import *
from event import create_event
from fast import *
from nofity import notify_all_admins


def start_add_admin(update, context):
    ic(context)
    user_id = update.message.chat_id
    user_nickname = update.message.chat.username
    if find_in_admins(user_id):
        update.message.reply_text(f"{user_nickname}, перешлите сообщение от пользователя, которого вы хотите сделать "
                                  f"администратором.")
        return WAIT_ADD_ADMIN_NAME  # Перейти в состояние ADD_ADMIN_TEXT для обработки текстовых сообщений
    else:
        update.message.reply_text(f"{user_nickname}, у вас недостаточно прав для добавления нового администратора.")
        return get_state()


def add_admin(update, context):
    adder_admin_nickname = update.message.chat.username
    new_admin_id = update.message.forward_from.id
    new_admin_nickname = update.message.forward_from.username
    if new_admin_id is None:
        update.message.reply_text(f"@{new_admin_nickname} не является пользователем бота.")
    elif new_admin_nickname is None:
        update.message.reply_text(
            f"Этот пользователь не может стать администратором так как у него отсутствует ник в телеграмме")
    elif find_in_players(new_admin_id):
        update.message.reply_text(f"@{new_admin_nickname} является игроком и не может быть администратором.")
        return get_state()
    elif find_in_users(new_admin_id) and not find_in_admins(new_admin_id):
        with open(ADMINS, "a") as admin_file:
            admin_file.write(f"{new_admin_id} ...\n")
        context.bot.send_message(chat_id=new_admin_id, text=f"@{adder_admin_nickname} сделал вас администратором.\n"
                                                            f"Проверьте доступные команды с помощью команды /commands.")
        update.message.reply_text(f"Администратор @{new_admin_nickname} успешно добавлен.")
    elif find_in_admins(new_admin_id):
        update.message.reply_text(f"@{new_admin_nickname} уже является администратором.")
    else:
        update.message.reply_text(f"@{new_admin_nickname} не является пользователем бота.")
    return get_state()  # Вернуться в основное состояние после завершения действия


def start_delete_admin(update, context):
    ic(context)
    user_id = update.message.chat_id
    user_nickname = update.message.chat.username
    if find_in_admins(user_id):
        update.message.reply_text(f"{user_nickname}, перешлите сообщение от администратора, которого вы хотите сделать "
                                  f"пользователем.")
        return WAIT_DELETE_ADMIN_NAME  # Перейти в состояние DELETE_ADMIN для обработки текстовых сообщений
    else:
        update.message.reply_text(f"{user_nickname}, у вас недостаточно прав для удаления администратора.")
        return get_state()


def delete_admin(update, context):
    deleter_admin_nickname = update.message.chat.username
    new_admin_id = update.message.forward_from.id
    new_admin_nickname = update.message.forward_from.username
    admins_to_keep = []
    with open(ADMINS, "r") as admin_file:
        admins = admin_file.readlines()
    for line in admins:
        if str(new_admin_id) not in line.strip():
            admins_to_keep.append(line)
    with open(ADMINS, "w") as admin_file:
        admin_file.writelines(admins_to_keep)
    if len(admins_to_keep) < len(admins):
        context.bot.send_message(chat_id=new_admin_id, text=f"@{deleter_admin_nickname} удалил вас из администраторов.")
        update.message.reply_text(f"Администратор @{new_admin_nickname} успешно удален.")
    else:
        update.message.reply_text(f"@{new_admin_nickname} не являлся администратором.")
    return get_state()


def cancel_set_admin(update, context):
    ic(context)
    update.message.reply_text("Добавление администратора отменено.")
    return get_state()  # Вернуться в основное состояние после отмены


def start_set_event_name(update, context):
    ic(context)
    user_id = update.message.chat_id
    user_nickname = update.message.chat.username
    event_name = get_event_name()
    if find_in_admins(user_id):
        update.message.reply_text(f"Сейчас имеется следующее название события: {event_name}, если вы хотите его "
                                  f"изменить, введите новое название.")
        update.message.reply_text(f"Если хотите оставить его прежним нажмите /cancel")
        return WAIT_NEW_EVENT_NAME
    else:
        update.message.reply_text(f"{user_nickname}, у вас недостаточно прав для удаления администратора.")
        return get_state()


def set_event_name(update, context):
    user_nickname = update.message.chat.username
    event_name = update.message.text
    with open(EVENT_NAME, 'w') as event_file:
        event_file.write(event_name)
    update.message.reply_text(f"Название события изменено на: {event_name}")
    mess = f"Админ @{user_nickname} изменил имя события на {event_name}"
    notify_all_admins(mess, context)
    return get_state()


def cancel_set_event_name(update, context):
    ic(context)
    update.message.reply_text("Изменение названия события отменено.")
    return get_state()  # Вернуться в основное состояние после отмены


def start_event(update, context):
    user_id = update.message.chat_id
    user_nickname = get_user_name(user_id)
    if find_in_admins(user_id):
        with open(USERS, 'r') as file:
            user_ids = file.read().splitlines()
            for user_id in user_ids:
                user_id = int(user_id.split(",")[0].strip())  # Получаем user_id из файла
                set_event_state(EVENT)
                context.user_data[user_id] = {
                    "state": f"{get_state()}"}  # Устанавливаем состояние "EVENT" для пользователя

                try:
                    context.bot.send_message(user_id, f"Cобытие {get_event_name()} началось.")
                except Exception.__name__:
                    pass

        update.message.reply_text(f"{user_nickname}, Вы начали событие.")
        clear_file(RATING)
        create_event(update, context)
        ic(context.user_data)
        return get_state()

    else:
        update.message.reply_text(f"{user_nickname}, у вас недостаточно прав для начала события.")
        return get_state()
