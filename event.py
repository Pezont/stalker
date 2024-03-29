from icecream import ic

from config import *
from fast import *
from nofity import notify_all_players
from event_state.players_on_event import find_player_by_code, find_target_index, remove_player_from_lists, \
    remove_player_from_targets, remove_player_from_enter_codes, get_code, get_next_code, get_next_target
import random
from event_state.set_rating import create_points_list, send_top_5, update_rating_plus, get_quantity, get_point_print, \
    get_rating_of_points


def create_event(update, context):
    clear_event_files()
    create_code_list()
    create_target_list()
    create_points_list()
    send_codes(update, context)
    send_targets(update, context)
    mess = f"Проверьте доступные команды с помощью /commands."
    notify_all_players(mess, context)


def create_code():
    characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    code = "".join(random.choice(characters) for _ in range(1))
    return code


def create_code_list():
    with open("event_state/event_data/codes.txt", "w") as codes_file, open("event_state/event_data/players.txt",
                                                                           "r") as player_file:
        players = [line.strip().split(",")[0] for line in player_file]
        for user_id in players:
            code = create_code()
            codes_file.write(f"{user_id},{code}\n")


def create_target_list():
    user_id_to_name = {}

    with open("event_state/event_data/targets.txt", "w") as file, open("event_state/event_data/enter_codes.txt",
                                                                       "w") as codes_file, open("event_state/event_data/players.txt", "r") as player_file:
        players = [line.strip().split(",") for line in player_file]
        event_players = players
        random.shuffle(event_players)

        for player in event_players:
            user_id = player[0]
            player_name = player[1]
            user_id_to_name[user_id] = player_name

        for user_id, _ in event_players:
            target_index = (find_target_index(event_players, user_id) + 1) % len(event_players)
            target_user_id, target_user_name = event_players[target_index]
            file.write(f"{user_id},{target_user_id}\n")
            codes_file.write(f"{user_id},{get_code(target_user_id)}\n")


def attempt_to_find_target(update, context):
    if get_state() != EVENT:
        update.message.reply_text("Событие приостановлено или завершено")
    else:
        user_id = update.message.chat_id
        if find_in_players(user_id):
            update.message.reply_text("Введите код цели:")
            return WAIT_CODE
        else:
            update.message.reply_text("У вас недостаточно прав для использования команды.")
    return get_state()


def enter_code(update, context):
    user_id = update.message.chat_id
    try_code = update.message.text.strip()

    code_lines = read_file(CODES)
    target_lines = read_file(TARGETS)
    player_lines = read_file(PLAYERS)
    enter_code_lines = read_file(ENTER_CODES)
    point_lines = read_file(POINTS)
    found_player = False

    for enter_code_line in enter_code_lines:
        current_user_id, current_code = enter_code_line.strip().split(",")
        if current_user_id == str(user_id) and current_code == try_code:
            found_player = find_player_by_code(try_code, code_lines)

    if found_player:
        found_player_id = int(found_player)
        new_target = get_next_target(user_id)
        new_code = get_next_code(found_player_id)

        # remove player from lists
        code_lines, player_lines, point_lines = remove_player_from_lists(found_player_id, code_lines, player_lines,
                                                                         point_lines)
        enter_code_lines = remove_player_from_enter_codes(user_id, found_player_id, enter_code_lines)
        target_lines = remove_player_from_targets(user_id, found_player_id, target_lines)

        write_file(CODES, code_lines)
        write_file(PLAYERS, player_lines)
        write_file(POINTS, point_lines)
        write_file(ENTER_CODES, enter_code_lines)
        write_file(TARGETS, target_lines)

        try:
            context.bot.send_message(
                chat_id=found_player_id,
                text=f"Вас нашли. Теперь ваша роль: Пользователь.\n"
                     f"Проверьте доступные команды с помощью /commands")
            get_point_print(update, context)
            get_rating_of_points(update, context)
        except Exception as e:
            ic(e)

        if get_quantity(PLAYERS) == 1:
            context.bot.send_message(chat_id=user_id,
                                     text="Вы стали победителем события. Поздравляю!")
            update_rating_plus(user_id, found_player_id)
            close_event(update, context)

        else:
            context.bot.send_message(
                chat_id=user_id,
                text=f"Вы нашли цель. Ваша новая цель: {get_player_real_name(new_target)}"
            )
            update_rating_plus(user_id, found_player_id)

        return get_state()

    update.message.reply_text(f"{try_code} - неверный код")
    return get_state()


def send_codes(update, context):
    codes = read_file(CODES)
    for line in codes:
        user_id, code = line.strip().split(",")
        try:
            context.bot.send_message(chat_id=int(user_id), text=f"Ваш код: {code}")
        except Exception as e:
            ic(e)


def send_targets(update, context):
    targets = read_file(TARGETS)
    for line in targets:
        user_id, target = line.strip().split(",")
        try:
            context.bot.send_message(chat_id=int(user_id), text=f"Ваша цель: {get_player_real_name(target)}")
        except Exception as e:
            ic(e)


def get_target_print(update, context):
    user_id = update.message.chat_id
    if find_in_players(user_id):
        targets = read_file(TARGETS)
        for line in targets:
            userid, target = line.strip().split(",")
            print(userid, "---", target)
            print(get_player_real_name(target))
            if userid == str(user_id):
                update.message.reply_text(f"Ваша цель: {get_player_real_name(target)}")
                return get_state()
    else:
        update.message.reply_text("У вас недостаточно прав для использования команды.")
        return get_state()


def get_quantity_players_print(update, context):
    update.message.reply_text(f"В событии участвует {get_quantity(PLAYERS)} игроков на данный момент.")


def close_event(update, context):
    set_event_state(MENU)
    with open(USERS, 'r') as file:
        user_ids = file.read().splitlines()
        for ids in user_ids:
            user_id = int(ids.split(",")[0].strip())
            context.user_data[user_id] = {"state": f"{get_state()}"}
            context.bot.send_message(user_id, f"Событие {get_event_name()} окончено.\n"
                                              f"Проверьте доступные команды с помощью /commands")
            send_top_5()
            # допилить
            #
            #
            #
            #
            #
            #
            print(f"{user_id} -- {context.user_data[user_id]}")
            clear_file(PLAYERS)
    return get_state()
