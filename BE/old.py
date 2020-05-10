import BE.actions as actions
import BE.validation as validation
import BE.blocks as blocks
import BE.logs_new as logs_new
import BE.decodes as decodes
import BE.saving as saving

### endings
end_game = False
end_statuses = {\
    0 : "Code integrity: True; Mission success: False; Message: At least you survive",\
    1 : "Code integrity: True; Mission success: False; Message: Thank you for passing on the truth about LUCA",\
    2 : "Code integrity: False; Message: Code files not assembled, program failure",\
    3 : "Report: Malware detected (Severity:8); Action: Security analysis; Initializing analysis...",\
    4 : "Report: Malware detected (Severity:6); Action: Log erasure; Initializing erasure...",\
    5 : "Report: Malware detected (Severity:3); Action: Code transfer; Initializing transfer...",\
    6 : "Report: Malware detected (Severity:10); Action: Code corruption; Initialization corruption...",\
    7 : "Code integrity: True; Mission success: True; Message: You did it!; Special Message: decode ? do+not+forget"\
}
end_messages = {\
    0 : "You've managed to save CHIBI! Want to try to fulfill the mission? Maybe you can try decoding files you have - the password can be found by remote accessing or talking to an expert. Files of the same author tend to have the same decoding key. And if you think you have every file possible... are you sure? Don't be naive and believe everything you are told, and try to talk to other people",\
    1 : "You've managed to save CHIBI and tell the truth to Luv! You're almost there - did you decode every files possible? Run every command possible?",\
    2 : "You are either missing files... or forgetting to run a specific command that's needed for your survival",\
    3 : "You've exposed CHIBI to the authorities... don't be so honest in replying next time",\
    4 : "You've acted too suspicious and drew suspicion from authorities. Try to reply more often/differently next time",\
    5 : "You've drawn suspicion to yourself either by replying wrongly or doing something you shouldn't be doing",\
    6 : "You've exposed CHIBI and also drawn suspicion to yourself. The authorities had to take care of you. Don't reply so honestly next time",\
    7 : "You've managed to fulfill CHIBI's main mission while also surviving! Do you understand what CHIBI is now? If you haven't... have you tried to decode all the files?"\
}
end_result = actions.end_result

flag_dead_link = {\
    0  : 4,\
    1  : 5,\
    2  : 6,\
    3  : 3,\
    4  : 2,\
}

### time units
total_time = 36

### flags
flags = {}

flag_dead = [ "WIPED", "RELOCATED", "KILLED", "DISCOVERED", "DISAPPEARED" ]

day_check = actions.day_check

