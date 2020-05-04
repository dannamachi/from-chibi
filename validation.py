def check_notes(*args):
    '''
    Returns bool if argument list is valid for notes(flags,current_time) or notes(flags,current_time,key)
    '''
    return len(args) == 2 or len(args) == 3

def check_dt(*args):
    '''
    Returns bool if argument list is valid for demtube(flags,current_time)
    '''
    return len(args) == 2

def check_decrypt(*args):
    '''
    Returns bool if argument list is valid for decrypt(flags,current_time,block_id)
    '''
    return len(args) == 3

def check_read(*args):
    '''
    Returns bool if argument list is valid for read(flags,current_time) or read_block(flags,current_time,current_id)
    '''
    return len(args) == 2 or len(args) == 3

def check_work(*args):
    '''
    Returns bool if argument list is valid for work(flags,current_time)
    '''
    return len(args) == 2

def check_remote(*args):
    '''
    Returns bool if argument list is valid for remote_access(flags,current_time,username,password)
    '''
    return len(args) == 4

def check_contact(*args):
    '''
    Returns bool if argument list is valid for contact(flags,current_time,wavelength)
    '''
    return len(args) == 3

def check_help(*args):
    '''
    Returns bool if argument list is valid for help(flags,current_time)
    '''
    return len(args) == 2

def check_decode(*args):
    '''
    Returns bool if argument list is valid for decode(flags,current_time,filename,key)
    '''
    return len(args) == 4

def check_root(*args):
    '''
    Returns bool if argument list is valid for root(flags,current_time)
    '''
    return len(args) == 2

def check_reply(*args):
    '''
    Returns bool if argument list is valid for reply(flags,current_time,log_id) or reply(flags,current_time,log_id,choice)
    '''
    return len(args) == 3 or len(args) == 4

def check_time(*args):
    '''
    Returns bool if argument list is valid for time_change(flags,current_time,terminal_id)
    '''
    return len(args) == 3

def check_overspace(*args):
    '''
    Returns bool if argument list is valid for overspace(flags,current_time)
    '''
    return len(args) == 2

def check_save(*args):
    '''
    Returns bool if argument list is valid for save(flags,current_time)
    '''
    return len(args) == 2

def check_load(*args):
    '''
    Returns bool if argument list is valid for load(flags,current_time)
    '''
    return len(args) == 2
