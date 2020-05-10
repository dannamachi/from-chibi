from Section import Section
import constants
import tools

class ReadSection(Section):
    def __init__(self):
        Section.__init__(self, constants.SECT_READ, constants.RECT_READ)
        self.color = constants.BLUE
        self.lines = []
        self.start_line = 0
        self.end_line = 0
        self.max_row = 20

    def set_text(self,text):
        self.text = text
        self.lines = tools.divide_into_lines(self.text,30)
        # scrolling variables
        self.start_line = 0
        self.end_line = self.start_line + self.max_row
        if self.end_line > len(self.lines):
            self.end_line = len(self.lines)

    def shift_up_one_row(self):
        if self.start_line > 0:
            self.start_line -= 1
            self.end_line -= 1
    
    def shift_down_one_row(self):
        if self.end_line < len(self.lines):
            self.end_line += 1
            self.start_line += 1
        
    def render_font(self, font):
        '''
        Returns dictionary of rendered font=> loc
        '''
        rendered = {}
        index = 0
        for i in range(self.start_line,self.end_line):
            line = self.lines[i]
            font_img = font.render(line,True,self.color)
            font_loc = (self.dimension[0] + constants.OFF_READ[0], self.dimension[1] + constants.OFF_READ[1] + index * 20)
            index += 1
            rendered[font_img] = font_loc
        return rendered
