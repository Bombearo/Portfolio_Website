import os
from flask import render_template, Blueprint, url_for
from portfolio_app.app_functions.info import *
from portfolio_app.models import *

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
def index():
    path = os.getcwd()+'/portfolio_app'+url_for('static', filename='website_content/1_about_me.txt')
    about_me = get_about_me(path)
    nav = [['about', 'About Me'],['projects', 'Projects'],['experience','Experience'],['contact', 'Contact Me']]
    slider = ['Student','Temp']
    user = User.query.first()
    return render_template('portfolio.html',nav = nav, about_me=about_me, slider=slider, user = user)
