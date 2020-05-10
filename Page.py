class Page(object):
    def __init__(self,page_id,sections):
        self.num = page_id
        self.sections = sections
    
    def has_id(self,num):
        return self.num == num

    def get_sections(self):
        return self.sections

    def has_section(self,section_id):
        for section in self.sections:
            if section.has_id(section_id):
                return True
        return False
