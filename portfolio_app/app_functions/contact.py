class Contact:
    def __init__(self, path, contact='tempEmail@outlook.co.uk'):
        self.contact = contact
        self.path = path
    
    def write_contact(self):
        file = open(self.path,'w')
        file.write(self.contact+'\n')
        file.close()

    def get_contacts(self):
        file = open(self.path,'r')
        contents = file.read()
        file.close()
        return contents