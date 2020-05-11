import BE.old as old
import BE.actions as actions
import constants
import BE.logs_new as logs_new
import BE.blocks as blocks
import BE.decodes as decodes
import BE.saving as saving

# constants
IS_QUIT = False
IS_SAVING = False
IS_LOADING = False
IS_MENU = False
END_GAME = False
END_RESULT = 0
END_STATUS = ""
END_MESSAGE = ""
TOTAL_TIME = old.total_time
TIME_SPENT = 0
DECRYPT_ENQUEUD = False
FLAGS = old.flags


### TO DO
# end/start sequence
# save and load commands to be saved as section-switching commands
# button to return to main menu
# button to reset all saves
# save/load shortcut shown in save/load page

# section mapping
SECTION_MAPPING = {\
    0  : constants.SECT_READ,\
    1  : constants.SECT_MSG,\
    2  : constants.SECT_READ,\
    3  : constants.SECT_READ,\
    4  : constants.SECT_MSG,\
    5  : constants.SECT_MSG,\
    6  : constants.SECT_MSG,\
    7  : constants.SECT_MSG,\
    8  : constants.SECT_MSG,\
    9  : constants.SECT_NOTE,\
    10 : constants.SECT_READ,\
    14 : constants.SECT_MSG,\
    15 : constants.SECT_NOTE,\
    16 : constants.SECT_MSG,\
    17 : constants.SECT_MSG
}

def get_intro():
    return old.print_intro()

def get_save_slot_info():
    info = saving.read_save()
    if info == 'Unable to load save file':
        return False, info
    return True, info

def run_command(comm_id, *args):
    '''
    Reserve for save/load
    '''
    global IS_SAVING, IS_LOADING, END_GAME, TIME_SPENT, TOTAL_TIME
    if not (comm_id in [11,12]):
        return False, "Not valid"
    argument_list = [FLAGS,TOTAL_TIME,*args]
    text, TOTAL_TIME = old.action_command_call[comm_id](*argument_list)
    # reset variables if load
    if comm_id == 12:
        IS_SAVING = False
        IS_LOADING = False
        END_GAME = False
        TIME_SPENT = 0
    if comm_id == 11:
        if text == 'Game saved':
            return True, text
    else:
        if text == 'Game loaded' or text == 'Game restarted':
            return True, text
    return False, text

def run_game_command(comm_id, *args):
    '''
    Returns text, section id
    '''
    global END_GAME, END_RESULT, END_MESSAGE, END_STATUS, TOTAL_TIME, FLAGS, TIME_SPENT, DECRYPT_ENQUEUD
    global IS_QUIT, IS_SAVING, IS_LOADING, IS_MENU
    argument_list = [FLAGS,TOTAL_TIME,*args]
    # check quit
    error_code = is_special(comm_id)
    if error_code != 4:
        if error_code == 0:
            IS_MENU = True
            return 'Quitting the session...', constants.SECT_MSG
        if error_code == 5:
            IS_SAVING = True
            return 'Switching to saving...', constants.SECT_MSG
        if error_code == 6:
            IS_LOADING = True
            return 'Switching to loading...', constants.SECT_MSG     
    # check doable by flag
    error_code = can_be_done(comm_id, FLAGS)
    if error_code != 4:
        if error_code == 1:
            return "Root access needed", constants.SECT_MSG
        else:
            return "Command not recognized. Are you missing any file/script?", constants.SECT_MSG
    # check correct syntac
    error_code = is_valid(comm_id, *argument_list)
    if error_code != 4:
        return "Invalid syntax", constants.SECT_MSG
    # run command
    previous_time = TOTAL_TIME
    text, TOTAL_TIME = old.action_command_call[comm_id](*argument_list)
    TIME_SPENT = previous_time - TOTAL_TIME
    # post command
    DECRYPT_ENQUEUD = (comm_id == 1)
    # update block variation
    for key in logs_new.LOG_VARIATIONS.keys():
        if logs_new.LOG_NEED_FLAGS[key] in list(FLAGS.keys()):
            logs_new.LOGS_NEW[key[:6]] = logs_new.LOG_VARIATIONS[key]
    # update new block status
    # update new day
    if TOTAL_TIME <= 24 and not old.day_check["Day 1"]:
        blocks.BLOCKS_NEW["0611"] = True 
        if not ("Another day" in list(FLAGS.keys())):
            FLAGS["WIPED"] = True
        old.day_check["Day 1"] = True
    if TOTAL_TIME <= 12 and not old.day_check["Day 2"]:
        blocks.BLOCKS_NEW["0612"] = True
        if not ("Another CHIBI" in list(FLAGS.keys())):
            FLAGS["DISAPPEARED"] = True
        old.day_check["Day 2"] = True
    if TOTAL_TIME <= 0 and not old.day_check["Day 3"]:
        END_GAME = True
        return "Time's up", constants.SECT_END
    # update special command
    if "p5-9" in list(FLAGS.keys()) and decodes.KEYFLAG["last_piece.bpt"] and not ("Assembled" in list(FLAGS.keys())):
        FLAGS["Assembled"] = True
    # check dead
    for i in range(len(old.flag_dead)):
        if old.flag_dead[i] in FLAGS:
            # print("Disconnected - " + flag_dead[i])
            END_RESULT = old.flag_dead_link[i]
            END_GAME = True
            END_MESSAGE = old.end_messages[END_RESULT]
            END_STATUS = old.end_statuses[END_RESULT]
            return "Disconnected", constants.SECT_MSG
    # check end game
    if "MISSION END" in list(FLAGS.keys()):
        END_RESULT = 7
        END_GAME = True
        END_MESSAGE = old.end_messages[END_RESULT]
        END_STATUS = old.end_statuses[END_RESULT]
        return "Code running...", constants.SECT_MSG
    # check which section do info text go to
    return text, SECTION_MAPPING[comm_id]

def update_helpful_note(helpful_section):
    '''
    Updates helpful section, also does decrypting update
    Returns helpful section
    '''
    isRoot = "Root Access" in list(old.flags.keys())
    remove_list = []
    for item in list(actions.decrypt_track.keys()):
        actions.decrypt_track[item] -= TIME_SPENT
        if actions.decrypt_track[item] <= 0:
            actions.update_block_status(item,actions.is_in_which_block_group(item))
            remove_list.append(item)
    for item in remove_list:
        actions.decrypt_track.pop(item, None)
    tips = old.print_helpful_note(TOTAL_TIME,isRoot)
    if len(remove_list) > 0:
        tips += "! Some block(s) have finished decrypting"
    helpful_section.set_text(tips)
    return helpful_section

def is_special(comm_id):
    if comm_id == 11:
        return 5
    if comm_id == 12:
        return 6
    if comm_id == 13:
        return 0
    return 4

def can_be_done(comm_id, flags):
    if comm_id in list(old.action_flags.keys()):
        if not ("Root Access" in list(flags.keys())) and "Root Access" in list(old.action_flags[comm_id]):
            # command_status = "Root access needed"
            return 1
        else:
            for flag in old.action_flags[comm_id]:
                if not (flag in list(flags.keys())):
                    # command_status = "Command not recognized. Are you missing any package/script? Watch dtube or find files via logs"
                    return 2
    return 4

def is_valid(comm_id, *args):
    if not old.action_validation[comm_id](*args):
        # command_status = "Invalid syntax"
        return 3
    return 4