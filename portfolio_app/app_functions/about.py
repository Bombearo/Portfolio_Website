class About:
    def __init__(self,title,first_line,content):
        self.title = title
        self.first_line=first_line
        self.content = content
        self.id = title.lower().split(' ')[0]