'''
All action functions are called with flags and current_time as first two arguments
All action functions are to update flags if necessary and current_time if the command goes through
'''

import schedule
import logs
import logs_new
import blocks
import remote
import decodes
import actions_help

flag_demtube_triggers = {\
    34 : "Can Root Access",\
    26 : "Remote Access",\
    28 : "Pre-war?",\
    22 : "Animals",\
    12 : "Fast Decrypt",\
    8  : "Decoder",\
}

flag_work_triggers = {\
    20 : "Change Time",\
}

flag_contact = 0

contact_red = ["266694:990002::", "9933:12:45900:009::", "11111:111:1111:1::"]

def chibi(*args):
    '''
    Returns string of result
    '''
    flags = args[0]
    current_time = args[1]
    if not is_flag_triggered(flags,"Another CHIBI"):
        tips =  "File assembling in progress... Success. Running self replication sequence... Success. Scanning network for next target... Success. Initializing persona code 'chibisuke'... Success. Initializing file transfer to target... Success. Message: mission not fulfilled, please run mission"
        flags["Another CHIBI"] = True
        current_time -= 2
    else:
        tips = "Code assembled. File transfer already in progress. Message: mission not fulfilled, please run mission"
    return tips, current_time

def notes(*args):
    '''
    Returns string of helpful notes
    '''
    current_time = args[1]
    if len(args) == 2:
        return actions_help.GENERAL_HELP + "\n\n" + actions_help.DEMTUBE_HELP + "\n\n" + actions_help.WORK_HELP, current_time
    else:
        key = args[2]
        if key in ["general","dt","work"]:
            if key == "general":
                return actions_help.GENERAL_HELP, current_time
            elif key == "dt":
                return actions_help.DEMTUBE_HELP, current_time
            else:
                return actions_help.WORK_HELP, current_time
        else:
            return "Notes not found", current_time


def save(flags,current_time):
    '''
    Saves game
    '''
    return "This function is not yet supported", current_time

def load(flags,current_time):
    '''
    Loads game
    '''
    return "This function is not yet supported", current_time

def overspace(flags,current_time):
    '''
    Returns string of result
    '''
    current_time -= 2
    if is_flag_triggered(flags,"Overspace"):
        flags["MISSION END"] = True
        return "Attempting to connect. . . . . . . . . . . . . . . . . . . . . Success", current_time
    else:
        return "Attempting to connect. . . . . . . . . . . . . . . . . . . . . . . . .", current_time

def time_change(flags,current_time,terminal_id):
    '''
    Returns string of result, and new time
    '''
    if terminal_id != "Chibi":
        return "Error. Security warning", current_time
    else:
        if is_flag_triggered(flags,"Hack Chibi"):
            return "Already done", current_time
        # raise linked flag
        flags["Hack Chibi"] = True
        # update time
        current_time -= 2
        return "Success. Log replication may occur", current_time 

def is_flag_triggered(flags, flagname):
    '''
    Returns bool if flag is set
    '''
    if flagname in list(flags.keys()):
        return flags[flagname]
    return False

def can_reply(flags,reply_id):
    '''
    Returns bool if reply can be used, based on flags
    '''
    if reply_id in list(logs_new.LOG_NEED_FLAGS.keys()):
        flag_needed = logs_new.LOG_NEED_FLAGS[reply_id]
        return is_flag_triggered(flags,flag_needed)
    return True

