from Section import Section
import constants
import api

class MainSection(Section):
    def __init__(self):
        Section.__init__(self, constants.SECT_MAIN, constants.RECT_MAIN)

    def run_command(self):
        api.run_command(12, "restart")