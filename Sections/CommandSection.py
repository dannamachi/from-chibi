from Sections.Section import Section
import api
import constants

class CommandSection(Section):
    def __init__(self):
        Section.__init__(self, constants.SECT_CLI, constants.RECT_CLI)
        self.command = -1
        self.arguments = []
        self.past_commands = []
        self.past_index = -1
        self.color = constants.GREEN
    
    def reset(self):
        self.command = -1
        self.arguments = []
        Section.reset(self)

    def set_text(self,text):
        if len(text) < 70:
            self.text = text

    def reverse_one_command(self):
        if len(self.past_commands) + self.past_index >= 0 :
            self.text = self.past_commands[self.past_index]
            self.past_index -= 1
            
    def forward_one_command(self):
        if self.past_index < -1:
            self.past_index += 1
            self.text = self.past_commands[self.past_index]

    def process_command(self):
        if len(self.past_commands) == 0:
            self.past_commands.append(self.text)
        elif self.past_commands[-1] != self.text:
            self.past_commands.append(self.text)
        self.past_index = -1
        command_list = self.text.strip().split(' ')
        if len(command_list) > 0:
            # check that command is valid for this section
            for num, key in constants.ACTIONS.items():
                if command_list[0] == key:
                    self.command = num
                    break
            # if it is, set the corresponding arguments
            if self.command != -1:
                if len(command_list) > 1:
                    self.arguments = [*command_list[1:]]
                self.text = ""


    # Success bool, error code
    # -1 Invalid
    #  0 Is quit
    #  1 Root 
    #  2 No flag
    #  3 Invalid syntax
    #  4 Success
    #  5 Save
    #  6 Load
    def run_command(self):
        '''
        Returns text and section id to show that text
        '''
        if self.command != -1:
            text, section_id =  api.run_game_command(self.command, *self.arguments)
            self.command = -1
            self.arguments = []
            return text, section_id
        else:
            return "Command not found", constants.SECT_MSG

    def render_font(self, font):
        '''
        Returns dictionary of rendered font=> loc
        '''
        rendered = {}
        font_img = font.render("Nekoi>> " + self.text, True, self.color)
        font_loc = (self.dimension[0] + constants.OFF_CLI[0], self.dimension[1] + constants.OFF_CLI[1] + 5)
        rendered[font_img] = font_loc
        return rendered
        
