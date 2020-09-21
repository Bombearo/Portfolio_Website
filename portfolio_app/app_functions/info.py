from portfolio_app.app_functions.about import About 
from portfolio_app.app_functions.project import Project 
from portfolio_app.app_functions.contact import Contact 
def readfile(filepath):
    file = open(filepath)
    contents = file.read()
    file.close()
    return contents.split('\n\n')

def get_about_me(filepath):
    contents = readfile(filepath)
    title,first_line,content,buttons = contents[0], contents[1], contents[2], contents[3:]
    about = About(title,first_line,content,buttons,filepath)
    about.format_buttons()
    return about

def retrieve_contacts(filepath):
    contacts = Contact(filepath)
    return contacts.get_contacts()

def validate_table(table,tname):
    return table.query.filter_by(name=tname).first()

def get_projects(projects):
    if isinstance(projects,list):
        thumbnails = [project.thumbnails for project in projects]
        portfolio_thumbnails = [[media for media in thumbnail] for thumbnail in thumbnails]
        project_list = zip(projects,portfolio_thumbnails)
        return [Project(project.id,project.title,project.description,project.github_link,thumbnails,project.author) for project,thumbnails in project_list]
    thumbnails = [media for media in projects.thumbnails]
    return Project(projects.id,projects.title,projects.description,projects.github_link,thumbnails,projects.author)