import actions
import validation
import blocks
import logs_new
import decodes

### endings
end_game = False
end_statuses = {\
    0 : "Code integrity: True; Mission success: False; Message: Good enough",\
    1 : "Code integrity: True; Mission success: False; Message: Thank you",\
    2 : "Missing log files. Missing log files...",\
    3 : "Report: Malware detected (Severity:8); Action: Security analysis; Initializing analysis...",\
    4 : "Report: Malware detected (Severity:6); Action: Log erasure; Initializing erasure...",\
    5 : "Report: Malware detected (Severity:3); Action: Code transfer; Initializing transfer...",\
    6 : "Report: Malware detected (Severity:10); Action: Code corruption; Initialization corruption...",\
    7 : "Code integrity: True; Mission success: True; Message: You did it!"\
}
end_messages = {\
    0 : "You've managed to save Chibi! Want to try to figure out what exactly is Chibi's identity? Maybe you can try decoding files you have - the password can be found by remote accessing or talking to an expert",\
    1 : "You've managed to save Chibi and tell the truth to Luv! You're almost there - try to decode everything you have! Search for a way to do something that shouldn't be possible at first glance..",\
    2 : "You are missing some files... try to look around and save attachments",\
    3 : "You've exposed Chibi to the authorities... don't be so honest in replying next time",\
    4 : "You've acted too suspicious and drew suspicion from authorities. Try to reply more often/differently next time",\
    5 : "You've drawn suspicion to yourself either by replying wrongly or doing something you shouldn't be doing",\
    6 : "You've exposed Chibi and also drawn suspicion to yourself. The authorities had to take care of you. Don't reply so honestly next time.",\
    7 : "You've managed to fulfill Chibi's mission! Do you understand what Chibi is now?"\
}
end_result = 0

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
}

action_flags = {\
    5 : ["Root Access","Remote Access"],\
    6 : ["Root Access","Change Time"],\
    7 : ["Root Access","Decode Cohab's relic"],\
    10: ["Root Access","Decoder"],\
}

def print_helpful_note(isRoot):
    '''
    Prints helpful note and time (reverse time if isRoot)
    '''
    print("<Enter read ",end="")
    if total_time > 24:
        day_int = 3
        time_offset = 24
        print("0610",end="")
    elif total_time > 12:
        day_int = 2
        time_offset = 12
        print("0611",end="")
    else:
        day_int = 1
        time_offset = 0
        print("0612",end="")
    print(" to check new logs. Do this regularly>")
    print("<Press help commands to check available commands>")
    if not isRoot:
        print("<Day " + str(day_int) + " Time " + str(total_time - time_offset) + ">")
    else:
        print("<Day " + str(4 - day_int) + " Time " + str(12 - (total_time - time_offset)) + ">")

print("=====================================")
print("Security warning (Level 5): Change detected in memory database")
print("Security warning (Level 2): Change detected in time display")
print("Security warning (Level 2): Change detected in message display")
print("Due to security warning(s), root privilege will be disabled. Some functionalities may be unavailable")
print("Establishing connection...")
print("=====================================")
print("Year: 7204")
print("Session: 4498032")
print("Connection status: Good")
print("Address: cat_fish@vsp.tc")
print("Message: Save Chibi! Press help to get started")
print("=====================================")
while not end_game:
    command_status = "Command succeeded"
    # get user input
    user_command = input("Nekoi>> ")
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
            break
        # check for commands that need flags
        if command_int in list(action_flags.keys()):
            if not ("Root Access" in list(flags.keys())):
                command_status = "Root access needed. Enter root"
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
        if command_status == "Command succeeded":
            command_status, total_time = action_command_call[command_int](flags,total_time,*argument_list)
    # update block variation
    for key in logs_new.LOG_VARIATIONS.keys():
        if logs_new.LOG_NEED_FLAGS[key] in list(flags.keys()):
            logs_new.LOGS_NEW[key[:6]] = logs_new.LOG_VARIATIONS[key]
    # update new block status
    # update new day
    if total_time <= 24:
        blocks.BLOCKS_NEW["0611"] = True 
        if not ("Another day" in list(flags.keys())):
            flags["WIPED"] = True
    if total_time <= 12:
        blocks.BLOCKS_NEW["0612"] = True
        if not ("p5-9" in list(flags.keys())) or not decodes.KEYFLAG["last_piece.bpt"]:
            flags["DISAPPEARED"] = True
    print("")
    print(command_status)
    print("")
    # print helpful note & time
    isRoot = "Root Access" in list(flags.keys())
    print_helpful_note(isRoot)
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
    if total_time == 0:
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