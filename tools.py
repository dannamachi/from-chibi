# def divide_into_lines(text_string, max_char):
#     '''
#     Assumes text_string is sectioned by /n
#     Returns array of string
#     '''
#     sections = text_string.split('\n')
#     lines = []
#     for section in sections:
#         segment_num = int(len(section) / max_char)
#         remainder = len(section) - max_char * segment_num
#         for index in range(segment_num):
#             lines.append(section[index * max_char:(index + 1) * max_char])
#         if remainder > 0:
#             lines.append(section[segment_num * max_char:])
#     return lines

def divide_into_lines(text_string, max_char):
    '''
    Assumes text_string is sectioned by \n and word divided by space
    Returns array of string
    '''
    # divide into sections by \n
    sections = text_string.split('\n')
    lines = []
    for section in sections:
        # get all words in section
        words = section.strip().split(' ')
        while True:
            segment_string = ""
            # add word to segment string until reached max_char
            while True:
                segment_string += words.pop(0) + " "
                # check still have word left
                if len(words) == 0:
                    break
                if len(segment_string) + len(words[0]) > max_char:
                    break
            lines.append(segment_string)
            # check still have word left
            if len(words) == 0:
                break
    return lines

