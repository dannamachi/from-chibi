from Sections.Section import Section
import constants
import api

class LoadSection(Section):
    def __init__(self):
        Section.__init__(self, constants.SECT_LOAD, constants.RECT_SLOT)
        self.button = -1
        self.selected = ""
        self.slot_info = []
        self.text = "LOADING"
        self.color = constants.MAGENTA
    
    def get_selected(self):
        return self.selected

    def is_selected(self):
        return self.button != -1

    def reset(self):
        self.button = -1
        self.selected = ""

    def get_slot_info(self, index):
        if len(self.slot_info) > 0:
            return self.slot_info[index]
        else:
            return "Unavailable"

    def reload(self):
        result, info = api.get_save_slot_info()
        if result:
            self.slot_info = info.split('\n')
            self.slot_info.pop(0)
        else:
            self.slot_info = []

    def set_restart(self):
        self.button = -2

    def select(self, button_name):
        if (button_name[:4] == "SLOT"):
            self.button = int(button_name.split(' ')[1]) - 1
            self.selected = button_name

    def run_command(self):
        if self.button != -1:
            if self.button == -2:
                self.button = 'restart'
            result, text = api.run_command(12,self.button)
            self.reset()
            return result, text
        else:
            return False, "Unable to load"

    def render_font(self,font):
        rendered = {}
        font_img = font.render(self.text,True,self.color)
        font_loc = constants.OFF_SAVE
        rendered[font_img] = font_loc
        return rendered