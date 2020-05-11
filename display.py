import constants

def has_border(sect_id):
    return sect_id in list(DISPLAY_RECT.keys())

def change_hover_display(button_name):
    for button in list(BUTTON_DISPLAY_KEY.keys()):
        if button == button_name:
            BUTTON_DISPLAY_KEY[button] = 1
        else:
            BUTTON_DISPLAY_KEY[button] = 0

DISPLAY_RECT = {\
    constants.SECT_READ  : [(constants.GREEN, constants.RECT_READ, 1), (constants.GREEN, (constants.RECT_READ[0],constants.RECT_READ[1],constants.RECT_READ[2],constants.OFF_READ[1]), 1)],\
    constants.SECT_NOTE  : [(constants.GREEN, constants.RECT_NOTE, 1), (constants.GREEN, (constants.RECT_NOTE[0],constants.RECT_NOTE[1],constants.RECT_NOTE[2],constants.OFF_NOTE[1]), 1)],\
}

BUTTON_RECT = {\
    "START GAME"          : [(constants.GREEN, constants.MAIN_START, 8), (constants.GREEN, constants.MAIN_START)],\
    "LOAD GAME"           : [(constants.GREEN, constants.MAIN_LOAD, 8), (constants.GREEN, constants.MAIN_LOAD)],\
    "SAVE"                : [(constants.MAGENTA, constants.SAVE_SAVE, 8), (constants.MAGENTA, constants.SAVE_SAVE)],\
    "LOAD"                : [(constants.MAGENTA, constants.LOAD_LOAD, 8), (constants.MAGENTA, constants.LOAD_LOAD)],\
    "RETURN"              : [(constants.GREEN, constants.LOAD_RETURN, 8), (constants.GREEN, constants.LOAD_RETURN)],\
    "RETURN GAME"         : [(constants.GREEN, constants.SAVE_RETURN, 8), (constants.GREEN, constants.SAVE_RETURN)],\
}

BUTTON_DISPLAY_KEY = {\
    "START GAME"          : 0,\
    "LOAD GAME"           : 0,\
    "SAVE"                : 0,\
    "LOAD"                : 0,\
    "RETURN"              : 0,\
    "RETURN GAME"         : 0,\
}

SLOT_LIST = []

for i in range(20):
    SLOT_LIST.append("SLOT " + str(i + 1))
    BUTTON_RECT["SLOT " + str(i + 1)] = [(constants.MAGENTA, constants.SAVE_SLOTS[i], 2), (constants.MAGENTA, constants.SAVE_SLOTS[i])]
    BUTTON_DISPLAY_KEY["SLOT " + str(i + 1)] = 0