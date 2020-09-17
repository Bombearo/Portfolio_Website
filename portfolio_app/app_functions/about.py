from flask import url_for
import re
class About:
    def __init__(self,title,first_line,content,buttons,path):
        self.title = title
        self.first_line = first_line
        self.content = content
        self.buttons = buttons
        self.id = title.lower().split(' ')[0]
        self.path = path

    def format_buttons(self):
        self.buttons = [button.split(',') for buttons in self.buttons for button in buttons.split('\n')]
    
    def write_content(self):
        content = re.sub(r'\n+','', self.content)
        buttons = [','.join(button) for button in self.buttons]
        buttons = '\n'.join(buttons)
        file = open(self.path,'w')
        file.write(self.title+'\n\n')
        file.write(self.first_line+'\n\n')
        file.write(content+'\n\n')
        for button in buttons:
            if button:
                file.write(button)
        file.close()