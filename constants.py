# colors
BLACK = (0, 0, 0)
GRAY = (127, 127, 127)
WHITE = (255, 255, 255)

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)

# dimensions
SCREEN_SIZE = (800,600)
RECT_1 = (50, 20, 120, 100)
RECT_2 = (100, 60, 120, 100)
RECT_3 = (350, 20, 120, 100)
RECT_4 = (400, 60, 120, 100)

RECT_SCREEN = (0,0,SCREEN_SIZE[0],SCREEN_SIZE[1])
RECT_CLI = (0,SCREEN_SIZE[1] * 7/8, SCREEN_SIZE[0], SCREEN_SIZE[1] * 1/8)
RECT_MSG = (0,SCREEN_SIZE[1] * 6/8, SCREEN_SIZE[0], SCREEN_SIZE[1] * 1/8)
RECT_READ = (SCREEN_SIZE[0] * 5/8,0,SCREEN_SIZE[0] * 3/8, SCREEN_SIZE[1] * 6/8)
RECT_NOTE = (0,0,SCREEN_SIZE[0] * 3/8, SCREEN_SIZE[1] * 6/8)
RECT_HELP = (SCREEN_SIZE[0] * 3/8,0,SCREEN_SIZE[0] * 2/8,SCREEN_SIZE[1] * 6/8)
RECT_END = (0,0,SCREEN_SIZE[0],SCREEN_SIZE[1] * 6/8)

# text offset
OFF_CLI = (20,40)
OFF_MSG = (20,0)
OFF_READ = (20,25)
OFF_NOTE = (20,25)
OFF_HELP = (20,100)
OFF_END = (50,100)

# page id
PAGE_MAIN = 0
PAGE_SAVE = 1
PAGE_LOAD = 2
PAGE_GAME = 3
PAGE_END  = 4

# button rects
MAIN_START = (SCREEN_SIZE[0] * 1/8, SCREEN_SIZE[1] * 5/8, SCREEN_SIZE[0] * 2/8, SCREEN_SIZE[1] * 1/8)
MAIN_LOAD  = (SCREEN_SIZE[0] * 5/8, SCREEN_SIZE[1] * 5/8, SCREEN_SIZE[0] * 2/8, SCREEN_SIZE[1] * 1/8)

SAVE_SLOTS = {}
for index in range(20):
    SAVE_SLOTS[index] = (0, SCREEN_SIZE[1] * 1/12 + index * SCREEN_SIZE[1] * 5/6 / 20, SCREEN_SIZE[0], SCREEN_SIZE[1] * 5/6 / 20)

SAVE_SAVE   = (SCREEN_SIZE[0] * 4/5, SCREEN_SIZE[1] * 11/12, SCREEN_SIZE[0] * 1/5, SCREEN_SIZE[1] * 1/12)
SAVE_RETURN = (0, SCREEN_SIZE[1] * 11/12, SCREEN_SIZE[0] * 1/5, SCREEN_SIZE[1] * 1/12)
LOAD_LOAD   = (SCREEN_SIZE[0] * 4/5, SCREEN_SIZE[1] * 11/12, SCREEN_SIZE[0] * 1/5, SCREEN_SIZE[1] * 1/12)
LOAD_RETURN = (0, SCREEN_SIZE[1] * 11/12, SCREEN_SIZE[0] * 1/5, SCREEN_SIZE[1] * 1/12)


# section id
SECT_CLI = 0
SECT_MSG = 1
SECT_END = 2
SECT_READ = 4
SECT_NOTE = 3
SECT_HELP = 5

# actions
ACTIONS = {\
    0  : "dt",\
    1  : "decrypt",\
    2  : "read",\
    3  : "work",\
    4  : "root",\
    5  : "remote",\
    6  : "time",\
    7  : "overspace",\
    8  : "ping",\
    9  : "help",\
    10 : "decode",\
    11 : "save",\
    12 : "load",\
    13 : "quit",\
    14 : "reply",\
    15 : "notes",\
    16 : "chibi",\
    17 : "download",\
}

ACTION_COMMANDS = range(18)