import pygame
import time
from pygame.locals import *
from pygame.rect import *

import constants
import api
import buttons
import display

from Sections.CommandSection import CommandSection
from Sections.MessageSection import MessageSection
from Sections.ReadSection import ReadSection
from Sections.NoteSection import NoteSection
from Sections.HelpfulSection import HelpfulSection
from Sections.EndSection import EndSection
from Sections.MainSection import MainSection
from Sections.LoadSection import LoadSection
from Sections.SaveSection import SaveSection
from Sections.CreditSection import CreditSection

from Page import Page

pygame.init()

SCREEN = pygame.display.set_mode(constants.SCREEN_SIZE)
FONT = pygame.font.SysFont('consolas',20)
pygame.display.set_caption("From CHIBI")

# load images
IMG_MAIN = pygame.image.load("img/main_title.png")
IMG_MAIN = pygame.transform.scale(IMG_MAIN,constants.SCREEN_SIZE)
IMG_MUSIC_ON = pygame.image.load("img/music_on.png")
IMG_MUSIC_ON = pygame.transform.scale(IMG_MUSIC_ON,(constants.RECT_MUSIC[2],constants.RECT_MUSIC[3]))
IMG_MUSIC_OFF = pygame.image.load("img/music_off.png")
IMG_MUSIC_OFF = pygame.transform.scale(IMG_MUSIC_OFF,(constants.RECT_MUSIC[2],constants.RECT_MUSIC[3]))

# music
pygame.mixer.init()
MUSIC_NAME = 'bgm/main.ogg'
MUSIC_PLAYER = pygame.mixer.Sound(MUSIC_NAME)
IS_UNMUTED = False
IS_MUTED = False
PLAYING = True

# text input setup
TEXTINPUT = ""
FONT_IMAGES = {}  # map rendered img to location (x,y)
deleting = False
delete_speed = 20

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
CREDITS = CreditSection()

SHOWING_GAME = Page(constants.PAGE_GAME, [COMMANDLINE, MESSAGE, NOTES, READS, HELPS])
SHOWING_END = Page(constants.PAGE_END, [ENDS])
SHOWING_MAIN = Page(constants.PAGE_MAIN, [MAIN], ["START GAME", "LOAD GAME","CREDITS","QUIT GAME"])
SHOWING_LOAD = Page(constants.PAGE_LOAD, [LOADS], ["RESTART","RETURN","LOAD"])
SHOWING_SAVE = Page(constants.PAGE_SAVE, [LOADS], ["RESTART","RETURN GAME","SAVE"])
SHOWING_CREDITS = Page(constants.PAGE_CRED, [CREDITS], ["RETURN"])

# starting
previous_page = SHOWING_MAIN
CURRENT_PAGE = SHOWING_MAIN
SAVES.reload()
LOADS.reload()
MUSIC_PLAYER.play(loops=-1,fade_ms=1000)

