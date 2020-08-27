import os
from flask import render_template, Blueprint, url_for
from portfolio_app.app_functions.info import *

portfolio = Blueprint('portfolio', __name__)

@portfolio.route('/tutor', methods =['GET','POST'])
def tutoring():
    path = r'C:\Users\Jaden\Desktop\Projects\Portfolio\portfolio_app\static\website_content'
    temp = get_about_me(url_for('static', filename='website_content/2_projects.txt'))
    nav = []
    return render_template('tutor.html', nav = nav, about_me=temp)
