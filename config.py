USERS = 'config/users.txt'
PLAYERS = 'event_state/event_data/players.txt'
ADMINS = 'config/admins.txt'
EVENT_NAME = 'config/event_name.txt'
TARGETS = 'event_state/event_data/targets.txt'
CODES = 'event_state/event_data/codes.txt'
ENTER_CODES = 'event_state/event_data/enter_codes.txt'
POINTS = 'event_state/event_data/points.txt'
RATING = 'event_state/event_data/rating_survivours.txt'
with open('config/token.txt', 'r') as token_file:
    TOKEN = token_file.read().strip()

[MENU, WAIT_DELETE_ADMIN_NAME, WAIT_ADD_PLAYER_NAME, WAIT_SET_PLAYER_NAME, WAIT_NEW_EVENT_NAME,
 EVENT, SET_EVENT_NAME, WAIT_MESSAGE_FOR_USER, WAIT_MESSAGE_FOR_PLAYERS, WAIT_MESSAGE_FOR_ADMINS,
 WAIT_ADD_ADMIN_NAME, WAIT_CODE, WAIT_MESSAGE_FOR_ALL_USERS, WAIT_MESSAGE_FOR_ALL_PLAYERS, WAIT_MESSAGE_FOR_ALL_ADMINS,
 WAIT_CODE_LEAVE, WAIT_EVENT] = range(
    17)


def get_state():
    with open('config/state.txt', 'r') as state_file:
        return int(state_file.read().strip())


def set_event_state(state):
    with open('config/state.txt', 'w') as state_file:
        state_file.write(str(state))