while not api.IS_QUIT:
    # check hover button
    mouse_pos = pygame.mouse.get_pos()
    for button in CURRENT_PAGE.get_buttons():
        if buttons.is_clicked(mouse_pos,button):
            display.BUTTON_DISPLAY_KEY[button] = 1
        else:
            display.BUTTON_DISPLAY_KEY[button] = 0
    if CURRENT_PAGE.has_id(constants.PAGE_CRED):
        for event in pygame.event.get():
            if event.type == QUIT:
                api.IS_QUIT = True
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    if buttons.is_clicked(event.pos,"RETURN"):
                        CURRENT_PAGE = SHOWING_MAIN
                # scrolling for credits
                elif event.button == 4 and buttons.is_hovered(event.pos,constants.SECT_CRED):
                    CREDITS.shift_up_one_row()
                elif event.button == 5 and buttons.is_hovered(event.pos,constants.SECT_CRED):
                    CREDITS.shift_down_one_row()
    ## Save game
    elif CURRENT_PAGE.has_id(constants.PAGE_SAVE):
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
                        for section in SHOWING_GAME.get_sections():
                            section.reset()
                        ENDS.set_text(api.get_intro())
                        MESSAGE.set_text(message_text)
                        # music
                        if PLAYING:
                            pygame.mixer.stop()
                            MUSIC_NAME = "bgm/one.ogg"
                            MUSIC_PLAYER = pygame.mixer.Sound(MUSIC_NAME)
                            MUSIC_PLAYER.play(loops=-1,fade_ms=5000)
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
                            day_after_load = api.what_day_is_it()
                            # music
                            if PLAYING:
                                if day_after_load == 1:
                                    pygame.mixer.stop()
                                    MUSIC_NAME = "bgm/one.ogg"
                                    MUSIC_PLAYER = pygame.mixer.Sound(MUSIC_NAME)
                                    MUSIC_PLAYER.play(loops=-1,fade_ms=5000)
                                elif day_after_load == 2:
                                    pygame.mixer.stop()
                                    MUSIC_NAME = "bgm/two.ogg"
                                    MUSIC_PLAYER = pygame.mixer.Sound(MUSIC_NAME)
                                    MUSIC_PLAYER.play(loops=-1,fade_ms=5000)
                                elif day_after_load == 3:
                                    pygame.mixer.stop()
                                    MUSIC_NAME = "bgm/three.ogg"
                                    MUSIC_PLAYER = pygame.mixer.Sound(MUSIC_NAME)
                                    MUSIC_PLAYER.play(loops=-1,fade_ms=5000)
                    elif buttons.is_clicked(event.pos,"RESTART"):
                        LOADS.set_restart()
                        load_result, message_text, section_id = *LOADS.run_command(), constants.SECT_MSG
                        CURRENT_PAGE = SHOWING_END
                        for section in SHOWING_GAME.get_sections():
                            section.reset()
                        ENDS.set_text(api.get_intro())
                        MESSAGE.set_text(message_text)
                        # music
                        if PLAYING:
                            pygame.mixer.stop()
                            MUSIC_NAME = "bgm/one.ogg"
                            MUSIC_PLAYER = pygame.mixer.Sound(MUSIC_NAME)
                            MUSIC_PLAYER.play(loops=-1,fade_ms=5000)
                    for button in display.SLOT_LIST:
                        if buttons.is_clicked(event.pos,button):
                            LOADS.select(button)
                            break
    ## Main page
    elif CURRENT_PAGE.has_id(constants.PAGE_MAIN):
        # check music mute
        if IS_MUTED:
            pygame.mixer.pause()
            IS_MUTED = False
            IS_UNMUTED = False
            PLAYING = False
        if IS_UNMUTED:
            pygame.mixer.unpause()
            IS_MUTED = False
            IS_UNMUTED = False  
            PLAYING = True    
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
                        # music
                        if PLAYING:
                            pygame.mixer.stop()
                            MUSIC_NAME = "bgm/one.ogg"
                            MUSIC_PLAYER = pygame.mixer.Sound(MUSIC_NAME)
                            MUSIC_PLAYER.play(loops=-1,fade_ms=5000)
                    elif buttons.is_clicked(event.pos,"LOAD GAME"):
                        api.IS_LOADING = True
                    elif buttons.is_clicked(event.pos,"QUIT GAME"):
                        api.IS_QUIT = True
                    elif buttons.is_clicked(event.pos,"CREDITS"):
                        CREDITS.set_text(constants.CREDITS)
                        CURRENT_PAGE = SHOWING_CREDITS
                    elif buttons.is_clicked(event.pos,"MUSIC"):
                        if PLAYING: IS_MUTED = True
                        else: IS_UNMUTED = True
    ## Game page
    elif CURRENT_PAGE.has_id(constants.PAGE_GAME):
        # deleting for cli
        if deleting: 
            delete_speed -= 1
            if delete_speed == 0:
                delete_speed = 20
                if len(TEXTINPUT) > 0:
                    TEXTINPUT = TEXTINPUT[:-1]
        else:
            delete_speed = 20

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
                # scrolling for helps
                elif event.button == 4 and buttons.is_hovered(event.pos,constants.SECT_HELP):
                    HELPS.shift_up_one_row()
                elif event.button == 5 and buttons.is_hovered(event.pos,constants.SECT_HELP):
                    HELPS.shift_down_one_row()
                # scrolling for msg
                elif event.button == 4 and buttons.is_hovered(event.pos,constants.SECT_MSG):
                    MESSAGE.shift_up_one_row()
                elif event.button == 5 and buttons.is_hovered(event.pos,constants.SECT_MSG):
                    MESSAGE.shift_down_one_row()
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    day_before_cmd = api.what_day_is_it()
                    COMMANDLINE.set_text(TEXTINPUT)
                    COMMANDLINE.process_command()
                    message_text, section_id = COMMANDLINE.run_command()
                    HELPS = api.update_helpful_note(HELPS)
                    TEXTINPUT = ""
                    day_after_cmd = api.what_day_is_it()
                    # music
                    if day_before_cmd != day_after_cmd and PLAYING and not api.END_GAME:
                        if day_after_cmd == 1:
                            pygame.mixer.fadeout(3000)
                            MUSIC_NAME = "bgm/one.ogg"
                            MUSIC_PLAYER = pygame.mixer.Sound(MUSIC_NAME)
                            MUSIC_PLAYER.play(loops=-1,fade_ms=5000)
                        elif day_after_cmd == 2:
                            pygame.mixer.fadeout(3000)
                            MUSIC_NAME = "bgm/two.ogg"
                            MUSIC_PLAYER = pygame.mixer.Sound(MUSIC_NAME)
                            MUSIC_PLAYER.play(loops=-1,fade_ms=5000)
                        elif day_after_cmd == 3:
                            pygame.mixer.fadeout(3000)
                            MUSIC_NAME = "bgm/three.ogg"
                            MUSIC_PLAYER = pygame.mixer.Sound(MUSIC_NAME)
                            MUSIC_PLAYER.play(loops=-1,fade_ms=5000)
                elif event.key == K_BACKSPACE:
                    if len(TEXTINPUT) > 0:
                        TEXTINPUT = TEXTINPUT[:-1]
                    deleting = True
                    delete_speed = 160
                elif event.key == K_UP:
                    COMMANDLINE.reverse_one_command()
                    TEXTINPUT = COMMANDLINE.get_text()
                elif event.key == K_DOWN:
                    COMMANDLINE.forward_one_command()
                    TEXTINPUT = COMMANDLINE.get_text()
                else:
                    TEXTINPUT += event.unicode
            if event.type == KEYUP:
                if event.key == K_BACKSPACE and deleting:
                    deleting = False

        COMMANDLINE.set_text(TEXTINPUT)
        TEXTINPUT = COMMANDLINE.get_text()

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
            if api.TIME_SPENT != 0:
                READS.set_stale()
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
            # music
            if PLAYING:
                ending = api.what_ending_is_it()
                pygame.mixer.stop()
                MUSIC_NAME = "bgm/" + str(ending) + ".ogg"
                MUSIC_PLAYER = pygame.mixer.Sound(MUSIC_NAME)
                MUSIC_PLAYER.play(loops=-1,fade_ms=5000)

    ## End page (end/start)
    elif CURRENT_PAGE.has_id(constants.PAGE_END):
        # event check for end page
        for event in pygame.event.get():
            if event.type == QUIT:
                api.IS_QUIT = True
            if event.type == KEYDOWN:
                if event.key == K_RETURN and not api.END_GAME and ENDS.finished():
                    COMMANDLINE.set_text("help")
                    COMMANDLINE.process_command()
                    message_text, section_id = COMMANDLINE.run_command()
                    HELPS = api.update_helpful_note(HELPS)
                    TEXTINPUT = ""
                    CURRENT_PAGE = SHOWING_GAME
                elif event.key == K_RETURN and api.END_GAME and ENDS.finished():
                    # switch to main menu
                    api.IS_MENU = True
                elif event.key == K_RETURN and not ENDS.finished():
                    ENDS.advance()

    # switch page
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
        if PLAYING:
            pygame.mixer.stop()
            MUSIC_NAME = "bgm/main.ogg"
            MUSIC_PLAYER = pygame.mixer.Sound(MUSIC_NAME)
            MUSIC_PLAYER.play(loops=-1,fade_ms=2000)

    # get rendered imgs from sections
    FONT_IMAGES = {}
    for section in CURRENT_PAGE.get_sections():
        renders = section.render_font(FONT)
        for img,loc in renders.items():
            FONT_IMAGES[img] = loc

    # display
    SCREEN.fill(constants.BLACK)
    # background img & music
    if CURRENT_PAGE.has_id(constants.PAGE_MAIN):
        SCREEN.blit(IMG_MAIN,(0,0,*constants.SCREEN_SIZE))
        if PLAYING: 
            SCREEN.blit(IMG_MUSIC_ON, constants.RECT_MUSIC)
        else:
            SCREEN.blit(IMG_MUSIC_OFF, constants.RECT_MUSIC)
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