def reply(*args):
    '''
    Returns either string of result or possible replies to make
    '''
    flags = args[0]
    current_time = args[1]
    log_id = args[2]

    # narrow down wrong id
    if len(log_id) != 6:
        return "Invalid log id", current_time
    # narrow down log that can be replied to (using log time)
    time_list = list(filter(lambda item: current_time - 4 <= item,logs_new.LOG_TIME.keys()))
    time_window = min(time_list,key=lambda item: item - current_time)
    if not (log_id in logs_new.LOG_TIME[time_window]):
        return "Cannot reply to that log at this time", current_time
    # narrow down log with attachment
    if log_id in logs_new.LOG_ATTACHMENT.keys():
        logs_new.LOG_ATTACHMENT[log_id] = True
        if log_id == "061101":
            flags["p5-9"] = True
        elif log_id == "061201":
            decodes.KEYFLAG["catgirl.bpt"] = True
        else:
            if is_flag_triggered(flags,"Cohab") or is_flag_triggered(flags,"Cohab@"): decodes.KEYFLAG["Cohab.clf"] = True
            if is_flag_triggered(flags,"Bpaint") or is_flag_triggered(flags,"Bpaint@"): decodes.KEYFLAG["last_piece.bpt"] = True
        return "Attachment saved", current_time
    # narrow down log that can be replied to
    if not (log_id in logs_new.LOG_NEED_REPLIES.keys()):
        return "Cannot reply to that log", current_time
    # narrow down log that hasn't been replied to
    if not logs_new.LOG_NEED_REPLIES[log_id]:
        return "Log is already replied", current_time
    
    reply_id = logs_new.LOG_LINK_REPLIES[log_id]
    reply_ids = []
    # filter replies by flags
    possible_reply_codes = list(filter(lambda item: can_reply(flags,item), list(logs_new.LOG_REPLIES.keys())))
    # filter replies by log_id
    for repcode in possible_reply_codes:
        if repcode[:6] == reply_id and repcode[6] != "i":
            reply_ids.append(repcode)

    if len(args) == 3:
        result = "Enter reply " + log_id + " followed by reply code. For eg: reply" + log_id + " a "
        for code in reply_ids:
            result += "\n" + code[6] + ": " + logs_new.LOG_REPLIES[code] + "; "
        return result, current_time
    else:
        reply_code = reply_id + args[3]
        if not (reply_code in reply_ids):
            return "Invalid reply code", current_time
        # update reply and flag
        logs_new.LOGS_NEW[reply_id] = "Reply: " + logs_new.LOG_REPLIES[reply_code]
        logs_new.LOG_NEED_REPLIES[log_id] = False
        if reply_code in list(logs_new.LOG_GIVE_FLAGS.keys()):
            flags[logs_new.LOG_GIVE_FLAGS[reply_code]] = True
        # update time
        current_time -= 1
        return "Reply completed", current_time

def demtube(flags,current_time):
    '''
    Returns string of show watched
    '''
    hour_list = sorted(list(schedule.DEMTUBE.keys()),reverse=True)
    for i in range(len(hour_list)):
        if current_time >= hour_list[i]:
            # raise linked flag
            if hour_list[i] in list(flag_demtube_triggers.keys()):
                flags[flag_demtube_triggers[hour_list[i]]] = True
            # update time
            current_time -= 1
            return "Watching: " + schedule.DEMTUBE[hour_list[i]], current_time

def update_block_status(block_id,group_id):
    '''
    Updates block status
    '''
    if group_id == 0:
        blocks.BLOCKS[block_id] = True
    if group_id == 2:
        blocks.BLOCKS_SPECIAL_TWO[block_id] = True
    if group_id == 3:
        blocks.BLOCKS_ROOT[block_id] = True

def decrypt(flags,current_time,block_id):
    '''
    Returns string of result
    '''
    block_group = is_in_which_block_group(block_id)
    if not (block_group in [0,1,2,3]): 
        return "Block not found", current_time
    if block_group == 1:
        return "That block is not encrypted", current_time
    if can_block_be_read(flags,block_id,block_group,current_time):
        return "Block already decrypted", current_time
    # update block list
    update_block_status(block_id,block_group)
    # update time
    if is_flag_triggered(flags,"Fast Decrypt"): 
        current_time -= 1
    else:
        current_time -= 2
    return "Block " + block_id + " has been decrypted", current_time

def get_log_content(log_id, is_old):
    '''
    Returns string in log
    '''
    if is_old:
        return logs.LOGS[log_id]
    else:
        return logs_new.LOGS_NEW[log_id]

def address_to_name(address_string):
    '''
    Returns name corresponding to address
    '''
    if address_string in list(actions_help.ADDRESS_TO_NAME.keys()):
        return actions_help.ADDRESS_TO_NAME[address_string]
    return "Unknown"

