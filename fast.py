USERS = 'config/users.txt'
PLAYERS = 'event_state/event_data/players.txt'
ADMINS = 'config/admins.txt'
EVENT_NAME = 'config/event_name.txt'
TARGETS = 'event_state/event_data/targets.txt'
CODES = 'event_state/event_data/codes.txt'
ENTER_CODES = 'event_state/event_data/enter_codes.txt'
POINTS = 'event_state/event_data/points.txt'


def find_in_users(user_id):
    with open(USERS, "r") as user_file:
        lines = user_file.readlines()
        for line in lines:
            line = line.strip()
            if str(user_id) in line:
                return True
    return False


def find_in_players(user_id):
    with open(PLAYERS, "r") as player_file:
        lines = player_file.readlines()
        for line in lines:
            line = line.strip()
            if str(user_id) in line:
                return True
    return False


def find_in_admins(user_id):
    with open(ADMINS, "r") as admin_file:
        lines = admin_file.readlines()
        for line in lines:
            line = line.strip()
            if str(user_id) in line:
                return True
    return False


def get_user_name(user_id):
    with open(USERS, "r") as user_file:
        lines = user_file.readlines()
        for line in lines:
            line = line.strip()
            if str(user_id) in line:
                return str(line.split(",")[1].strip())


def get_player_real_name(user_id):
    print(f"{user_id}user_id")
    with open(PLAYERS, "r") as player_file:
        lines = player_file.readlines()
        for line in lines:
            line = line.strip()
            if str(user_id) == str(line.split(",")[0].strip()):
                print(f"{line}line")
                return str(line.split(",")[1].strip())


def read_file(file_name):
    with open(file_name, "r") as file:
        return file.readlines()


def write_file(file_name, lines):
    with open(file_name, "w") as file:
        file.writelines(lines)


def clear_file(file_name):
    with open(file_name, "w") as file:
        file.write("")


def get_event_name():
    with open(EVENT_NAME, 'r') as event_file:
        event_name = event_file.read()
    return event_name


def clear_event_files():
    clear_file(CODES)
    clear_file(TARGETS)
    clear_file(ENTER_CODES)
    clear_file(POINTS)
    return
