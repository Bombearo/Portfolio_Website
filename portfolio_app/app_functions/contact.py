class Contact:
    def __init__(self, path, email='tempEmail@outlook.co.uk',github = 'Temp'):
        self.email = email
        if r'https://github.com' in github:
            self.github = github 
        self.github= r'https://github.com/'+github
        self.path = path
    
    def __str__(self):
        return self.github

    def write_contact(self):
        file = open(self.path,'w')
        file.write(self.email+'\n')
        file.write(self.github)
        file.close()

    def get_contacts(self):
        file = open(self.path,'r')
        contents = file.read()
        file.close()
        return contents.split('\n')