def get_log_info(log_id, is_old):
    '''
    Returns sender/recipient string of log
    '''
    if is_old:
        sender = 'Unknown'
        receiver = "Unknown"
        for address in logs.LOGS_SENDER.keys():
            if log_id in logs.LOGS_SENDER[address]:
                sender = address
                break
        for address in logs.LOGS_RECIPIENT.keys():
            if log_id in logs.LOGS_RECIPIENT[address]:
                receiver = address
                break
        return "Log " + log_id + " From " + address_to_name(sender) + " To " + address_to_name(receiver) + ": "
    else:
        for address in logs_new.LOGS_NEW_ADDRESS.keys():
            if log_id in logs_new.LOGS_NEW_ADDRESS[address]:
                return "Log " + log_id + " " + address_to_name(address) + ": "
        return "Log " + log_id + " Unknown: "

def log_reply_status(log_id, current_time):
    '''
    Returns 0 is no reply needed, 1 is reply needed, 2 if reply expired
    '''
    # narrow down log that can be replied to 
    if not (log_id in logs_new.LOG_NEED_REPLIES.keys()):
        return 0
    # narrow down log that is already replied
    if not logs_new.LOG_NEED_REPLIES[log_id]: 
        return 0
    # narrow down log that can be replied to (using log time)
    time_list = list(filter(lambda item: current_time - 4 <= item,logs_new.LOG_TIME.keys()))
    time_window = min(time_list,key=lambda item: item - current_time)
    if not (log_id in logs_new.LOG_TIME[time_window]):
        return 2
    return 1

def can_block_be_read(flags, block_id, group_id, current_time):
    '''
    Return bool whether block can be read
    '''
    if group_id == 0:
        return blocks.BLOCKS[block_id]
    if group_id == 2:
        return blocks.BLOCKS_SPECIAL_TWO[block_id] and current_time <= 24
    if group_id == 3:
        return blocks.BLOCKS_ROOT[block_id] and is_flag_triggered(flags, "Root Access")
    return False

def is_in_which_block_group(block_id):
    '''
    Returns integer indicating which block group does block id belongs to
    '''
    if block_id in list(blocks.BLOCKS.keys()):
        return 0 # original blocks
    if block_id in list(blocks.BLOCKS_NEW.keys()):
        return 1 # new blocks
    if block_id in list(blocks.BLOCKS_SPECIAL_TWO.keys()):
        return 2 # day 2+ blocks
    if block_id in list(blocks.BLOCKS_ROOT.keys()):
        return 3 # root blocks
    return -1

def read(*args):
    '''
    Returns string of result, whether it is read block or read log
    '''
    flags = args[0]
    current_time = args[1]
    if len(args) == 2:
        log_id = read_log(flags,current_time)
        result = ""
        result += get_log_info(log_id,False)
        result += "\n\t" + get_log_content(log_id,False)
        # reply status
        reply_status = log_reply_status(log_id,current_time)
        if reply_status == 2:
            result += "\n\tReply EXPIRED"
        elif reply_status == 1:
            result += show_possible_replies(flags,current_time,log_id)
        return result, current_time
    else:
        block_id = args[2]
        # check whether new or old block
        block_group = is_in_which_block_group(block_id)
        is_old_block = not (block_group == 1)
        # return result if not found
        if block_group == -1:
            return "Block not found", current_time
        # return result of if locked
        if is_old_block:
            if not can_block_be_read(flags,block_id,block_group,current_time):
                return "Block may be locked or inaccessible", current_time
        else:
            if not blocks.BLOCKS_NEW[block_id]:
                return "Block is unavailable at this time", current_time
        log_list = read_block(flags,current_time,block_id,is_old_block,block_group)
        result = "Block " + block_id + ": "
        for i in range(len(log_list)):
            log_id = log_list[i]
            result += "\n\n" + get_log_info(log_id,is_old_block)
            result += "\n\t" + get_log_content(log_id,is_old_block)
            # reply status
            reply_status = log_reply_status(log_id,current_time)
            if reply_status == 2:
                result += "\n\tReply EXPIRED"
            elif reply_status == 1:
                result += show_possible_replies(flags,current_time,log_id)
        return result, current_time

