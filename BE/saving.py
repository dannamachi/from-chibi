import json

TOTAL_SAVE_SLOT = 20

def initialize_save():
    '''
    Initializes save file with slots
    Returns bool for success
    '''
    DATA_SAVES = {'Success' : 1}
    for index in range(TOTAL_SAVE_SLOT):
        DATA_SAVES[index] = {}
        DATA_SAVES[index]['Filled'] = 0
    with open('saves.dat', 'w') as savefile:
        json.dump(DATA_SAVES, savefile)
        save_success = True
    return save_success
    

def read_data_from_file():
    '''
    Returns dictionary of saves
    '''
    DATA_SAVES = {'Success' : 0}
    # read from file
    with open('saves.dat') as json_file:
        DATA_SAVES = json.load(json_file)
        return DATA_SAVES

def format_time(isRoot,current_time):
    '''
    Returns string of formatted time
    '''
    if current_time > 24:
        day_int = 3
        time_offset = 24
    elif current_time > 12:
        day_int = 2
        time_offset = 12
    else:
        day_int = 1
        time_offset = 0
    if not isRoot:
        time = current_time - time_offset
    else:
        day_int = 4 - day_int
        time = 12 - (current_time - time_offset)
    return 'Day ' + str(day_int) + " Time " + str(time)

def read_save():
    '''
    Returns string of result
    '''
    DATA_SAVES = read_data_from_file()
    if DATA_SAVES['Success'] != 1:
        return 'Unable to load save file'
    tips = "Save slots:"
    for index in range(TOTAL_SAVE_SLOT):
        slot = str(index)
        isFilled = DATA_SAVES[slot]['Filled']
        if isFilled == 1:
            time = DATA_SAVES[slot]['TIME']
            isRoot = 'Root Access' in DATA_SAVES[slot]['FLAGS']
            time_string = format_time(isRoot,time)
            tips += "\n" + str(slot) + ": " + time_string + " (Root: " + str(isRoot) +")"
        else:
            tips += "\n" + str(slot)
    return tips

def save_data_to_file(\
    flags, current_time, flag_contact, day_check, decrypt_track,\
    blocks, blocks_root, blocks_two, blocks_three, blocks_new,\
    keyflag, logs_new, logs_need_replies, log_attachment,\
    slot_index):
    '''
    Writes data dictionaries to file
    Returns bool whether succeeds
    '''
    slot_index = str(slot_index)
    # read from file
    DATA_SAVES = read_data_from_file()
    if DATA_SAVES['Success'] != 1:
        return False
    save_success = False
    # save to file
    DATA_SAVES[slot_index] = {}
    DATA_SAVES[slot_index]["FLAGS"] = flags
    DATA_SAVES[slot_index]["TIME"] = current_time
    DATA_SAVES[slot_index]["CONTACTCOUNT"] = flag_contact
    DATA_SAVES[slot_index]["DAYCHECK"] = day_check
    DATA_SAVES[slot_index]["DECRYPT"] = decrypt_track
    DATA_SAVES[slot_index]["BLOCKS"] = blocks
    DATA_SAVES[slot_index]["BLOCKSROOT"] = blocks_root
    DATA_SAVES[slot_index]["BLOCKSTWO"] = blocks_two
    DATA_SAVES[slot_index]["BLOCKSTHREE"] = blocks_three
    DATA_SAVES[slot_index]["BLOCKSNEW"] = blocks_new
    DATA_SAVES[slot_index]["DECODES"] = keyflag
    DATA_SAVES[slot_index]["LOGSNEW"] = logs_new
    DATA_SAVES[slot_index]["LOGSREPLY"] = logs_need_replies
    DATA_SAVES[slot_index]["LOGSATTACHMENT"] = log_attachment
    DATA_SAVES[slot_index]['Filled'] = 1

    with open('saves.dat', 'w') as savefile:
        json.dump(DATA_SAVES, savefile)
        save_success = True

    return save_success 
