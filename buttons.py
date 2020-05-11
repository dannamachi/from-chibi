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
    "SAVE"        : constants.SAVE_SAVE,\
    "LOAD"        : constants.LOAD_LOAD,\
    "RETURN"      : constants.LOAD_RETURN,\
    "RETURN GAME" : constants.SAVE_RETURN,\
    "RESTART"     : constants.RESTART,\
}

BUTTON_FONT_COLOR = {\
    "START GAME"  : [constants.GREEN, constants.BLACK],\
    "LOAD GAME"   : [constants.GREEN, constants.BLACK],\
    "SAVE"        : [constants.MAGENTA, constants.BLACK],\
    "LOAD"        : [constants.MAGENTA, constants.BLACK],\
    "RETURN"      : [constants.GREEN, constants.BLACK],\
    "RETURN GAME" : [constants.GREEN, constants.BLACK],\
    "RESTART"     : [constants.MAGENTA, constants.BLACK],\
}

for i in range(20):
    BUTTON_DICT["SLOT " + str(i + 1)] = constants.SAVE_SLOTS[i]
    BUTTON_FONT_COLOR["SLOT " + str(i + 1)] = [constants.MAGENTA, constants.BLACK]

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
