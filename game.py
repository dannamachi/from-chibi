import pygame
import time
from pygame.locals import *
from pygame.rect import *

import constants
import api
import buttons
import display

from CommandSection import CommandSection
from MessageSection import MessageSection
from ReadSection import ReadSection
from NoteSection import NoteSection
from HelpfulSection import HelpfulSection
from EndSection import EndSection
from MainSection import MainSection
from LoadSection import LoadSection
from SaveSection import SaveSection

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
MAIN = MainSection()
LOADS = LoadSection()
SAVES = SaveSection()

SHOWING_GAME = Page(constants.PAGE_GAME, [COMMANDLINE, MESSAGE, NOTES, READS, HELPS])
SHOWING_END = Page(constants.PAGE_END, [ENDS])
SHOWING_MAIN = Page(constants.PAGE_MAIN, [MAIN], ["START GAME", "LOAD GAME"])
SHOWING_LOAD = Page(constants.PAGE_LOAD, [LOADS], ["RESTART","RETURN","LOAD"])
SHOWING_SAVE = Page(constants.PAGE_SAVE, [LOADS], ["RESTART","RETURN GAME","SAVE"])

# starting
previous_page = SHOWING_MAIN
CURRENT_PAGE = SHOWING_MAIN
SAVES.reload()
LOADS.reload()

