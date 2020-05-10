import pygame
import constants
import api

class Section(object):
    def __init__(self, num, dimension = constants.RECT_SCREEN):
        self.num = num
        self.text = ""
        self.dimension = dimension
        self.color = constants.GREEN

    def __eq__(self, aSect):
        return self.num == aSect.num 

    def __ne__(self, aSect):
        return self.num != aSect.num

    def has_id(self,num):
        return self.num == num

    def set_stale(self):
        pass

    def get_text(self):
        return self.text

    def get_dimension(self):
        return self.dimension

    def set_text(self, text):
        self.text = text

    def render_font(self, font):
        '''
        Returns dictionary of rendered font=> loc
        '''
        return {}


            

    