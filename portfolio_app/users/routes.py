import os
from flask import render_template, url_for, flash, redirect, request, Blueprint, abort
from flask_login import login_user, current_user, logout_user, login_required
from portfolio_app import db
from portfolio_app.app_functions.info import *
from portfolio_app.models import User, Portfolio
from portfolio_app.users.forms import *
from portfolio_app.users.utils import save_picture

users = Blueprint('users', __name__)

@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
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
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your details have been updated!','success')
        return redirect(url_for('main.index'))
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
        flash('Your details have been updated!','success')
        return redirect(url_for('users.admin'))
    elif request.method == 'GET':
        form.first_line.data = about_me.first_line
        form.about.data = about_me.content

    return render_template('tutor.html', title='Account', form = form)

@users.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page',1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page = page, per_page=5)
    return render_template('user_posts.html', posts=posts, user = user)

@users.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author = current_user)
        if form.media.data:
            media_file = save_picture(form.media.data)
            post.media = media_file
        
        db.session.add(post)
        db.session.commit()        
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post', form = form, legend = 'New Post')

@users.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post = post)

@users.route('/post/<int:post_id>/update', methods = ['GET','POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        if form.media.data:
            picture_file = save_picture(form.media.data)
            post.media = picture_file
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!','success')
        return redirect(url_for('main.home'))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title="Update Post", post = post, 
                            form=form, legend = 'Update Post')

@users.route('/post/<int:post_id>/delete',methods = ['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author!=current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))