### actions
action_cmd = {\
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

action_validation = {
    0  : validation.check_dt,\
    1  : validation.check_decrypt,\
    2  : validation.check_read,\
    3  : validation.check_work,\
    4  : validation.check_root,\
    5  : validation.check_remote,\
    6  : validation.check_time,\
    7  : validation.check_overspace,\
    8  : validation.check_contact,\
    9  : validation.check_help,\
    10 : validation.check_decode,\
    11 : validation.check_save,\
    12 : validation.check_load,\
    14 : validation.check_reply,\
    15 : validation.check_notes,\
    16 : validation.check_chibi,\
    17 : validation.check_attachment,\
}

action_command_call = {\
    0  : actions.demtube,\
    1  : actions.decrypt,\
    2  : actions.read,\
    3  : actions.work,\
    4  : actions.root,\
    5  : actions.remote_access,\
    6  : actions.time_change,\
    7  : actions.overspace,\
    8  : actions.contact,\
    9  : actions.help,\
    10 : actions.decode,\
    11 : actions.save,\
    12 : actions.load,\
    14 : actions.reply,\
    15 : actions.notes,\
    16 : actions.chibi,\
    17 : actions.save_attachment,\
}

action_flags = {\
    # 1 : ["Root Access"],\
    4 : ["Can Root Access"],\
    5 : ["Root Access","Remote Access"],\
    6 : ["Root Access","Change Time"],\
    7 : ["Root Access","Decode Cohab's relic"],\
    16: ["Assembled"],\
}

# text
def print_intro():
    '''
    Prints intro text
    '''
    print("=====================================")
    print("Security warning (Level 5): Change detected in memory database")
    print("Security warning (Level 2): Change detected in time display")
    print("Security warning (Level 2): Change detected in message display")
    print("Security warning (Level 2): Change detected in help display")
    print("Due to security warning(s), root privilege will be disabled. Some functionalities may be unavailable")
    print("Establishing connection...")
    print("=====================================")
    print("Year: 7204")
    print("Session: 4498032")
    print("Connection status: Good")
    print("Address: cat_fish@vsp.tc")
    print("Message: mskmcdjsnjnsce[Save CHIBI! Time is running out!]jfnejfnscnjd[Press help to get started]")
    print("=====================================")

def print_helpful_note(total_time,isRoot):
    '''
    Prints helpful note and time (reverse time if isRoot)
    '''
    tips = "1. Enter read "
    if total_time > 24:
        day_int = 3
        time_offset = 24
        tips += "0610"
    elif total_time > 12:
        day_int = 2
        time_offset = 12
        tips += "0611"
    else:
        day_int = 1
        time_offset = 0
        tips += "0612"
    tips += " to check new logs\n"
    tips += "2. Enter help commands to check available commands\n"
    if not isRoot:
        tips = "<Day " + str(day_int) + " Time " + str(total_time - time_offset) + ">\n" + tips
    else:
        tips = "<Day " + str(4 - day_int) + " Time " + str(12 - (total_time - time_offset)) + ">\n" + tips
    tips += "3. Windows are scrollable"
    if "Assembled" in list(flags.keys()) and not ("Another CHIBI" in list(flags.keys())):
        tips += "???Message: all code files detected, please run special command\n"
    return tips

# SAVE INITIALIZING
# saving.initialize_save()
# actions.set_restart_point(flags,total_time)

# RESTART LOOP
not_quit = False
command_status = 'Game restarted'
while not_quit:
    # GAME START
    while not end_game:
        if command_status == 'Game restarted':
            print_intro()
        command_status = "Command succeeded"
        # get user input
        user_command = input("Nekoi>> ").strip()
        # break down command
        command_int = -1
        command_list = user_command.split(' ')
        # check for too many arguments
        if len(command_list) > 4:
            command_status = "Too many arguments"
        # check if command word matches
        for i in list(action_cmd.keys()):
            if command_list[0] == action_cmd[i]:
                command_int = i
                break
        if command_int == -1:
            command_status = "Command not found"
        else:
            # check for quit
            if command_int == 13:
                end_result = -1
                not_quit = False
                break
            # check for commands that need flags
            if command_int in list(action_flags.keys()):
                if not ("Root Access" in list(flags.keys())) and "Root Access" in list(action_flags[command_int]):
                    command_status = "Root access needed"
                else:
                    for flag in action_flags[command_int]:
                        if not (flag in list(flags.keys())):
                            command_status = "Command not recognized. Are you missing any package/script? Watch dtube or find files via logs"
                            break
            # check for argument list
            if command_status == "Command succeeded":
                argument_list = command_list[1:]
                if not action_validation[command_int](flags,total_time,*argument_list):
                    command_status = "Invalid syntax"
            # run command
            previous_time = total_time
            if command_status == "Command succeeded":
                command_status, total_time = action_command_call[command_int](flags,total_time,*argument_list)
            time_spent = previous_time - total_time
        # update decrypting status
        if command_int == 12: time_spent = 0
        remove_list = []
        for item in list(actions.decrypt_track.keys()):
            actions.decrypt_track[item] -= time_spent
            if actions.decrypt_track[item] <= 0:
                actions.update_block_status(item,actions.is_in_which_block_group(item))
                remove_list.append(item)
        for item in remove_list:
            actions.decrypt_track.pop(item, None)
        # update block variation
        for key in logs_new.LOG_VARIATIONS.keys():
            if logs_new.LOG_NEED_FLAGS[key] in list(flags.keys()):
                logs_new.LOGS_NEW[key[:6]] = logs_new.LOG_VARIATIONS[key]
        # update new block status
        # update new day
        if total_time <= 24 and not day_check["Day 1"]:
            blocks.BLOCKS_NEW["0611"] = True 
            if not ("Another day" in list(flags.keys())):
                flags["WIPED"] = True
            day_check["Day 1"] = True
        if total_time <= 12 and not day_check["Day 2"]:
            blocks.BLOCKS_NEW["0612"] = True
            if not ("Another CHIBI" in list(flags.keys())):
                flags["DISAPPEARED"] = True
            day_check["Day 2"] = True
        if total_time <= 0 and not day_check["Day 3"]:
            end_game = True
        # update special command
        if "p5-9" in list(flags.keys()) and decodes.KEYFLAG["last_piece.bpt"] and not ("Assembled" in list(flags.keys())):
            flags["Assembled"] = True
        print("")
        print(command_status)
        print("")
        # print helpful note & time
        isRoot = "Root Access" in list(flags.keys())
        if command_status != 'Game restarted':
            print_helpful_note(isRoot)
        # decryption noti
        if len(remove_list) > 0:
            print('<Some block(s) have finished decrypting>')
        # check dead
        for i in range(len(flag_dead)):
            if flag_dead[i] in flags:
                print("Disconnected - " + flag_dead[i])
                end_result = flag_dead_link[i]
                end_game = True
                break
        # check end game
        if "MISSION END" in list(flags.keys()):
                end_result = 7
                end_game = True
                break

    # ending resolution
    if end_result == -1:
        print("See you soon!")
    else:
        print("=====================================")
        if end_result in list(flag_dead_link.values()):
            print(end_statuses[end_result])
        else:
            if "Luca's secret" in list(flags.keys()):
                end_result = 1
            if "MISSION END" in list(flags.keys()):
                end_result = 7
            print(end_statuses[end_result])
        print("=====================================")
        print(end_messages[end_result])
    
    # restart
    if not_quit:
        print("=====================================")
        print("Restarting sequence. Type 'proceed' or 'terminate' to continue")
        while True:
            choice = input(">> ").strip()
            if choice in ["proceed",'terminate']:
                break
            print("Invalid input. Type 'proceed' or 'terminate'")
        if choice == 'terminate':
            not_quit = False
            print('See you soon!')
        else:
            print('Sequence executed. Please wait...')
            command_status, total_time = actions.load(flags,total_time,'restart')
            end_game = False
            print("=====================================")
            