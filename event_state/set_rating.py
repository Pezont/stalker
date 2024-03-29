from config import *
from fast import *


def create_points_list():
    with open(POINTS, "w") as codes_file, open(PLAYERS, "r") as player_file:
        players = [line.strip().split(",")[0] for line in player_file]
        for user_id in players:
            point = 0
            codes_file.write(f"{user_id},{point}\n")


def add_point(user_id):
    with open(POINTS, "r") as points_file:
        points = points_file.readlines()

    updated_points = []
    for line in points:
        user_id_from_line, point = line.strip().split(",")
        if user_id_from_line == str(user_id):
            point = int(point) + 1
        updated_points.append((user_id_from_line, int(point)))

    sorted_points = sorted(updated_points, key=lambda x: x[1], reverse=True)

    with open(POINTS, "w") as points_file:
        for i in range(len(sorted_points)):
            if i > 0 and sorted_points[i][1] > sorted_points[i - 1][1]:
                updated_points[i], updated_points[i - 1] = updated_points[i - 1], updated_points[i]

        for user_id, point in sorted_points:
            points_file.write(f"{user_id},{point}\n")


def get_point_print(update, context):
    user_id = update.message.chat_id
    user_nickname = get_user_name(user_id)
    with open(POINTS, "r") as points_file:
        points = points_file.readlines()
    found = False
    for line in points:
        user_id_from_line, point = line.strip().split(",")
        if user_id_from_line == str(user_id):
            update.message.reply_text(f"Ваше количество найденных целей: {point}")
            found = True
            break
    if not found:
        update.message.reply_text(f"Вас нет в списке количества найденных целей.")


def get_point(user_id):
    with open(POINTS, "r") as points_file:
        points = points_file.readlines()
    for line in points:
        user_id_from_line, point = line.strip().split(",")
        if user_id_from_line == str(user_id):
            return point


def get_rating_of_points(update, context):
    with open(POINTS, "r") as points_file:
        points = points_file.readlines()
    rating = ""
    index = 1
    for line in points:
        user_id_from_line, point = line.strip().split(",")
        if user_id_from_line == str(update.message.chat_id):
            rating = index
            update.message.reply_text(f"Ваше место в рейтинге найденных целей: {rating}")
            return get_state()
        index += 1
    update.message.reply_text(f"Вас нет в списке рейтинга.")
    return get_state()


def get_quantity(file):
    return len(read_file(file))


def try_create_rating_top_5(n, found_player_id):
    top_players = {}
    with open(RATING, "r") as rating_file:
        # Read rating file and populate top_players dictionary
        for line in rating_file:
            player_id, player_score = map(int, line.strip().split(","))
            top_players[player_score] = player_id

    # Update top_players dictionary with new player and score
    top_players = {n: found_player_id, **top_players}

    with open(RATING, "w") as rating_file:
        for score, player in top_players.items():
            rating_file.write(f"{player},{score}\n")


def update_rating_plus(user_id, found_player_id):
    add_point(user_id)
    quantity = get_quantity(PLAYERS)
    if quantity == 4:
        try_create_rating_top_5(5, found_player_id)
    elif quantity == 3:
        try_create_rating_top_5(4, found_player_id)
    elif quantity == 2:
        try_create_rating_top_5(3, found_player_id)
    elif quantity == 1:
        try_create_rating_top_5(2, found_player_id)
        try_create_rating_top_5(1, user_id)


def send_top_5():
    with open(RATING, "r") as rating_file:
        top5 = [line.strip().split(',') for line in rating_file.readlines()]
        print(
            f"1 место - @{get_user_name(top5[0][0])}\n"
            f"2 место - @{get_user_name(top5[1][0])}\n"
            f"3 место - @{get_user_name(top5[2][0])}\n"
            f"4 место - @{get_user_name(top5[3][0])}\n"
            f"5 место - @{get_user_name(top5[4][0])}\n"
        )
