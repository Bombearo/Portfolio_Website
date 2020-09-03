from portfolio_app.app_functions.about import About 
def readfile(filepath):
    file = open(filepath)
    contents = file.read()
    file.close()
    return contents.split('\n')

def get_about_me(filepath):
    contents = readfile(filepath)
    title,first_line,content,buttons = contents[0], contents[1], contents[2], contents[3:]
    return About(title,first_line,content,buttons,filepath)