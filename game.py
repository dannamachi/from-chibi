import pygame
import time
from pygame.locals import *
from pygame.rect import *

import constants
import api
import buttons

from CommandSection import CommandSection
from MessageSection import MessageSection
from ReadSection import ReadSection
from NoteSection import NoteSection
from HelpfulSection import HelpfulSection
from EndSection import EndSection

from Page import Page

pygame.init()

SCREEN = pygame.display.set_mode(constants.SCREEN_SIZE)
FONT = pygame.font.SysFont('tahoma',20)
pygame.display.set_caption("From Chibi")

# text input setup
TEXTINPUT = ""
FONT_IMAGES = {}  # map rendered img to location (x,y)
deleting = False
delete_speed = 60

# sections setup
message_text = ""
section_id = -1
COMMANDLINE = CommandSection()
MESSAGE = MessageSection()
NOTES = NoteSection()
READS = ReadSection()
HELPS = HelpfulSection()
ENDS = EndSection()

SHOWING_GAME = Page(constants.PAGE_GAME, [COMMANDLINE, MESSAGE, NOTES, READS, HELPS])
SHOWING_END = Page(constants.PAGE_END, [ENDS])

# starting
CURRENT_PAGE = SHOWING_END
ENDS.set_text(api.get_intro())

while not api.IS_QUIT:
    ## Game page
    if CURRENT_PAGE.has_id(constants.PAGE_GAME):
        if deleting: 
            delete_speed -= 1
            if delete_speed == 0:
                delete_speed = 60
                if len(TEXTINPUT) > 0:
                    TEXTINPUT = TEXTINPUT[:-1]
        else:
            delete_speed = 60

        # event detection for game page
        for event in pygame.event.get():
            if event.type == QUIT:
                api.IS_QUIT = True
            if event.type == MOUSEBUTTONDOWN:
                # scrolling for reads
                if event.button == 4 and buttons.is_hovered(event.pos,constants.SECT_READ):
                    READS.shift_up_one_row()
                elif event.button == 5 and buttons.is_hovered(event.pos,constants.SECT_READ):
                    READS.shift_down_one_row()
                # scrolling for notes
                elif event.button == 4 and buttons.is_hovered(event.pos,constants.SECT_NOTE):
                    NOTES.shift_up_one_row()
                elif event.button == 5 and buttons.is_hovered(event.pos,constants.SECT_NOTE):
                    NOTES.shift_down_one_row()
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    COMMANDLINE.set_text(TEXTINPUT)
                    COMMANDLINE.process_command()
                    message_text, section_id = COMMANDLINE.run_command()
                    HELPS = api.update_helpful_note(HELPS)
                    TEXTINPUT = ""
                elif event.key == K_BACKSPACE:
                    if len(TEXTINPUT) > 0:
                        TEXTINPUT = TEXTINPUT[:-1]
                    deleting = True
                else:
                    TEXTINPUT += event.unicode
            if event.type == KEYUP and deleting:
                if event.key == K_BACKSPACE:
                    deleting = False

        COMMANDLINE.set_text(TEXTINPUT)

        # update for game page
        if section_id != -1:
            for section in SHOWING_GAME.get_sections():
                if section.has_id(section_id):
                    section.set_text(message_text)
                if api.TIME_SPENT != 0:
                    section.set_stale()
                elif isinstance(section,NoteSection) and api.DECRYPT_ENQUEUD:
                    section.set_stale()
            section_id = -1
            message_text = ""
        # check switch page
        if api.END_GAME:
            CURRENT_PAGE = SHOWING_END
            end_hints  = "=====================================\n"
            end_hints += api.END_STATUS
            end_hints += "=====================================\n"
            end_hints += api.END_MESSAGE
            ENDS.set_text(end_hints)

    ## End page (end/start)
    elif CURRENT_PAGE.has_id(constants.PAGE_END):
        # event check for end page
        for event in pygame.event.get():
            if event.type == QUIT:
                api.IS_QUIT = True
            if event.type == KEYDOWN:
                if event.key == K_RETURN and not api.END_GAME:
                    COMMANDLINE.set_text("help")
                    COMMANDLINE.process_command()
                    message_text, section_id = COMMANDLINE.run_command()
                    HELPS = api.update_helpful_note(HELPS)
                    TEXTINPUT = ""
                    CURRENT_PAGE = SHOWING_GAME
                elif event.key == K_RETURN and api.END_GAME:
                    # switch to main menu
                    api.IS_QUIT = True
        # update for end page

    # get rendered imgs from sections
    FONT_IMAGES = {}
    for section in CURRENT_PAGE.get_sections():
        renders = section.render_font(FONT)
        for img,loc in renders.items():
            FONT_IMAGES[img] = loc

    # display
    SCREEN.fill(constants.BLACK)
    for img,loc in FONT_IMAGES.items():
        SCREEN.blit(img,loc)  
    pygame.display.update()
        

pygame.quit()