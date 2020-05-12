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

# max chars
MAX_CLI = 80
MAX_CRED = 80
MAX_HELP = 22
MAX_MSG = 80
MAX_NOTE = 36
MAX_READ = 36

# max rows
MAX_R_CRED = 25
MAX_R_HELP = 24
MAX_R_MSG = 5
MAX_R_NOTE = 25
MAX_R_READ = 25

# dimensions
SCREEN_SIZE = (1280,720)
RECT_MUSIC = (0,670,50,50)

RECT_SCREEN = (0,0,int(SCREEN_SIZE[0]),int(SCREEN_SIZE[1]))
RECT_CLI = (0,int(SCREEN_SIZE[1] * 7/8), int(SCREEN_SIZE[0]), int(SCREEN_SIZE[1] * 1/8))
RECT_MSG = (0,int(SCREEN_SIZE[1] * 6/8), int(SCREEN_SIZE[0]), int(SCREEN_SIZE[1] * 1/8))
RECT_READ = (int(SCREEN_SIZE[0] * 5/8),0,int(SCREEN_SIZE[0] * 3/8), int(SCREEN_SIZE[1] * 6/8))
RECT_NOTE = (0,0,int(SCREEN_SIZE[0] * 3/8), int(SCREEN_SIZE[1] * 6/8))
RECT_HELP = (int(SCREEN_SIZE[0] * 3/8),0,int(SCREEN_SIZE[0] * 2/8),int(SCREEN_SIZE[1] * 6/8))
RECT_END = (0,0,int(SCREEN_SIZE[0]),int(SCREEN_SIZE[1] * 6/8))
RECT_MAIN = (0,0,int(SCREEN_SIZE[0]),int(SCREEN_SIZE[1] * 5/8))
RECT_SLOT = (0,int(SCREEN_SIZE[1] * 1/12), int(SCREEN_SIZE[0]),int(SCREEN_SIZE[1] * 5/6))
RECT_CRED = RECT_END


# text offset
OFF_CLI = (20,40)
OFF_MSG = (20,10)
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
PAGE_CRED = 5

# button rects
MAIN_START = (SCREEN_SIZE[0] - 230, int(SCREEN_SIZE[1] * 1/6) + 60, 180, 60)
MAIN_LOAD  = (SCREEN_SIZE[0] - 230, int(SCREEN_SIZE[1] * 1/6) + 60 + 1 * int(SCREEN_SIZE[1] / 6), 180, 60)
MAIN_CREDITS = (SCREEN_SIZE[0] - 230, int(SCREEN_SIZE[1] * 1/6) + 60 + 2 * int(SCREEN_SIZE[1] / 6), 180, 60)
MAIN_QUIT = (SCREEN_SIZE[0] - 230, int(SCREEN_SIZE[1] * 1/6) + 60 + 3 * int(SCREEN_SIZE[1] / 6), 180, 60)

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
SECT_CRED = 9

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

CREDITS  = "Developed by Mochimochi95 with PyGame"
CREDITS += "\nBeta-ed by Seairah and Bambosh"
CREDITS += "\nMusic by Kevin MacLeod - scroll down for detailed credits"
CREDITS += "\n-----"
CREDITS += "\nMany thanks to my beloved friends who helped make this game more playable for others, and for sticking with it until the end"
CREDITS += "\nI suppose this can be called the game I make that is passable for others to play"
CREDITS += "\nI hope you enjoy this and figure out CHIBI's identity by the end of the game"
CREDITS += "\n-----"
CREDITS += "\nCredits for music used:"
CREDITS += "\nLicense: http://creativecommons.org/licenses/by/4.0/"
CREDITS += "\n\nScreen Saver by Kevin MacLeod"
CREDITS += "\nLink: https://incompetech.filmmusic.io/song/5715-screen-saver"
CREDITS += "\n\nLimit 70 by Kevin MacLeod"
CREDITS += "\nLink: https://incompetech.filmmusic.io/song/5710-limit-70"
CREDITS += "\n\nFloating Cities by Kevin MacLeod"
CREDITS += "\nLink: https://incompetech.filmmusic.io/song/3765-floating-cities"
CREDITS += "\n\nLong note One by Kevin MacLeod"
CREDITS += "\nLink: https://incompetech.filmmusic.io/song/3992-long-note-one"
CREDITS += "\n\nComfortable Mystery 3 by Kevin MacLeod"
CREDITS += "\nLink: https://incompetech.filmmusic.io/song/3529-comfortable-mystery-3"
CREDITS += "\n\nBeauty Flow by Kevin MacLeod"
CREDITS += "\nLink: https://incompetech.filmmusic.io/song/5025-beauty-flow"
CREDITS += "\n\nInspired by Kevin MacLeod"
CREDITS += "\nLink: https://incompetech.filmmusic.io/song/3918-inspired"
CREDITS += "\n\nChill Wave by Kevin MacLeod"
CREDITS += "\nLink: https://incompetech.filmmusic.io/song/3498-chill-wave"


