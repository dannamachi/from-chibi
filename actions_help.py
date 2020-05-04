GENERAL_HELP = """1 block = 1 day = 12 time units (from unit 0 to unit 12)
Log reply ticket expires in 2-4 units
Reply regularly (except for Cass, she's a chatterbox)
Logs can be hidden anywhere so try to decode everything"""

DEMTUBE_HELP ="""Demtube schedule:
    D1 0 - 2   : security bypass (note: enter root)
    D1 5 - 8   : encryption (note: watch this to bluff to Luv)
    D1 9 - 10  : remote access tech (note: get everyone else's secret key)
    D2 0 - 2   : weird machines (note: Luv seems to like the kitts)
    D2 9 - 12  : decryption tech
    D3 1 - 4   : decoding tech"""

WORK_HELP ="""Log to delete:
    D1 9 - 10  : scandal from 6100
    D2 1 - 2   : something hidden by the govt
    D2 5 - 6   : prank to change the time (note: get them to send stuff twice)
    D2 9 - 10  : the truth of cybermite (note: is this related to Luv?)
    D3 11 - 12 : suicide note from an aeternist"""

ADDRESS_TO_NAME = {\
    "chibisuke@vsp.tc"   : "new kid",\
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
    tips = "NOTE: Ensure you already have root access. Check notes for details\n"
    tips += "\nEnter help for general info, or help [commands/files/archive/contacts] for specific info"
    tips += "\nEnter notes to read all notes, or notes [general/dt/work] to read notes in that section"
    tips += "\nEnter dt to watch demtube. Your main source of info"
    tips += "\nEnter work to delete log from earthline database"
    tips += "\nEnter read to check only the latest log received/sent"
    tips += "\nEnter read [block id] to read all logs in a block (first 4 numbers of log id)"
    tips += "\nEnter decrypt [block id] to unlock old logs"
    tips += "\nEnter reply [log id] to check if you can reply to a log"
    tips += "\nEnter reply [log id] to save attachment from a new log"
    tips += "\nEnter quit to quit the session"
    if is_flag_triggered(flags,"Change Time"):
        tips += "\n! Enter time [UID] to change the time of another terminal"
    if is_flag_triggered(flags,"Can Root Access"):
        tips += "\n! Enter root to get root access"
    if is_flag_triggered(flags,"Remote Access"):
        tips += "\n! Enter remote [UID] [password] to remote access another terminal"
    if is_flag_triggered(flags,"Decoder"):
        tips += "\n! Enter decode [file name] [key] to decode a file"
    if is_flag_triggered(flags,"Decode Cohab's relic"):
        tips += "\n! Enter overspace to connect to Overspace - make sure your connection is uninterrupted"
    return tips