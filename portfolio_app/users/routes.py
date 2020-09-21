import os
from flask import render_template, url_for, flash, redirect, request, Blueprint, abort
from flask_login import login_user, current_user, logout_user,login_required
from flask_security import roles_required
from portfolio_app import db
from portfolio_app.app_functions.info import *
from portfolio_app.app_functions.about import About
from portfolio_app.app_functions.contact import Contact
from portfolio_app.models import *
from portfolio_app.users.forms import *
from portfolio_app.users.utils import *


users = Blueprint('users', __name__)

def restricted(access_level):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            roles = [str(role) for role in current_user.roles]
            if access_level not in roles:
                abort(403)
            return func(*args, **kwargs)
        return wrapper
    return decorator

def password_change(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if current_user.check_password('AdminPass'):
            flash('You must change your password to securely manage your website','warning')
            return redirect(url_for('users.account'))
        return func(*args,**kwargs)
    return wrapper

@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('users.admin'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('users.admin'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form,user=User.query.first())


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@users.route("/admin", methods =['GET','POST'])
@login_required
@restricted(access_level='Admin')
@password_change
def admin():
    return render_template('admin.html', title='Account',user=current_user)

@users.route('/projects')
def projects():
    projects = Portfolio.query.all()
    user=User.query.first()
    my_projects = get_projects(projects)
    return render_template('projects.html', title='My Projects', user=user, projects=my_projects)

@users.route('/projects/<int:project_id>')
def project(project_id):
    project = Portfolio.query.get_or_404(project_id)
    my_projects = get_projects(project)
    user = User.query.first()
    print(project.thumbnails)
    return render_template('project.html', title=project.title, project = my_projects,user=user)

@users.route("/admin/account", methods =['GET','POST'])
@login_required
@restricted(access_level='Admin')
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.alias = form.name.data
        if form.password.data:
            current_user.set_password(form.password.data)
        if form.picture.data:
            picture_file = save_image(form.picture.data,'profile_pics',720,720)
            current_user.profile_pic = picture_file
        db.session.commit()
        flash('Your details have been updated!','success')
        return redirect(url_for('users.admin'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.name.data = current_user.alias
    return render_template('account.html', title='Account',form = form,user=current_user)

@users.route("/admin/about", methods=['GET', 'POST'])
@login_required
@restricted(access_level='Admin')
@password_change
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
        new_about = About(title,first_line,content,buttons,path)
        new_about.write_content()
        flash('Your details have been updated!','success')
        return redirect(url_for('users.admin'))
    elif request.method == 'GET':
        form.first_line.data = about_me.first_line
        form.about.data = about_me.content
        if '' not in about_me.buttons[0]:
            form.button_1_text.data = about_me.buttons[0][0]
            form.button_1_link.data = about_me.buttons[0][1]
        if '' not in about_me.buttons[1]:
            form.button_2_text.data = about_me.buttons[1][0]
            form.button_2_link.data = about_me.buttons[1][1]

    return render_template('edit_about.html', title='Account', form = form,user=current_user)

@users.route("/admin/new_project", methods=['GET', 'POST'])
@login_required
@restricted(access_level='Admin')
@password_change
def new_project():
    form = PortfolioForm()
    if form.validate_on_submit():
        project = Portfolio(title=form.title.data, description=form.description.data,github_link=form.github_link.data, author = current_user.id)
        db.session.add(project)
        db.session.commit()

        thumbnails = request.files.getlist('thumbnails')
   
        for thumbnail in thumbnails:
            if thumbnail and allowed_file(thumbnail.filename):
                media_file = save_image(thumbnail,'thumbnails',1280,720)
                media = Portfolio_Media(thumbnail=media_file,project_id=project.id)
                db.session.add(media)
        db.session.commit()
        tags = form.tags.data.split()
        if tags:
            for tag in tags:
                if not validate_table(Portfolio_tags,tag):
                    t = Portfolio_tags(name=tag)
                    db.session.add(t)
                    db.session.commit()
                else:
                    t = Portfolio_tags.query.filter_by(name=tag)
                t.project_tags.append(project)
        db.session.commit()
        
        
        flash('Your project has been added!', 'success')
        return redirect(url_for('users.admin'))
    return render_template('add_project.html', form = form, legend = 'New Post',user=current_user)  



@users.route('/projects/<int:project_id>/update', methods = ['GET','POST'])
@login_required
@restricted(access_level='Admin')
@password_change
def update_project(project_id):
    project = Portfolio.query.get_or_404(project_id)
    if project.author != current_user.id:
        abort(403)
    form = PortfolioForm()
    if form.validate_on_submit():
        if 'thumbnails' not in request.files:
            flash('No file part')
            return redirect(request.url)
        project.title = form.title.data
        project.description = form.description.data
        project.github_link = form.github_link.data
        db.session.commit()

        thumbnails = request.files.getlist('thumbnails')
   
        for thumbnail in thumbnails:
            print(thumbnail)
            if thumbnail and allowed_file(thumbnail.filename):
                media_file = save_image(thumbnail,'thumbnails',1280,720)
                media = Portfolio_Media(thumbnail=media_file,project_id=project.id)
                db.session.add(media)
                db.session.commit()
        flash('Project Successfully Updated!')
        return redirect(url_for('users.admin'))
    elif request.method == 'GET':
        form.title.data = project.title
        form.description.data = project.description
        form.github_link.data = project.github_link
    return render_template('add_project.html', title="Update Project", project = project, 
                            form=form, legend = 'Update Project',user=current_user)

@users.route('/projects/<int:project_id>/delete',methods = ['POST'])
@login_required
@restricted(access_level='Admin')
@password_change
def delete_project(project_id):
    project = Portfolio.query.get_or_404(project_id)
    if project.author!=current_user.id:
        abort(403)
    for thumbnail in project.thumbnails:
        db.sesion.delete(thumbnail)
    db.session.delete(project)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('users.admin'))

@users.route('/admin/contact', methods=['GET','POST'])
@login_required
@restricted(access_level='Admin')
@password_change
def update_contacts():
    form = UpdateContactForm()
    user = User.query.first()
    path = os.getcwd()+'/portfolio_app'+url_for('static', filename='website_content/2_contact_me.txt')
    contacts = Contact(path)
    if form.validate_on_submit(): 
        contacts = Contact(path,form.email.data,form.github_profile.data)
        contacts.write_contact()
        flash('Contacts Successfully Updated!','success')
        return redirect(url_for('users.admin'))
    elif request.method == 'GET':
        c = contacts.get_contacts()
        form.email.data = c[0]
        form.github_profile.data = c[1].split('/')[-1]

    return render_template('contacts.html', form=form,user=user )