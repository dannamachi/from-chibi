import pygame
import constants
from pygame.rect import *

SECTION_HOVER_ID = {\
    constants.SECT_READ   : constants.RECT_READ,\
    constants.SECT_NOTE   : constants.RECT_NOTE,\
}

BUTTON_DICT = {\
    "START GAME"  : constants.MAIN_START,\
    "LOAD GAME"   : constants.MAIN_LOAD,\
    "SLOT 1"      : constants.SAVE_SLOTS[0],\
    "SLOT 2"      : constants.SAVE_SLOTS[1],\
    "SLOT 3"      : constants.SAVE_SLOTS[2],\
    "SLOT 4"      : constants.SAVE_SLOTS[3],\
    "SLOT 5"      : constants.SAVE_SLOTS[4],\
    "SLOT 6"      : constants.SAVE_SLOTS[5],\
    "SLOT 7"      : constants.SAVE_SLOTS[6],\
    "SLOT 8"      : constants.SAVE_SLOTS[7],\
    "SLOT 9"      : constants.SAVE_SLOTS[8],\
    "SLOT 10"      : constants.SAVE_SLOTS[9],\
    "SLOT 11"      : constants.SAVE_SLOTS[10],\
    "SLOT 12"      : constants.SAVE_SLOTS[11],\
    "SLOT 13"      : constants.SAVE_SLOTS[12],\
    "SLOT 14"      : constants.SAVE_SLOTS[13],\
    "SLOT 15"      : constants.SAVE_SLOTS[14],\
    "SLOT 16"      : constants.SAVE_SLOTS[15],\
    "SLOT 17"      : constants.SAVE_SLOTS[16],\
    "SLOT 18"      : constants.SAVE_SLOTS[17],\
    "SLOT 19"      : constants.SAVE_SLOTS[18],\
    "SLOT 20"      : constants.SAVE_SLOTS[19],\
    "SAVE"        : constants.SAVE_SAVE,\
    "LOAD"        : constants.LOAD_LOAD,\
    "RETURN"      : constants.LOAD_RETURN,\
    "RETURN GAME" : constants.SAVE_RETURN,\
                            
}

COLOR_MAIN_BUTTONS = {\
    constants.MAIN_START  : constants.GREEN,\
    constants.MAIN_LOAD   : constants.MAGENTA,\
}

COLOR_SLOTS = constants.CYAN

COLOR_SAVE_BUTTONS = {\
    constants.SAVE_SAVE   : constants.BLUE,\
    constants.SAVE_RETURN : constants.GREEN,\
}

COLOR_LOAD_BUTTONS = {\
    constants.LOAD_LOAD   : constants.MAGENTA,\
    constants.LOAD_RETURN : constants.GREEN,\
}

def is_hovered(mouse_pos, section_id):
    if section_id in list(SECTION_HOVER_ID.keys()):
        rect = pygame.Rect(*SECTION_HOVER_ID[section_id])
        return rect.collidepoint(mouse_pos)
    return False

def is_clicked(mouse_pos, button_name):
    if button_name in list(BUTTON_DICT.keys()):
        rect = pygame.Rect(*BUTTON_DICT[button_name])
        return rect.collidepoint(mouse_pos)
    return False
