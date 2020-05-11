import display

class Page(object):
    def __init__(self,page_id,sections,buttons=[]):
        self.num = page_id
        self.sections = sections
        self.buttons = []
        for button in buttons:
            if button in list(display.BUTTON_RECT.keys()):
                self.buttons.append(button)
    
    def has_id(self,num):
        return self.num == num

    def get_sections(self):
        return self.sections

    def get_buttons(self):
        return self.buttons

    def has_section(self,section_id):
        for section in self.sections:
            if section.has_id(section_id):
                return True
        return False
