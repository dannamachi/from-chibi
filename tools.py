def divide_into_lines(text_string, max_char):
    '''
    Assumes text_string is sectioned by /n
    Returns array of string
    '''
    sections = text_string.split('\n')
    lines = []
    for section in sections:
        segment_num = int(len(section) / max_char)
        remainder = len(section) - max_char * segment_num
        for index in range(segment_num):
            lines.append(section[index * max_char:(index + 1) * max_char])
        if remainder > 0:
            lines.append(section[segment_num * max_char:])
    return lines