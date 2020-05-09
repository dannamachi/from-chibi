from Section import Section
import constants
import tools

class MessageSection(Section):
    def __init__(self):
        Section.__init__(self, constants.SECT_MSG, constants.RECT_MSG)
        self.color = constants.GREEN

    def render_font(self, font):
        '''
        Returns dictionary of rendered font=> loc
        '''
        rendered = {}
        lines = tools.divide_into_lines(self.text,50)
        index = 0
        for line in lines:
            font_img = font.render(line,True,self.color)
            font_loc = (self.dimension[0] + constants.OFF_MSG[0], self.dimension[1] + constants.OFF_MSG[1] + index * 30)
            index += 1
            rendered[font_img] = font_loc
        return rendered
        
        
