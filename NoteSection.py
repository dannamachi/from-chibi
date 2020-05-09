from Section import Section
import constants
import tools

class NoteSection(Section):
    def __init__(self):
        Section.__init__(self, constants.SECT_NOTE, constants.RECT_NOTE)
        self.color = constants.CYAN

    def render_font(self, font):
        '''
        Returns dictionary of rendered font=> loc
        '''
        rendered = {}
        lines = tools.divide_into_lines(self.text,30)
        index = 0
        for line in lines:
            font_img = font.render(line,True,self.color)
            font_loc = (self.dimension[0] + constants.OFF_NOTE[0], self.dimension[1] + constants.OFF_NOTE[1] + index * 30)
            index += 1
            rendered[font_img] = font_loc
        return rendered
        
