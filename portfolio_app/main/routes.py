import os
from flask import render_template, Blueprint, url_for
from portfolio_app.app_functions.info import *
from portfolio_app.models import *

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
def index():
    a_path = os.getcwd()+'/portfolio_app'+url_for('static', filename='website_content/1_about_me.txt')
    c_path = os.getcwd()+'/portfolio_app'+url_for('static', filename='website_content/2_contact_me.txt')
    about_me = get_about_me(a_path)
    nav = [['about', 'About Me'],['projects', 'Projects'],['contact', 'Contact Me']]
    slider = ['Student']
    user = User.query.first()
    projects =Portfolio.query.all()
    my_projects = get_projects(projects)
    contacts = retrieve_contacts(c_path)
    return render_template('portfolio.html',title = 'Home', nav = nav, about_me=about_me, slider=slider, user = user,projects=my_projects, contact=contacts)
