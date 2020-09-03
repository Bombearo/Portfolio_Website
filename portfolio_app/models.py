from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
from portfolio_app import db, login_manager
from flask_login import UserMixin

user_roles = db.Table('user_roles',
    db.Column('user_id',db.String(36),db.ForeignKey('users.id')),
    db.Column('role_id',db.String(60),db.ForeignKey('roles.id'))
)

project_tags = db.Table('project_tags',
    db.Column('portfolio_id',db.String(36),db.ForeignKey('portfolio.id')),
    db.Column('tag_id',db.String(60),db.ForeignKey('portfolio_tags.id'))
)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password_hash = db.Column(db.String(128))
    roles = db.relationship('Roles', secondary=user_roles, backref = db.backref("user_roles", lazy=True))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'
    
class Roles(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), index=True, unique=True)

    def __repr__(self):
        return f'<Role {self.title}>'
    
    
class Portfolio(db.Model):
    __tablename__ = 'portfolio'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), index=True, unique=True)
    thumbnail = db.Column(db.String(64), index=True, unique=True, nullable=True)
    description = db.Column(db.String(64), index=True, unique=True)
    github_link = db.Column(db.String(64), index=True, unique=True)
    author = db.Column(db.String(50), db.ForeignKey('users.id'))
    tags = db.relationship('Portfolio_tags', secondary=project_tags, backref = db.backref("project_tags", lazy=True))

    def __repr__(self):
        return f'<Project {self.title}>'

class Portfolio_tags(db.Model):
    __tablename__ = 'portfolio_tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)

    def __repr__(self):
        return f'<Tag {self.name}>'
    
