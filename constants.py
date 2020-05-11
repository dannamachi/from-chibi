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

BLUEGRAY = (0, 14, 25)
BLUEOKAY = (0, 42, 76)

# dimensions
SCREEN_SIZE = (800,600)
RECT_1 = (50, 20, 120, 100)
RECT_2 = (100, 60, 120, 100)
RECT_3 = (350, 20, 120, 100)
RECT_4 = (400, 60, 120, 100)

RECT_SCREEN = (0,0,int(SCREEN_SIZE[0]),int(SCREEN_SIZE[1]))
RECT_CLI = (0,int(SCREEN_SIZE[1] * 7/8), int(SCREEN_SIZE[0]), int(SCREEN_SIZE[1] * 1/8))
RECT_MSG = (0,int(SCREEN_SIZE[1] * 6/8), int(SCREEN_SIZE[0]), int(SCREEN_SIZE[1] * 1/8))
RECT_READ = (int(SCREEN_SIZE[0] * 5/8),0,int(SCREEN_SIZE[0] * 3/8), int(SCREEN_SIZE[1] * 6/8))
RECT_NOTE = (0,0,int(SCREEN_SIZE[0] * 3/8), int(SCREEN_SIZE[1] * 6/8))
RECT_HELP = (int(SCREEN_SIZE[0] * 3/8),0,int(SCREEN_SIZE[0] * 2/8),int(SCREEN_SIZE[1] * 6/8))
RECT_END = (0,0,int(SCREEN_SIZE[0]),int(SCREEN_SIZE[1] * 6/8))
RECT_MAIN = (0,0,int(SCREEN_SIZE[0]),int(SCREEN_SIZE[1] * 5/8))
RECT_SLOT = (0,int(SCREEN_SIZE[1] * 1/12), int(SCREEN_SIZE[0]),int(SCREEN_SIZE[1] * 5/6))

# text offset
OFF_CLI = (20,40)
OFF_MSG = (20,0)
OFF_READ = (20,28)
OFF_NOTE = (20,28)
OFF_HELP = (10,40)
OFF_END = (50,100)
OFF_SLOT = (10,10)
OFF_BUTTON = (10,10)
OFF_SAVE = (7,7)

# page id
PAGE_MAIN = 0
PAGE_SAVE = 1
PAGE_LOAD = 2
PAGE_GAME = 3
PAGE_END  = 4

# button rects
MAIN_START = (int(SCREEN_SIZE[0] * 1/8), int(SCREEN_SIZE[1] * 5/8), int(SCREEN_SIZE[0] * 2/8), int(SCREEN_SIZE[1] * 1/8))
MAIN_LOAD  = (int(SCREEN_SIZE[0] * 5/8), int(SCREEN_SIZE[1] * 5/8), int(SCREEN_SIZE[0] * 2/8), int(SCREEN_SIZE[1] * 1/8))

SAVE_SLOTS = {}
for index in range(10):
    SAVE_SLOTS[index] = (0, int(SCREEN_SIZE[1] * 1/12 + index * SCREEN_SIZE[1] * 5/6 / 10 - 10), int(SCREEN_SIZE[0] * 1/2), int(SCREEN_SIZE[1] * 5/6 / 10))
for index in range(10,20):
    SAVE_SLOTS[index] = (int(SCREEN_SIZE[0] * 1/2), int(SCREEN_SIZE[1] * 1/12 + (index - 10) * SCREEN_SIZE[1] * 5/6 / 10 - 10), int(SCREEN_SIZE[0] * 1/2), int(SCREEN_SIZE[1] * 5/6 / 10))

SAVE_SAVE   = (int(SCREEN_SIZE[0] * 4/5), int(SCREEN_SIZE[1] * 11/12), int(SCREEN_SIZE[0] * 1/5), int(SCREEN_SIZE[1] * 1/12))
SAVE_RETURN = (0, int(SCREEN_SIZE[1] * 11/12), int(SCREEN_SIZE[0] * 1/5), int(SCREEN_SIZE[1] * 1/12))
LOAD_LOAD   = (int(SCREEN_SIZE[0] * 4/5), int(SCREEN_SIZE[1] * 11/12), int(SCREEN_SIZE[0] * 1/5), int(SCREEN_SIZE[1] * 1/12))
LOAD_RETURN = (0, int(SCREEN_SIZE[1] * 11/12), int(SCREEN_SIZE[0] * 1/5), int(SCREEN_SIZE[1] * 1/12))
RESTART = (int(SCREEN_SIZE[0] * 2/5), int(SCREEN_SIZE[1] * 11/12), int(SCREEN_SIZE[0] * 1/5), int(SCREEN_SIZE[1] * 1/12))


# section id
SECT_CLI = 0
SECT_MSG = 1
SECT_END = 2
SECT_READ = 4
SECT_NOTE = 3
SECT_HELP = 5
SECT_MAIN = 6
SECT_LOAD = 7
SECT_SAVE = 8

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