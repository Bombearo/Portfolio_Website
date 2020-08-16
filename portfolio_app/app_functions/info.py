from portfolio_app.app_functions.about import About 
def readfile(filepath):
    file = open(filepath)
    contents = file.read()
    file.close()
    return contents.split('\n')

def get_about_me(filepath):
    path = r'C:\Users\Jaden\Desktop\Projects\Portfolio\portfolio_app\\'+filepath
    contents = readfile(path)
    title,first_line,content = contents[0], contents[1], contents[2:]
    return About(title,first_line,content)