from Sections.Section import Section
import constants
import tools

class HelpfulSection(Section):
    def __init__(self):
        Section.__init__(self, constants.SECT_HELP, constants.RECT_HELP)
        self.color = constants.GREEN
        self.lines = []
        self.start_line = 0
        self.end_line = 0
        self.max_row = 18
        self.max_char = 16
        self.is_reset = True
    
    def reset(self):
        self.lines = []
        self.start_line = 0
        self.end_line = 0
        Section.reset(self)
        self.is_reset = True

    def set_text(self,text):
        self.text = text
        self.lines = tools.divide_into_lines(self.text,self.max_char)
        # scrolling variables
        if self.is_reset:
            self.is_reset = False
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
            # print(str(i) + " - " + str(len(self.lines)) + "\n")
            line = self.lines[i]
            font_img = font.render(line,True,self.color)
            font_loc = (self.dimension[0] + constants.OFF_HELP[0], self.dimension[1] + constants.OFF_HELP[1] + index * 20)
            index += 1
            rendered[font_img] = font_loc
        return rendered
