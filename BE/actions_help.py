GENERAL_HELP = """1 block = 1 day = 12 time units (from unit 0 to unit 12)
Log reply ticket expires in 2-4 units
Reply regularly (except for Cass, she's a chatterbox)
Logs can be hidden anywhere so try to decode everything"""

DEMTUBE_HELP ="""Demtube schedule:
    D1 0 - 2   : getting root access
    D1 5 - 8   : encryption (note: good for bluffing)
    D1 9 - 10  : remote access tech (note: good for getting secret numbers)
    D2 0 - 2   : weird machines (note: Luv's favourite)
    D3 1 - 4   : decoding tech"""

WORK_HELP ="""Log to delete:
    D2 1 - 2   : something hidden by the govt
    D2 3 - 4   : prank to change the time (note: get them to send stuff twice)
    D2 9 - 10  : the truth of cybermite (note: does Luv need to know this?)
    D3 11 - 12 : suicide note from an aeternist"""

ADDRESS_TO_NAME = {\
    "chibisuke@vsp.tc"   : "weird kid",\
    "cat_fish@vsp.tc"    : "me",\
    "dt_81@fpu.tc"       : "Cass",\
    "em_81@fpu.tc"       : "Luv",\
}

CONTACT_COMMENTS = {\
    "chibisuke@vsp.tc"   : "kid who's got a virus, just bear with him for a while",\
    "cat_fish@vsp.tc"    : "always awesome",\
    "dt_81@fpu.tc"       : "history nerd, knows too much for her own good, expert with numbers",\
    "em_81@fpu.tc"       : "channel admin, likes kitts, cannot drink but drinks anyway",\
}

def is_flag_triggered(flags, flagname):
    '''
    Returns bool if flag is set
    '''
    if flagname in list(flags.keys()):
        return flags[flagname]
    return False

def get_contacts():
    '''
    Returns string with character info
    '''
    tips = "Address list: <Sorted: Recent>"
    for address in list(ADDRESS_TO_NAME.keys()):
        tips += "\n" + address + " - " + ADDRESS_TO_NAME[address] + ": " + CONTACT_COMMENTS[address]
    return tips

def get_possible_commands(flags):
    '''
    Returns string with possible commands
    '''
    tips = "help [commands | files | archive]: terminal info\n\n"
    tips += "notes [general | dt | work]: helpful info\n\n"
    tips += "dt: watch dtube\n\n"
    tips += "work: do vsp work\n\n"
    tips += "read [(block id)]: read latest log/read block\n\n"
    tips += "decrypt (block id): decrypt archive\n\n"
    tips += "decode (filename) (key): decode file\n\n"
    tips += "download (log id): save attachment from log\n\n"
    tips += "save: go to save menu\n\n"
    tips += "load: go to load menu\n\n"
    tips += "quit: quit the game\n\n"
    if is_flag_triggered(flags,"Change Time"):
        tips += "! time (address): change time of another terminal\n\n"
    if is_flag_triggered(flags,"Can Root Access"):
        tips += "! root: recover root access\n\n"
    if is_flag_triggered(flags,"Remote Access"):
        tips += "! remote (UID) (password): remote access another terminal\n\n"
    if is_flag_triggered(flags,"Assembled"):
        tips += "???chibi: run special command\n\n"
    if is_flag_triggered(flags,"Decode Cohab's relic"):
        tips += "! overspace: connect to Overspace - make sure your connection is uninterrupted\n\n"
    return tips