def show_possible_replies(flags, current_time, log_id):
    '''
    Returns string of possible replies to a log
    '''
    reply_id = logs_new.LOG_LINK_REPLIES[log_id]
    reply_ids = []
    # filter replies by flags
    possible_reply_codes = list(filter(lambda item: can_reply(flags,item), list(logs_new.LOG_REPLIES.keys())))
    # filter replies by log_id
    for repcode in possible_reply_codes:
        if repcode[:6] == reply_id and repcode[6] != "i":
            reply_ids.append(repcode)
    result = "\nEnter reply " + log_id + " followed by reply code. For eg: reply " + log_id + " a "
    for code in reply_ids:
        result += "\n\t" + code[6] + ": " + logs_new.LOG_REPLIES[code] + "; "
    return result


def read_log(flags,current_time):
    '''
    Returns log_id of latest log received
    '''
    # get list of time
    time_list = list(filter(lambda item: current_time - 4 <= item, list(logs_new.LOG_TIME.keys())))
    # sort log id by number (chronological)
    id_list = sorted(list(logs_new.LOGS_NEW.keys()),reverse=True)
    # filter log by time (logs that are visible by current time)
    log_list = []
    for i in id_list:
        for time in time_list:
            if i in logs_new.LOG_TIME[time]:
                log_list.append(i)
                break
    # remove empty log/log not written yet
    log_list = list(filter(lambda item: logs_new.LOGS_NEW[item] != "", log_list))
    # remove log that should not exist based on flags
    log_list = list(filter(lambda item: can_log_exist(flags,item),log_list))
    return log_list[0]

def can_log_exist(flags,log_id):
    '''
    Returns bool whether log can exist based on flags
    '''
    if not (log_id in list(logs_new.LOG_NEED_FLAGS.keys())): return True
    flag_needed = logs_new.LOG_NEED_FLAGS[log_id]
    return flag_needed in flags

def read_block(flags,current_time,block_id,is_old,group_id):
    '''
    Returns list of log IDs
    '''
    block_list = []
    
    if is_old:
        # get all matching log IDs
        id_list = sorted(list(logs.LOGS.keys()))
        for i in range(len(id_list)):
            if id_list[i][:4] == block_id:
                block_list.append(id_list[i])
    else:
        match_list = []
        # get all matching log IDs
        id_list = sorted(list(logs_new.LOGS_NEW.keys()))
        for i in range(len(id_list)):
            if id_list[i][:4] == block_id:
                match_list.append(id_list[i])
        # filter logs by time
        time_list = list(filter(lambda item: item >= current_time - 4, list(logs_new.LOG_TIME.keys())))
        for i in match_list:
            for time in time_list:
                if i in logs_new.LOG_TIME[time]:
                    block_list.append(i)
                    break
        # filter logs by flags
        block_list = list(filter(lambda item: can_log_exist(flags,item),block_list))
        # remove empty log/log not written yet
        block_list = list(filter(lambda item: logs_new.LOGS_NEW[item] != "", block_list))

    return block_list

def work(flags, current_time):
    '''
    Returns string of data cleaned up
    '''
    hour_list = sorted(list(schedule.WORK.keys()),reverse=True)
    for i in range(len(hour_list)):
        if current_time >= hour_list[i]:
            # raise linked flag
            if hour_list[i] in list(flag_work_triggers.keys()):
                flags[flag_work_triggers[hour_list[i]]] = True
            # update time
            current_time -= 1
            return "Deleting old log: " + schedule.WORK[hour_list[i]], current_time

def remote_access(flags, current_time, username, password):
    '''
    Returns string of result
    '''
    if username == "Chibi": return remote.RESULTS["Chibi"], current_time
    if username in list(remote.CREDENTIALS.keys()):
        if password == remote.CREDENTIALS[username]:
            # raise linked flag
            if username == "Cassilin":
                flags["Hack Cass"] = True
            elif username == "Luvluv":
                flags["Hack Luv"] = True
            # update time
            current_time -= 2
            return remote.RESULTS[username], current_time
        else:
            return "Wrong password", current_time
    else:
        return "Username not found", current_time

def contact(flags, current_time, wavelength):
    '''
    Returns network not found message
    '''
    global flag_contact
    # update flag count
    if wavelength in contact_red:
        flag_contact += 1
    if flag_contact == 10:
        flags["WIPED"] = True
    # update time
    current_time -= 1
    return "Network not found", current_time