while not api.IS_QUIT:
    # check hover button
    mouse_pos = pygame.mouse.get_pos()
    for button in CURRENT_PAGE.get_buttons():
        if buttons.is_clicked(mouse_pos,button):
            display.BUTTON_DISPLAY_KEY[button] = 1
        else:
            display.BUTTON_DISPLAY_KEY[button] = 0
    ## Save game
    if CURRENT_PAGE.has_id(constants.PAGE_SAVE):
        for button in display.SLOT_LIST:
            if buttons.is_clicked(mouse_pos,button):
                display.BUTTON_DISPLAY_KEY[button] = 1
            else:
                display.BUTTON_DISPLAY_KEY[button] = 0
        if SAVES.is_selected():
            display.BUTTON_DISPLAY_KEY[SAVES.get_selected()] = 1
        for event in pygame.event.get():
            if event.type == QUIT:
                api.IS_QUIT = True
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    if buttons.is_clicked(event.pos,"RETURN GAME"):
                        SAVES.reset()
                        CURRENT_PAGE = SHOWING_GAME
                        MESSAGE.set_text("")
                    elif buttons.is_clicked(event.pos,"SAVE"):
                        load_result, message_text, section_id = *SAVES.run_command(), constants.SECT_MSG
                        if load_result:
                            SAVES.reload()
                            LOADS.reload()
                    elif buttons.is_clicked(event.pos,"RESTART"):
                        SAVES.set_restart()
                        load_result, message_text, section_id = *SAVES.run_command(), constants.SECT_MSG
                        CURRENT_PAGE = SHOWING_END
                        ENDS.set_text(api.get_intro())
                        MESSAGE.set_text(message_text)
                    for button in display.SLOT_LIST:
                        if buttons.is_clicked(event.pos,button):
                            SAVES.select(button)
                            break
    ## Load page
    elif CURRENT_PAGE.has_id(constants.PAGE_LOAD):
        for button in display.SLOT_LIST:
            if buttons.is_clicked(mouse_pos,button):
                display.BUTTON_DISPLAY_KEY[button] = 1
            else:
                display.BUTTON_DISPLAY_KEY[button] = 0
        if LOADS.is_selected():
            display.BUTTON_DISPLAY_KEY[LOADS.get_selected()] = 1
        for event in pygame.event.get():
            if event.type == QUIT:
                api.IS_QUIT = True
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    if buttons.is_clicked(event.pos,"RETURN"):
                        LOADS.reset()
                        CURRENT_PAGE = previous_page
                        MESSAGE.set_text("")
                    elif buttons.is_clicked(event.pos,"LOAD"):
                        load_result, message_text, section_id = *LOADS.run_command(), constants.SECT_MSG
                        if load_result:
                            CURRENT_PAGE = SHOWING_GAME
                            for section in SHOWING_GAME.get_sections():
                                section.reset()
                            HELPS = api.update_helpful_note(HELPS)
                            SAVES.reload()
                            LOADS.reload()
                    elif buttons.is_clicked(event.pos,"RESTART"):
                        LOADS.set_restart()
                        load_result, message_text, section_id = *LOADS.run_command(), constants.SECT_MSG
                        CURRENT_PAGE = SHOWING_END
                        ENDS.set_text(api.get_intro())
                        print(message_text)
                        MESSAGE.set_text(message_text)
                    for button in display.SLOT_LIST:
                        if buttons.is_clicked(event.pos,button):
                            LOADS.select(button)
                            break
    ## Main page
    elif CURRENT_PAGE.has_id(constants.PAGE_MAIN):
        for event in pygame.event.get():
            if event.type == QUIT:
                api.IS_QUIT = True
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    if buttons.is_clicked(event.pos,"START GAME"):
                        MAIN.run_command()
                        CURRENT_PAGE = SHOWING_END
                        ENDS.set_text(api.get_intro())
                        MESSAGE.set_text("Session started")
                        api.END_GAME = False
                    elif buttons.is_clicked(event.pos,"LOAD GAME"):
                        api.IS_LOADING = True
    ## Game page
    elif CURRENT_PAGE.has_id(constants.PAGE_GAME):
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
                elif event.key == K_UP:
                    COMMANDLINE.reverse_one_command()
                    TEXTINPUT = COMMANDLINE.get_text()
                elif event.key == K_DOWN:
                    COMMANDLINE.forward_one_command()
                    TEXTINPUT = COMMANDLINE.get_text()
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
                elif api.TIME_SPENT != 0:
                    section.set_stale()
                elif isinstance(section,MessageSection):
                    section.set_stale()
                if isinstance(section,NoteSection) and api.DECRYPT_ENQUEUD:
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

    if api.IS_LOADING:
        api.IS_LOADING = False
        previous_page = CURRENT_PAGE
        CURRENT_PAGE = SHOWING_LOAD
        SAVES.reload()
        LOADS.reload()
    elif api.IS_SAVING:
        api.IS_SAVING = False
        previous_page = CURRENT_PAGE
        CURRENT_PAGE = SHOWING_SAVE
        SAVES.reload()
        LOADS.reload()
    elif api.IS_MENU:
        api.IS_MENU = False
        CURRENT_PAGE = SHOWING_MAIN

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
                    api.IS_MENU = True
        # update for end page

    # get rendered imgs from sections
    FONT_IMAGES = {}
    for section in CURRENT_PAGE.get_sections():
        renders = section.render_font(FONT)
        for img,loc in renders.items():
            FONT_IMAGES[img] = loc

    # display
    SCREEN.fill(constants.BLACK)
    # borders
    for section in CURRENT_PAGE.get_sections():
        if display.has_border(section.get_id()):
            for pic in display.DISPLAY_RECT[section.get_id()]:
                pygame.draw.rect(SCREEN, *pic)
    # save/load borders
    if CURRENT_PAGE.has_id(constants.PAGE_LOAD) or CURRENT_PAGE.has_id(constants.PAGE_SAVE):
        for i in range(len(display.SLOT_LIST)):
            slot = display.SLOT_LIST[i]
            pygame.draw.rect(SCREEN,*display.BUTTON_RECT[slot][display.BUTTON_DISPLAY_KEY[slot]])
            slot_text = LOADS.get_slot_info(i)
            button_img = FONT.render(slot_text,True,buttons.BUTTON_FONT_COLOR[slot][display.BUTTON_DISPLAY_KEY[slot]])
            button_loc = [*buttons.BUTTON_DICT[slot]]
            button_loc[0] += constants.OFF_BUTTON[0]
            button_loc[1] += constants.OFF_BUTTON[1]
            FONT_IMAGES[button_img] = button_loc
    # buttons
    for button in CURRENT_PAGE.get_buttons():
        pygame.draw.rect(SCREEN,*display.BUTTON_RECT[button][display.BUTTON_DISPLAY_KEY[button]])
        button_img = FONT.render(button,True,buttons.BUTTON_FONT_COLOR[button][display.BUTTON_DISPLAY_KEY[button]])
        button_loc = [*buttons.BUTTON_DICT[button]]
        button_loc[0] += constants.OFF_BUTTON[0]
        button_loc[1] += constants.OFF_BUTTON[1]
        FONT_IMAGES[button_img] = button_loc

    # img/text
    for img,loc in FONT_IMAGES.items():
        SCREEN.blit(img,loc)  
    pygame.display.update()
        

pygame.quit()