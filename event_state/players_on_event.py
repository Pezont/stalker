from icecream import ic
from config import *
from event_state.set_rating import update_rating_plus
from fast import read_file, get_user_name, get_player_real_name, find_in_players, write_file

ic.configureOutput(includeContext=True)


def get_next_target(user_id):
    with open(TARGETS, "r") as file:
        targets = [line.strip().split(",") for line in file]

    for i, (u_id, t_id) in enumerate(targets):
        if u_id == str(user_id):
            if i < len(targets) - 1:
                return targets[i + 1][1]
            if i == len(targets) - 1:
                return targets[0][1]


def get_next_code(user_id):
    with open(ENTER_CODES, "r") as file:
        codes = [line.strip().split(",") for line in file]
    for i, (u_id, code) in enumerate(codes):
        if u_id == str(user_id):
            if i < len(codes) - 1:
                return codes[i + 1][1]
            if i == len(codes) - 1:
                return codes[0][1]


def get_code(user_id):
    with open(CODES, "r") as codes_file:
        for line in codes_file:
            user_id_from_line, code = line.strip().split(",")
            if user_id_from_line == str(user_id):
                return code


def find_target_index(targets, user_id):
    for i, (u_id, t_id) in enumerate(targets):
        if u_id == str(user_id):
            return i


def find_player_by_code(code, code_lines):
    for line in code_lines:
        player, player_code = line.strip().split(",")
        if code == player_code:
            return player
    return None


def remove_player_from_lists(player_id, code_lines, player_lines, point_lines):
    code_lines = [line for line in code_lines if str(player_id) != line.split(",")[0]]
    player_lines = [line for line in player_lines if line.split(",")[0] != str(player_id)]
    point_lines = [line for line in point_lines if line.split(",")[0] != str(player_id)]
    ic(code_lines, player_lines, point_lines)
    return code_lines, player_lines, point_lines


def remove_player_from_enter_codes(user_id, player_id, enter_code_lines):
    updated_enter_code_lines = []
    for enter_code_line in enter_code_lines:
        current_user_id, current_code = enter_code_line.strip().split(",")
        if current_user_id != str(player_id) and current_user_id != str(user_id):
            updated_enter_code_lines.append(enter_code_line)
        if current_user_id == str(user_id):
            updated_enter_code_lines.append(f"{user_id},{get_next_code(user_id)}\n")
    ic(updated_enter_code_lines)
    return updated_enter_code_lines


def remove_player_from_targets(user_id, player_id, target_lines):
    updated_target_lines = []
    for target_line in target_lines:
        current_user_id, current_target = target_line.strip().split(",")
        if current_user_id != str(player_id) and current_user_id != str(user_id):
            updated_target_lines.append(target_line)
        if current_user_id == str(user_id):
            updated_target_lines.append(f"{user_id},{get_next_target(user_id)}\n")
    ic(updated_target_lines)
    return updated_target_lines


def get_code_print(update, context):
    user_id = update.message.chat_id
    if find_in_players(user_id):
        codes = read_file(CODES)
        for line in codes:
            userid, code_id = line.strip().split(",")
            if userid == str(user_id):
                code = code_id
                update.message.reply_text(f"Ваш код: {code}")
                return get_state()
    else:
        update.message.reply_text("У вас недостаточно прав для использования команды.")
        return get_state()


def start_leave_from_event(update, context):
    user_id = update.message.chat_id
    if find_in_players(user_id) and (get_state() == EVENT or get_state() == WAIT_EVENT):
        update.message.reply_text(f"ВНИМАНИЕ!\n"
                                  f"Если вы действительно хотите покинуть событие, введите ваш код\n"
                                  f"Если вы хотите остаться, введите /cancel")
        return WAIT_CODE_LEAVE
    else:
        update.message.reply_text(f"У вас недостаточно прав для использования команды.")
        return get_state()


def leave_from_event(update, context):
    seeker_id, target_id = 0, 0
    user_id = update.message.chat_id
    code = update.message.text
    if str(code) == str(get_code(user_id)):
        targets = read_file(TARGETS)
        for line in targets:
            userid, target = line.strip().split(",")
            ic(userid, target)
            if userid == str(user_id):
                target_id = target
        for line in targets:
            seeker, userid = line.strip().split(",")
            if userid == str(user_id):
                seeker_id = seeker
        ic(user_id)
        ic(seeker_id)
        ic(target_id)
        try:
            context.bot.send_message(
                chat_id=seeker_id,
                text=f"Пользователь @{get_user_name(user_id)} покинул событие. \n"
                     f"Теперь ваша новая цель: {get_player_real_name(target_id)}"
            )
        except Exception as e:
            ic(e)
        try:
            context.bot.send_message(
                chat_id=user_id,
                text=f"Вы покинули событие. Теперь ваша роль: Пользователь.\n"
                     f"Проверьте доступные команды с помощью /commands."
            )
        except Exception as e:
            ic(e)
        try:
            context.bot.send_message(
                chat_id=target_id,
                text=f"Текущий искатель покинул событие. Теперь у вас новый искатель\n"
            )
        except Exception as e:
            ic(e)

        code_lines = read_file(CODES)
        target_lines = read_file(TARGETS)
        player_lines = read_file(PLAYERS)
        enter_code_lines = read_file(ENTER_CODES)
        point_lines = read_file(POINTS)
        code_lines, player_lines, point_lines = remove_player_from_lists(user_id, code_lines, player_lines,
                                                                         point_lines)
        ic(code_lines, player_lines, target_lines)
        enter_code_lines = remove_player_from_enter_codes(seeker_id, user_id, enter_code_lines)
        ic(enter_code_lines)
        target_lines = remove_player_from_targets(seeker_id, user_id, target_lines)
        ic(target_lines)
        ic("-----")
        write_file(CODES, code_lines)
        write_file(PLAYERS, player_lines)
        write_file(POINTS, point_lines)
        write_file(ENTER_CODES, enter_code_lines)
        write_file(TARGETS, target_lines)
        ic(code_lines, player_lines, point_lines)
        ic(enter_code_lines, target_lines)
        update_rating_plus(seeker_id, user_id)
        return get_state()
    else:
        update.message.reply_text(f"{code} - неверный код, вы остаетесь в событии.")
        return get_state()


def cancel_leave_from_event(update, context):
    update.message.reply_text("Процесс отменен.")
    return get_state()
