import os
from flask import render_template, url_for, flash, redirect, request, Blueprint, abort
from flask_login import login_user, current_user, logout_user, login_required
from portfolio_app import db
from portfolio_app.app_functions.info import *
from portfolio_app.app_functions.about import About
from portfolio_app.models import User, Portfolio
from portfolio_app.users.forms import *
from portfolio_app.users.utils import save_picture

users = Blueprint('users', __name__)

@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('users.admin'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('users.admin'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@users.route("/admin", methods =['GET','POST'])
@login_required
def admin():
    return render_template('admin.html', title='Account')

@users.route("/admin/account", methods =['GET','POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your details have been updated!','success')
        return redirect(url_for('users.admin'))
    elif request.method == 'GET':
        form.username.data = current_user.username 
        form.email.data = current_user.email 
    return render_template('account.html', title='Account',form = form)


@users.route("/admin/about", methods=['GET', 'POST'])
@login_required
def edit_about():
    form = EditAboutForm()
    path = os.getcwd()+'/portfolio_app'+url_for('static', filename='website_content/1_about_me.txt')
    about_me = get_about_me(path)
    if form.validate_on_submit():
        title = 'About Me'
        first_line = form.first_line.data
        content = form.about.data
        button_1 = [form.button_1_text.data,form.button_1_link.data]
        button_2 = [form.button_2_text.data,form.button_2_link.data]
        buttons = [button_1,button_2]
        print(buttons)
        new_about = About(title,first_line,content,buttons,path)
        new_about.write_content()
        flash('Your details have been updated!','success')
        return redirect(url_for('users.admin'))
    elif request.method == 'GET':
        form.first_line.data = about_me.first_line
        form.about.data = about_me.content
        if about_me.buttons:
            form.button_1_text.data = about_me.buttons[0][0]
            form.button_1_link.data = about_me.buttons[0][1]
            if len(about_me.buttons)>1:
                form.button_2_text.data = about_me.buttons[1][0]
                form.button_2_link.data = about_me.buttons[1][1]

    return render_template('edit_about.html', title='Account', form = form)

