import pygame

from Section import Section
import constants
import tools

class EndSection(Section):
    def __init__(self):
        Section.__init__(self, constants.SECT_END, constants.RECT_END)
        self.color = constants.GREEN
        self.lines = []
        self.max_char = 70
        self.count = 1

    def finished(self):
        return self.count == len(self.lines)

    def set_text(self,text):
        self.count = 1
        self.text =  text
        self.text = "Press enter to proceed\n" + self.text
        self.lines = tools.divide_into_lines(self.text,self.max_char)

    def advance(self):
        if self.count < len(self.lines):
            self.count += 1
    
    def render_font(self, font):
        rendered = {}
        index = 0
        for i in range(self.count):
            line = self.lines[i]
            font_img = font.render(line,True,self.color)
            font_loc = (self.dimension[0] + constants.OFF_END[0], self.dimension[1] + constants.OFF_END[1] + index * 20)
            index += 1
            rendered[font_img] = font_loc
        return rendered