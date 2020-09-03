from flask import url_for
class About:
    def __init__(self,title,first_line,content,buttons,path):
        self.title = title
        self.first_line = first_line
        self.content = content.replace('|','\n')
        self.buttons = [button.split(',') for button in buttons]
        self.id = title.lower().split(' ')[0]
        self.path = path
    
    def write_content(self):
        buttons = [button.join(',') for button in self.buttons]
        buttons = '\n'.join(buttons)
        file = open(self.path,'w')
        file.write(f'{self.title}')
        file.write(f'{self.first_line}')
        file.close()