def help(*args):
    '''
    Returns game tips
    '''
    flags = args[0]
    current_time = args[1]
    if len(args) == 2:
        tips  = "You are a Virtual Police Officer, UID Nekoi, address cat_fish@vsp.tc"
        tips += "\nYour job is to regularly delete old logs from earthline database - you can read the schedule by entering 'notes work'"
        tips += "\nAs a security officer, you are closely watched by the channel admin and regulatory bots - read your logs regularly and reply on time"
        tips += "\nDemTube is the universal platform for entertainment and learning - you can read the schedule by entering 'notes dt'"
        tips += "\nEnter 'help commands' for a list of possible commands"
        tips += "\n181us[enterread0000]a15fqcfascafcq"
        tips += "\n3u38u@#83i23[mission:contactoverspace]9wdsijnc9ds9ds9xd[survive:donotforgetlastpiece]l984mednsc"
        return tips, current_time
    else:
        key = args[2]
        if not (key in ["archive","files","commands","contacts"]):
            return "Invalid syntax", current_time
        if key == "contacts":
            tips = actions_help.get_contacts()
            return tips, current_time
        if key == "archive":
            tips = "Archive status:\nSome blocks may not be accessible unless you have root access"
            # basic blocks
            for key in list(blocks.BLOCKS.keys()):
                tips += "\n\t" + str(key)
                if blocks.BLOCKS[key]: tips += " - Unlocked"
                else: tips += " - Locked"
            # day 2 blocks
            if current_time <= 24:
                for key in list(blocks.BLOCKS_SPECIAL_TWO.keys()):
                    tips += "\n\t" + str(key)
                    if blocks.BLOCKS_SPECIAL_TWO[key]: tips += " - Unlocked"
                    else: tips += " - Locked"
            # root blocks
            if is_flag_triggered(flags,"Root Access"):
                tips += "\nHidden blocks:"
                for key in list(blocks.BLOCKS_ROOT.keys()):
                    tips += "\n\t" + str(key)
                    if blocks.BLOCKS_ROOT[key]: tips += " - Unlocked"
                    else: tips += " - Locked"
            return tips, current_time
        if key == "files":
            tips = "Files in memory:\n\t"
            for item in list(decodes.KEYFLAG.keys()):
                if decodes.KEYFLAG[item]:
                    tips += item + " "
            if is_flag_triggered(flags,"p5-9"):
                tips += "\n\tdo.bpt not.bpt forget.bpt "
            if is_flag_triggered(flags,"Remote Access"):
                tips += "remote.exe "
            if is_flag_triggered(flags,"Change Time"):
                tips += "time.exe "
            if is_flag_triggered(flags,"Decoder"):
                tips += "decode.exe "
            if is_flag_triggered(flags,"Assembled"):
                tips += "chibi.exe "
            if is_flag_triggered(flags,"Decode Cohab's relic"):
                tips += "overspace.exe "
            return tips, current_time
        if key == "commands":
            tips = actions_help.get_possible_commands(flags)
            return tips, current_time

def decode(flags, current_time, filename,key):
    '''
    Return string of result
    '''
    if not (filename in list(decodes.KEYMAP.keys())):
        return "Unable to decode", current_time
    if not decodes.KEYFLAG[filename]:
        return "Cannot find file", current_time
    if key != decodes.KEYMAP[filename]:
        return "Invalid key", current_time
    # raise linked flag
    if filename == "catgirl.bpt":
        flags["Decode Luca's relic"] = True
    elif filename == "Cohab.clf":
        flags["Decode Cohab's relic"] = True
    # update time
    current_time -= 2
    return decodes.RESULTS[filename], current_time

def root(flags, current_time):
    '''
    Returns string of result
    '''
    if is_flag_triggered(flags,"Root Access"):
        return "Already enabled root privilege", current_time
    else:
        # raise linked flag
        flags["Root Access"] = True
        # update time
        current_time -= 2
        return "Attempting to gain root access. Success. Syncing time settings. Success. Welcome back, Nekoi", current_time